import os
import json
import uuid
import numpy as np
import redis
from openai import OpenAI
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.index_definition import IndexDefinition
from redis.commands.search.query import Query

# ========== 1. 基础配置 ==========
OLLAMA_BASE_URL = "http://10.160.108.2:11434/v1"
EMBED_MODEL = "bge-m3"  # 向量模型
LLM_MODEL = "qwen3-vl:8b"  # 对话模型
INDEX_NAME = "faq_index_v1"
VECTOR_DIM = 1024  # bge-m3 维度
DISTANCE_METRIC = "COSINE"

# 初始化客户端
client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
redis_client = redis.Redis(host="10.160.108.2", port=6379, decode_responses=False)


# ========== 2. 索引创建 ==========
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


# ========== 3. 导入逻辑 ==========
def import_from_json(file_path):
    """读取 JSON 并批量存入 Redis"""
    if not os.path.exists(file_path):
        print(f"❌ 找不到文件: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"🚀 开始导入 {len(data)} 条数据...")

    success_count = 0
    for item in data:
        question = item.get("question", "")
        answer = item.get("answer", "")
        # 如果 answer 为空，只对 question 进行向量化
        text_to_embed = f"{question} {answer}".strip()

        if not text_to_embed:
            continue

        try:
            # 1. 调用 Ollama 获取向量
            resp = client.embeddings.create(model=EMBED_MODEL, input=text_to_embed)
            embedding = resp.data[0].embedding
            vector = np.array(embedding, dtype=np.float32).tobytes()

            # 2. 准备存入 Redis 的数据
            metadata = item.get("metadata", {})
            doc_id = f"faq:{uuid.uuid4().hex}"

            redis_client.hset(doc_id, mapping={
                "question": question,
                "answer": answer,
                "source": metadata.get("source", ""),
                "category": metadata.get("category", ""),
                "embedding": vector
            })
            success_count += 1
            if success_count % 10 == 0:
                print(f"已处理 {success_count} 条...")

        except Exception as e:
            print(f"❌ 处理失败 [{question[:10]}...]: {e}")

    print(f"🎊 导入完成！成功: {success_count} 条。")


# ========== 4. RAG 查询逻辑 ==========
def local_rag_query(user_query: str):
    # 1. 向量化用户问题
    q_resp = client.embeddings.create(model=EMBED_MODEL, input=user_query)
    q_vector = np.array(q_resp.data[0].embedding, dtype=np.float32).tobytes()

    # 2. Redis 检索 (Top 3)
    search_query = (
        Query(f"*=>[KNN 3 @embedding $vec as score]")
        .sort_by("score")
        .return_fields("question", "answer", "score")
        .dialect(2)
    )
    results = redis_client.ft(INDEX_NAME).search(search_query, {"vec": q_vector})

    # 3. 构造 Prompt
    context = ""
    for doc in results.docs:
        # 过滤掉没有答案的参考资料
        if doc.answer:
            context += f"相关问答：\n问：{doc.question}\n答：{doc.answer}\n\n"

    if not context:
        prompt = user_query
    else:
        prompt = f"请根据以下参考资料回答问题：\n\n{context}\n问题：{user_query}"

    # 4. 生成回答
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ========== 5. 执行阶段 ==========
if __name__ == "__main__":
    # 步骤 1: 创建索引
    create_index()

    # 步骤 2: 导入数据 (填入你的文件名)
    # 假设你的文件名叫 my_data.json
    import_from_json("faq_processed.json")

    # 步骤 3: 进入对话循环
    print("\n" + "=" * 30)
    print("🤖 本地 RAG 系统启动成功 (使用 4090 + Ollama)")
    print("=" * 30)

    while True:
        user_input = input("\n👤 用户: ")
        if user_input.lower() in ['q', 'quit', 'exit']:
            break

        print("🔍 正在查询本地库并思考...")
        reply = local_rag_query(user_input)
        print(f"🤖 AI: {reply}")