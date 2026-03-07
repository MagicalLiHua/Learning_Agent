import os
import json
import uuid
import numpy as np
import redis
from openai import OpenAI
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.index_definition import IndexDefinition
from redis.commands.search.query import Query

# ========== 1. 基础配置 (保留你的生产环境) ==========
OLLAMA_BASE_URL = "http://10.160.108.2:11434/v1"
EMBED_MODEL = "bge-m3"  # 向量模型
LLM_MODEL = "qwen3-vl:8b"  # 对话模型
INDEX_NAME = "faq_index_v1"
VECTOR_DIM = 1024  # bge-m3 维度
DISTANCE_METRIC = "COSINE"
TOP_K = 3  # 相似度搜索返回的数量

# 初始化客户端
client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
redis_client = redis.Redis(host="10.160.108.2", port=6379, decode_responses=False)


# ========== 2. 索引与导入 (保留你的本地逻辑) ==========
def create_index():
    try:
        redis_client.ft(INDEX_NAME).info()
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


def import_from_json(file_path):
    """如果需要重新导入数据，保留此函数"""
    if not os.path.exists(file_path): return
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        question = item.get("question", "")
        answer = item.get("answer", "")
        text_to_embed = f"{question} {answer}".strip()
        if not text_to_embed: continue

        resp = client.embeddings.create(model=EMBED_MODEL, input=text_to_embed)
        vector = np.array(resp.data[0].embedding, dtype=np.float32).tobytes()

        doc_id = f"faq:{uuid.uuid4().hex}"
        redis_client.hset(doc_id, mapping={
            "question": question,
            "answer": answer,
            "source": item.get("metadata", {}).get("source", ""),
            "category": item.get("metadata", {}).get("category", ""),
            "embedding": vector
        })


# ========== 3. 将问题转为向量 (适配教程模块化) ==========
def embed_question(question: str):
    """使用 Ollama 的嵌入模型将文本转为向量字节流"""
    resp = client.embeddings.create(model=EMBED_MODEL, input=question)
    embedding = resp.data[0].embedding
    return np.array(embedding, dtype=np.float32).tobytes()


# ========== 4. 相似度搜索 (适配教程逻辑) ==========
def search_faq(question: str, top_k=TOP_K):
    """在 Redis 中进行向量相似度检索"""
    q_vector = embed_question(question)

    # 构造查询语句，增加从 Hash 中提取字段的范围
    query = (
        Query(f"*=>[KNN {top_k} @embedding $vec AS score]")
        .sort_by("score")
        .return_fields("question", "answer", "source", "category", "score")
        .dialect(2)
    )

    results = redis_client.ft(INDEX_NAME).search(query, query_params={"vec": q_vector})
    return results.docs


# ========== 5. 构建 Prompt (严格遵循教程模版) ==========
def build_prompt(user_question: str, retrieved_docs, top_k=TOP_K) -> str:
    """根据教程要求，构建严格的 Prompt 模版"""
    context_parts = []
    for i, doc in enumerate(retrieved_docs[:top_k], start=1):
        # 注意：从 Redis 返回的 bytes 需要 decode 为字符串
        q = doc.question.decode('utf-8') if isinstance(doc.question, bytes) else doc.question
        a = doc.answer.decode('utf-8') if isinstance(doc.answer, bytes) else doc.answer
        context_parts.append(f"【文档片段{i}】\nQ: {q}\nA: {a}")

    context_text = "\n\n".join(context_parts)

    prompt = f"""
你是一个智能问答助手，请仅根据提供的文档片段回答用户问题。
如果文档片段中没有相关内容，请回答“未找到相关信息”。

用户问题：
{user_question}

可用文档片段：
{context_text}

请基于以上信息，生成简洁明了的回答：
"""
    return prompt.strip()


# ========== 6. 主循环 (适配教程执行流程) ==========
if __name__ == "__main__":
    create_index()
    # 如果是第一次运行，取消下面这一行的注释来导入数据
    import_from_json("faq_processed.json")

    print("\n" + "=" * 30)
    print("🤖 本地 RAG 系统 (4090 + Ollama) 已就绪")
    print("=" * 30)

    while True:
        user_question = input("\n请输入问题（输入 exit 退出）：")
        if user_question.lower() in ["exit", "quit", "q"]:
            break

        # 1. 检索
        docs = search_faq(user_question, top_k=TOP_K)
        if not docs:
            print("⚠️ 未检索到相关文档")
            continue

        # 2. 构建 Prompt
        prompt = build_prompt(user_question, docs)

        # 调试用：查看生成的 Prompt
        # print("\n--- DEBUG: PROMPT ---")
        # print(prompt)
        # print("---------------------\n")

        # 3. 调用本地大模型生成回答
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        print(f"\n🤖 AI: {response.choices[0].message.content}")