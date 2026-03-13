import dotenv
from langchain_core.messages.utils import trim_messages, count_tokens_approximately
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

# 加载环境变量配置
dotenv.load_dotenv()
# 初始化本地大语言模型，配置模型名称和推理模式
model = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b", reasoning=False)
# 定义工具列表，
tools = []


def pre_model_hook(state):
    """
    在模型处理前对消息进行预处理的钩子函数

    该函数用于裁剪消息历史，只保留最近的若干条消息，避免上下文过长

    Args:
        state (dict): 包含对话状态的字典，其中"messages"键对应消息列表

    Returns:
        dict: 包含裁剪后消息的字典，键为"llm_input_messages"
    """
    # 参数说明:
    #   state["messages"]: 需要裁剪的消息列表
    #   strategy: 裁剪策略，"last"表示从最后开始裁剪
    #   token_counter: 用于计算token数量的函数，这里使用近似计算方法
    #   max_tokens: 最大token数量限制，设置为300
    #   start_on: 开始裁剪的消息类型，"human"表示从人类用户的消息开始
    #   end_on: 结束裁剪的消息类型，可以是"human"或"tool"类型的消息
    # 返回值: 裁剪后的消息列表
    trimmed_messages = trim_messages(
        state["messages"],
        strategy="last",
        token_counter=count_tokens_approximately,
        max_tokens=300,
        start_on="human",
        end_on=("human", "tool"),
    )

    return {"llm_input_messages": trimmed_messages}


checkpointer = InMemorySaver()
agent = create_react_agent(
    model,
    tools,
    pre_model_hook=pre_model_hook,
    checkpointer=checkpointer,
)
config = {"configurable": {"thread_id": "user-001"}}
msg1 = agent.invoke({"messages": [("user", "你好，我叫崔亮")]}, config)
msg1["messages"][-1].pretty_print()
like_list = ['唱', '跳', 'rap', '篮球']
for i in like_list:
    msg = "我喜欢做的事是：" + i
    print(msg)
    agent.invoke({"messages": [("user", msg)]}, config)
msg2 = agent.invoke({"messages": [("user", "我叫什么？我喜欢做的事是什么？")]}, config)
msg2["messages"][-1].pretty_print()