import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_redis import RedisConfig, RedisVectorStore, RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # 引入消息占位符
from langchain_core.runnables import RunnableWithMessageHistory

# 读取env配置
dotenv.load_dotenv()
# ---------- 工具 ----------

def format_docs(docs):
    return "\n\n".join(
        f"【文档片段{i + 1}】\n"
        f"Q: {doc.page_content}\n"
        f"A: {doc.metadata.get('answer', '')}"
        for i, doc in enumerate(docs)
    )


def extract_question(input_dict):
    """
    修改提取逻辑：RunnableWithMessageHistory 会传入一个字典
    """
    return input_dict["question"]


# ---------- 构建链 ----------

def build_chain():
    embedding = OllamaEmbeddings(base_url="http://10.160.108.2:11434", model="bge-m3")
    config = RedisConfig(index_name="faq", redis_url="redis://10.160.108.2:6379")
    vector_store = RedisVectorStore(embedding, config=config)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    # 【关键修改 1】：使用 ChatPromptTemplate 并添加 MessagesPlaceholder
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个外卖公司的智能客服，一定要礼貌热情。只回答外卖服务相关问题。"),
        MessagesPlaceholder(variable_name="history"),  # 历史记录将注入到这里
        ("human", "可用文档片段：\n{context}\n\n当前问题：{question}")
    ])

    llm = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b")
    parser = StrOutputParser()

    # 【关键修改 2】：重构 Chain 的逻辑
    # 注意：这里的输入现在是一个包含 question 和 history 的字典
    chain = (
            {
                "context": lambda x: format_docs(retriever.invoke(x["question"])),
                "question": lambda x: x["question"],
                "history": lambda x: x["history"]
            }
            | prompt
            | llm
            | parser
    )
    return chain


# ---------- 交互 ----------

def main():
    chain = build_chain()

    # 【关键修改 3】：定义一个函数来根据 session_id 获取历史记录
    def get_redis_history(session_id):
        return RedisChatMessageHistory(
            session_id=session_id,
            redis_url='redis://10.160.108.2:6379/0'
        )

    # 【关键修改 4】：完整配置 RunnableWithMessageHistory
    runnable = RunnableWithMessageHistory(
        chain,
        get_session_history=get_redis_history,
        input_messages_key="question",  # 对应输入字典里的问题字段
        history_messages_key="history"  # 对应 Prompt 里 Placeholder 的变量名
    )

    print(">>> 欢迎使用外卖智能客服系统，输入 quit 退出 <<<")

    # 固定的 session_id（实际应用中可以是每个用户的 ID）
    session_config = {"configurable": {"session_id": "user_001"}}

    while True:
        try:
            user_input = input("\n您：").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if user_input.lower() in {"quit", "exit", "q"}:
            break

        answer = runnable.invoke(
            {"question": user_input},
            config=session_config
        )
        print("客服：", answer)


if __name__ == "__main__":
    main()