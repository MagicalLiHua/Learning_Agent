import dotenv
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_redis import RedisConfig, RedisVectorStore, RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

# 读取env配置
dotenv.load_dotenv()


# ---------- 1. 定义网络请求的数据格式 ----------
# 告诉 FastAPI，前端发来的请求需要包含哪些字段
class ChatRequest(BaseModel):
    question: str
    session_id: str = "user_002"  # 默认值，允许前端传入不同的用户ID


class ChatResponse(BaseModel):
    answer: str


# ---------- 2. 工具和构建链 (保持原样) ----------

def format_docs(docs):
    return "\n\n".join(
        f"【文档片段{i + 1}】\n"
        f"Q: {doc.page_content}\n"
        f"A: {doc.metadata.get('answer', '')}"
        for i, doc in enumerate(docs)
    )


def extract_question(input_dict):
    return input_dict["question"]


def build_chain():
    # 注意：请确保这些 IP 和端口在运行 FastAPI 的机器上是可以访问的
    embedding = OllamaEmbeddings(base_url="http://10.160.108.2:11434", model="bge-m3")
    config = RedisConfig(index_name="faq", redis_url="redis://10.160.108.2:6379")
    vector_store = RedisVectorStore(embedding, config=config)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个外卖公司的智能客服，一定要礼貌热情。只回答外卖服务相关问题。"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "可用文档片段：\n{context}\n\n当前问题：{question}")
    ])

    llm = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b")
    parser = StrOutputParser()

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


def get_redis_history(session_id: str):
    return RedisChatMessageHistory(
        session_id=session_id,
        redis_url='redis://10.160.108.2:6379/0'
    )


# ---------- 3. 初始化 FastAPI 应用和 LangChain 实例 ----------

app = FastAPI(title="外卖智能客服 API", description="提供外卖客服问答服务")

# 在应用启动时就构建好模型链，避免每次请求都重新加载
chain = build_chain()
qa_runnable = RunnableWithMessageHistory(
    chain,
    get_session_history=get_redis_history,
    input_messages_key="question",
    history_messages_key="history"
)


# ---------- 4. 定义 API 接口 (取代原来的 while True) ----------

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    接收用户的提问，并返回大模型的回答。
    """
    # 配置 session_id 供历史记录使用
    session_config = {"configurable": {"session_id": request.session_id}}

    # 调用原有的 LangChain 逻辑
    answer = qa_runnable.invoke(
        {"question": request.question},
        config=session_config
    )

    # 返回打包好的 JSON 数据
    return ChatResponse(answer=answer)


# ---------- 5. 启动服务 ----------
if __name__ == "__main__":
    # 使用 uvicorn 启动应用
    print(">>> 正在启动外卖智能客服 API 服务... <<<")
    uvicorn.run(app, host="0.0.0.0", port=8000)