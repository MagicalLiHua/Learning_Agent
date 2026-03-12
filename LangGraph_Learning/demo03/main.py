from typing import TypedDict, Annotated,Literal
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph
from langgraph.types import interrupt, Command


# 定义 Agent 的状态结构，包含消息列表
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# 初始化本地大语言模型，配置模型名称和推理模式
llm = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b", reasoning=False)


# 聊天机器人函数，用于处理对话状态并生成回复
def chatbot(state: AgentState):
    return {"messages": [llm.invoke(state['messages'])]}

def human_approval(state: AgentState) -> Command[Literal["chatbot", END]]:
    question = "是否同意调用大语言模型？(y/n): "
    while True:
        response = input(question).strip().lower()
        if response in ("y", "yes"):
            return Command(goto="chatbot")
        elif response in ("n", "no"):
            print("❌ 已拒绝，流程结束。")
            return Command(goto=END)
        else:
            print("⚠️ 请输入 y 或 n。")

# 构建状态图结构
graph_builder = StateGraph(AgentState)

# 每个节点都与对应的处理函数进行绑定，构成工作流的基本单元
graph_builder.add_node("human_approval", human_approval)
graph_builder.add_node("chatbot", chatbot)

# 添加边：从 START 到 chatbot，然后到 END
graph_builder.add_edge(START, "human_approval")

checkpointer=InMemorySaver()
# 编译图结构，并绘制可视化图表
graph = graph_builder.compile(checkpointer=checkpointer)
# graph.get_graph().draw_png('./graph.png')
config = {"configurable": {"thread_id": "chat-1"}}
response1 = graph.invoke({"messages": ["北京天气怎么样"]},config)
print(response1["messages"][-1].content)
# 确认执行
final_result = graph.invoke(Command(resume=True),config)
print(final_result["messages"][-1].content)
# 取消执行
# final_result = graph.invoke(Command(resume=False),config)
# print(final_result["messages"][-1].content)