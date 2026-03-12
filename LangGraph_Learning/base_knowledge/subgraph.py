from operator import add
from typing import TypedDict, Annotated
from langgraph.constants import END
from langgraph.graph import StateGraph, MessagesState, START

class State(TypedDict):
    """
    定义状态类，用于存储图节点间传递的消息状态
    messages: 使用add函数合并的字符串列表消息
    """
    messages: Annotated[list[str], add]

def sub_node(state:State) -> MessagesState:
    # 子图节点处理函数，接收当前状态并返回响应消息
    # @param state 当前状态对象，包含消息列表
    # @return 包含子图响应消息的新状态
    return {"messages": ["response from subgraph"]}

# 创建子图构建器并配置节点和边
subgraph_builder = StateGraph(State)
subgraph_builder.add_node("sub_node", sub_node)
subgraph_builder.add_edge(START, "sub_node")
subgraph_builder.add_edge("sub_node", END)
subgraph = subgraph_builder.compile()

# 绘制子图结构图
# subgraph.get_graph().draw_png('./subgraph.png')

# 创建主图构建器并添加子图节点
builder = StateGraph(State)
builder.add_node("subgraph_node", subgraph)
builder.add_edge(START, "subgraph_node")
builder.add_edge("subgraph_node", END)

# 编译主图并绘制结构图
graph = builder.compile()
# graph.get_graph().draw_png('./graph.png')

# 执行图并打印结果
print(graph.invoke({"messages": ["hello subgraph"]}))