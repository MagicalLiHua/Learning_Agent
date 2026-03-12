from typing import TypedDict, Annotated, Literal
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langgraph.types import interrupt, Command


# 1. 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# 2. 初始化大模型 (请确保你的 Ollama 正在运行)
llm = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b", reasoning=False)


# 3. 审批节点 (核心改动在这里 💡)
def human_approval(state: AgentState) -> Command[Literal["chatbot", END]]:
    print("⏳ [节点: human_approval] 运行中，准备触发中断...")

    # 【神仙魔法】：interrupt() 会立刻冻结当前图的运行，并把状态存入 checkpointer！
    # 圆括号里的字符串 "需要人工审批..." 会作为挂起信息，暴露给外部程序。
    # 当图被唤醒时，human_response 会接收到外部传进来的 resume 数据。
    human_response = interrupt("需要人工审批：是否同意调用大模型？")

    # 往下走说明图已经被唤醒了！
    print(f"✅ [节点: human_approval] 图已被唤醒！收到外部传来的决定: {human_response}")

    if human_response.lower() in ("y", "yes"):
        print("➡️  [路由] 审批通过，走向 chatbot 节点...\n")
        return Command(goto="chatbot")
    else:
        print("🛑  [路由] 审批拒绝，走向 END 结束流程...\n")
        return Command(goto=END)


# 4. 大模型节点
def chatbot(state: AgentState):
    print("🤖 [节点: chatbot] 大模型开始思考...")
    response = llm.invoke(state['messages'])
    return {"messages": [response]}


# 5. 构建与编译图
builder = StateGraph(AgentState)
builder.add_node("human_approval", human_approval)
builder.add_node("chatbot", chatbot)

builder.add_edge(START, "human_approval")
builder.add_edge("chatbot", END)

# 必须要有存档器，图才能记住挂起时的状态
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# ==========================================
# ⬇️ 下面是模拟外部系统 (比如你的前端界面或主程序) ⬇️
# ==========================================
if __name__ == "__main__":
    # 指定一个存档槽位
    config = {"configurable": {"thread_id": "chat-1"}}

    print("\n" + "=" * 50)
    print("第一阶段：启动图并触发挂起")
    print("=" * 50)
    # 给图传入初始消息，图开始运行...
    # 注意：它运行到 human_approval 节点里的 interrupt() 时就会停下，并返回当前的快照。
    initial_input = {"messages": ["请问北京天气怎么样？"]}
    graph.invoke(initial_input, config)

    # 我们可以在外部偷看一下图现在的状态
    state_snapshot = graph.get_state(config)
    print(f"\n⏸️ 此时图的状态：正在等待 (next node: {state_snapshot.next})")
    print(f"📝 节点抛出的挂起信息: {state_snapshot.tasks[0].interrupts[0].value}")

    print("\n" + "=" * 50)
    print("第二阶段：人类去喝了杯咖啡，回来进行审批")
    print("=" * 50)

    # 注意：这个 input() 是写在图的外部的！模拟的是用户在网页上点击了“同意”按钮。
    user_decision = input(">> [模拟前端界面] 请输入审批意见 (y/n): ").strip()

    print("\n" + "=" * 50)
    print("第三阶段：恢复图的运行 (Resume)")
    print("=" * 50)

    # 关键代码：通过 Command(resume=...) 唤醒图，把用户的决定塞进刚才 interrupt() 挂起的地方。
    final_result = graph.invoke(Command(resume=user_decision), config)

    # 打印最终结果
    if "messages" in final_result and len(final_result["messages"]) > 1:
        print(f"\n🎉 最终回复内容:\n{final_result['messages'][-1].content}")
    else:
        print("\n🚫 流程已提前结束，未生成大模型回复。")