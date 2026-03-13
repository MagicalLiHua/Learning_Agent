import uuid
from typing import TypedDict, Annotated
import dotenv
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.redis import RedisSaver
from langgraph.constants import END, START
from langgraph.graph import StateGraph, MessagesState, add_messages
from langgraph.store.base import BaseStore
from langgraph.store.redis import RedisStore

# 加载环境变量配置
dotenv.load_dotenv()
# 初始化本地大语言模型，配置模型名称和推理模式
model = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b", reasoning=False)


class State(TypedDict):
    """
    定义图中状态的数据结构。

    属性:
        messages (Annotated[list, add_messages]): 使用 add_messages 合并的消息列表。
    """
    messages: Annotated[list, add_messages]


def save_memory(store: BaseStore, user_id: str, content: str):
    """
    将用户输入的内容保存为记忆。

    参数:
        store (BaseStore): 存储系统的实例，用于持久化数据。
        user_id (str): 用户唯一标识符。
        content (str): 需要存储的文本内容。
    """
    namespace = ("memories", user_id)
    store.put(namespace, str(uuid.uuid4()), {"data": content})


def recall_memories(store: BaseStore, user_id: str, query: str, limit: int = 5):
    """
    根据查询语句检索与用户相关的记忆。

    参数:
        store (BaseStore): 存储系统的实例。
        user_id (str): 用户唯一标识符。
        query (str): 查询关键词或句子。
        limit (int, optional): 返回的记忆条数上限，默认是 5 条。

    返回:
        list[str]: 匹配的记忆内容列表。
    """
    namespace = ("memories", user_id)
    memories = store.search(namespace, query=query, limit=limit)
    return [m.value["data"] for m in memories]


def chatbot(state: MessagesState, config: RunnableConfig, *, store: BaseStore):
    """
    聊天机器人主逻辑节点函数。

    参数:
        state (MessagesState): 当前对话的状态信息，包括历史消息等。
        config (RunnableConfig): 运行时配置信息，如线程ID、用户ID等。
        store (BaseStore): 用于读取和写入用户记忆的存储接口。

    返回:
        dict: 更新后的消息状态字典。
    """
    user_id = config["configurable"]["user_id"]

    # 检索历史记忆
    query = state["messages"][-1].content
    related_memories = recall_memories(store, user_id, query)

    # 构造系统提示
    system_msg = (
        "你是一个友好的聊天助手。\n"
        f"以下是关于用户的记忆:\n{chr(10).join(related_memories) if related_memories else '暂无'}"
    )

    # 保存当前消息到记忆
    save_memory(store, user_id, query)

    # 调用模型生成回复
    response = model.invoke(
        [{"role": "system", "content": system_msg}] + state["messages"]
    )
    return {"messages": response}


# 创建状态图并定义流程
builder = StateGraph(State)
builder.add_node(chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# 1. 定义 Redis 的 URI 连接字符串
REDIS_URI = "redis://10.160.108.2:6379"

# 2. 官方推荐写法：使用 .from_conn_string() 和 with 语句安全管理连接
with RedisSaver.from_conn_string(REDIS_URI) as checkpointer, \
        RedisStore.from_conn_string(REDIS_URI) as store:
    # 3. 首次使用必须调用 setup()，以便在 Redis 中建立 RediSearch 的索引结构
    checkpointer.setup()
    store.setup()

    # 4. 编译构建最终可运行的图对象
    graph = builder.compile(
        checkpointer=checkpointer,
        store=store,
    )

    # 第一次交互测试：记录用户基本信息
    config1 = {"configurable": {"thread_id": "1", "user_id": "1"}}
    msg1 = graph.invoke({"messages": [{"role": "user", "content": "我叫崔亮，喜欢学习。"}]}, config1)
    print("第一次回复：")
    msg1["messages"][-1].pretty_print()

    # 第二次交互测试：验证是否能回忆起之前的信息
    config2 = {"configurable": {"thread_id": "2", "user_id": "1"}}
    msg2 = graph.invoke({"messages": [{"role": "user", "content": "我叫什么？我喜欢做什么？"}]}, config2)
    print("第二次回复：")
    msg2["messages"][-1].pretty_print()

# ================= 修复部分结束 =================