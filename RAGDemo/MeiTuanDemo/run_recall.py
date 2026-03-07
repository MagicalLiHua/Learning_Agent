import os
import json
import uuid
import numpy as np
import redis
from openai import OpenAI
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.index_definition import IndexDefinition
from redis.commands.search.query import Query

# ========== 1. 基础配置 (保持你的生产环境) ==========
OLLAMA_BASE_URL = "http://10.160.108.2:11434/v1"
EMBED_MODEL = "bge-m3"  # 向量模型
LLM_MODEL = "qwen3-vl:8b"  # 对话模型
INDEX_NAME = "faq_index_v1"
VECTOR_DIM = 1024  # bge-m3 维度
DISTANCE_METRIC = "COSINE"

# 初始化客户端
client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
redis_client = redis.Redis(host="10.160.108.2", port=6379, decode_responses=False)


# ========== 2. 索引创建 (保持不变) ==========
def create_index():
    try:
        redis_client.ft(INDEX_NAME).info()
        print("✅ 索引已存在。")
    except Exception:
        schema = (
            TextField("question"),
            TextField("answer"),
            TextField("source"),
            TextField("category"),
            VectorField(
                "embedding",
                "HNSW",
                {"TYPE": "FLOAT32", "DIM": VECTOR_DIM, "DISTANCE_METRIC": DISTANCE_METRIC}
            )
        )
        redis_client.ft(INDEX_NAME).create_index(
            schema,
            definition=IndexDefinition(prefix=["faq:"])
        )
        print("✅ 成功创建 Redis 向量索引。")


# ========== 3. 相似度搜索 (核心修改点：模仿教程逻辑) ==========
def search_faq(question: str, top_k=3):
    """
    根据用户输入的问题，在 Redis 中进行向量相似度搜索，并直接打印结果。
    这里使用的是你的 Ollama bge-m3 模型
    """
    # 1. 向量化用户问题 (使用你的 Ollama 客户端)
    q_resp = client.embeddings.create(model=EMBED_MODEL, input=question)
    q_vector = np.array(q_resp.data[0].embedding, dtype=np.float32).tobytes()

    # 2. 构造 RediSearch 查询 (增加返回字段以匹配你的数据结构)
    query = (
        Query(f"*=>[KNN {top_k} @embedding $vec AS score]")
        .sort_by("score")
        .return_fields("question", "answer", "source", "category", "score")
        .dialect(2)
    )

    # 3. 执行查询
    results = redis_client.ft(INDEX_NAME).search(query, query_params={"vec": q_vector})

    print(f"\n🔎 检索问题: {question}")
    print(f"📊 命中 {len(results.docs)} 条相关 FAQ\n")

    # 4. 打印每条结果 (模仿教程的格式化输出)
    for i, doc in enumerate(results.docs, start=1):
        # 注意：Redis 返回的字段可能是 bytes，取决于连接配置，这里做简单处理
        # 如果你 decode_responses=False，需要使用 getattr 或 ['field']
        print(f"--- Top {i} ---")
        print(f"相似度分数: {doc.score}")
        print(f"Q: {getattr(doc, 'question', 'N/A')}")
        print(f"A: {getattr(doc, 'answer', 'N/A')}")
        print(f"来源: {getattr(doc, 'source', 'N/A')}")
        print(f"类别: {getattr(doc, 'category', 'N/A')}")
        print()


# ========== 4. 原有的 RAG 查询逻辑 (保留供对比) ==========
def local_rag_query(user_query: str):
    """这是你之前写的逻辑，会将结果喂给大模型"""
    q_resp = client.embeddings.create(model=EMBED_MODEL, input=user_query)
    q_vector = np.array(q_resp.data[0].embedding, dtype=np.float32).tobytes()

    search_query = (
        Query(f"*=>[KNN 3 @embedding $vec as score]")
        .sort_by("score")
        .return_fields("question", "answer", "score")
        .dialect(2)
    )
    results = redis_client.ft(INDEX_NAME).search(search_query, {"vec": q_vector})

    context = ""
    for doc in results.docs:
        if hasattr(doc, 'answer'):
            context += f"相关问答：\n问：{doc.question}\n答：{doc.answer}\n\n"

    prompt = f"请根据以下参考资料回答问题：\n\n{context}\n问题：{user_query}" if context else user_query

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ========== 5. 执行阶段 ==========
if __name__ == "__main__":
    # 确保索引存在
    create_index()

    # 如果你已经导入过数据，下面这一行可以注释掉
    # import_from_json("faq_processed.json")

    print("\n" + "=" * 30)
    print("🚀 生产环境：Redis 向量搜索模式")
    print("=" * 30)

    while True:
        user_input = input("\n👤 输入问题 (输入 q 退出): ")
        if user_input.lower() in ['q', 'quit', 'exit']:
            break

        # --- 这里改为调用我们新写的 search_faq ---
        search_faq(user_input, top_k=3)

        # 如果你还想看大模型的回答，可以取消下面这一行的注释
        # print(f"🤖 AI 回答: {local_rag_query(user_input)}")