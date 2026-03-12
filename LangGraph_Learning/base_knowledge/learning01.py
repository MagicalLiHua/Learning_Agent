from typing import TypedDict, Annotated
import operator

# 1. 定义图的状态 (State)
class AgentState(TypedDict):
    # Annotated[类型, 更新函数] 是 LangGraph 状态管理的核心
    messages: Annotated[list, operator.add]
    user_name: str

# 2. 定义一个普通的节点函数 (Node)
def greeting_node(state: AgentState):
    print(f"读取到之前的信息: {state.get('messages', [])}")
    # 节点只返回需要更新的字段，这里我们新增一条消息
    return {"messages": ["Hello from greeting_node!"]}

from langgraph.graph import StateGraph, START, END

# 1. 初始化状态图，传入我们定义的 State 骨架
graph_builder = StateGraph(AgentState)

# 2. 添加节点：给节点起个名字 "greeting"，并绑定具体的函数
graph_builder.add_node("greeting", greeting_node)

# # 3. 添加边：定义执行流向
# graph_builder.add_edge(START, "greeting") # 从起点走向 greeting 节点
# graph_builder.add_edge("greeting", END)   # 执行完后走向终点

# 1. 定义一个路由函数（交通警察）
def should_continue(state: AgentState):
    # 读取最新的消息
    last_message = state["messages"][-1]

    # 简单的逻辑判断：如果用户说 "再见"，就结束；否则去工具节点
    if "再见" in last_message:
        return "end"
    else:
        return "continue"


# 2. 在图里添加条件边
# 参数1: 起始节点
# 参数2: 路由函数
# 参数3: 映射字典 (路由函数的返回值 -> 实际的节点名称或终点)
graph_builder.add_conditional_edges(
    "greeting",  # 从 greeting 节点出来后开始判断
    should_continue,  # 调用这个函数做决定
    {
        "end": END,  # 如果函数返回 "end"，就走向图的终点
        "continue": "tools"  # 如果函数返回 "continue"，就走向名为 "tools" 的节点
    }
)

# 4. 编译成可执行的程序
app = graph_builder.compile()

# 运行测试
app.invoke({"messages": [], "user_name": "TestUser"})