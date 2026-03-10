from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_ollama import ChatOllama
from loguru import logger

# Redis 配置
REDIS_URL = "redis://10.160.108.2:6379/0"

# 初始化模型
llm = ChatOllama(base_url="http://10.160.108.2:11434",model="qwen3-vl:8b")

# 创建提示模板
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder("history"),
    ("human", "{question}")
])

# 保留的历史轮数
k = 2


def get_session_history(session_id: str) -> RedisChatMessageHistory:
    """获取或创建会话历史（使用 Redis）"""
    # 创建 Redis 历史对象
    history = RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL,
        ttl=3600  # 1小时过期
    )

    # 自动修剪：只保留最近 k 轮对话（2k 条消息）
    if len(history.messages) > k * 2:
        # 保留最近的消息
        messages_to_keep = history.messages[-k * 2:]
        history.clear()
        history.add_messages(messages_to_keep)

    return history


# 创建带历史的链
chain = RunnableWithMessageHistory(
    prompt | llm,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

# 配置
config = RunnableConfig(configurable={"session_id": "demo"})

# 主循环
print("开始对话（输入 'quit' 退出）")
while True:
    question = input("\n输入问题：")
    if question.lower() in ['quit', 'exit', 'q']:
        break

    response = chain.invoke({"question": question}, config)
    logger.info(f"AI回答:{response.content}")

    # 可选：显示当前历史消息数
    history = get_session_history("demo")
    logger.info(f"[当前历史消息数: {len(history.messages)}]")