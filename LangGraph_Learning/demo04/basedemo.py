from typing import TypedDict, Annotated
from langchain_ollama import ChatOllama
from langgraph.constants import START, END
from langgraph.graph import add_messages, StateGraph


# 定义 Agent 的状态结构，包含消息列表
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# 初始化本地大语言模型，配置模型名称和推理模式
llm = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b", reasoning=False)


# 聊天机器人函数，用于处理对话状态并生成回复
def chatbot(state: AgentState):
    return {"messages": [llm.invoke(state['messages'])]}


# 构建状态图结构
graph_builder = StateGraph(AgentState)

# 每个节点都与对应的处理函数进行绑定，构成工作流的基本单元
graph_builder.add_node("chatbot", chatbot)

# 添加边：从 START 到 chatbot，然后到 END
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot",END)


# 编译图结构，并绘制可视化图表
graph = graph_builder.compile()
# graph.get_graph().draw_png('./graph.png')

response1 = graph.invoke({"messages": ["北京天气怎么样"]})

print(response1["messages"][-1].content)