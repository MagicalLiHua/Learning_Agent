from RAGDemo.Embedding_test import embeddings


def naive_text_splitter(text: str, chunk_size: int):
    """极简版固定长度文本切分器 (利用生成器)"""
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]

def overlap_text_splitter(text: str, chunk_size: int, chunk_overlap: int):
    """
    带重叠的文本切分器
    请在这里补全你的代码（要求继续使用 yield）
    """
    for i in range(0, len(text), chunk_size-chunk_overlap):
        yield text[i: i + chunk_size]


import requests


def get_embedding(text: str, model_name: str = "nomic-embed-text") -> list[float]:
    """调用本地 Ollama 获取单个文本的向量"""
    url = "http://10.160.108.2:11434/api/embeddings"
    payload = {
        "model": model_name,
        "prompt": text
    }

    # 请在这里补充代码：
    # 1. 发送 POST 请求
    # 2. 解析返回的 JSON 数据
    # 3. 提取并返回 'embedding' 字段的值 (它应该是一个浮点数列表)
    response = requests.post(url, json=payload, timeout=30.0)
    response.raise_for_status()  # 确保请求成功，否则抛出异常
    result = response.json()
    if "embedding" not in result:
        raise ValueError(f"接口返回异常: {result}")
    return result["embedding"]


import numpy as np


def retrieve_top_k(query: str, chunk_texts: list[str], chunk_embeddings: list[list[float]], k: int = 2):
    """
    纯手工实现的向量数据库相似度检索
    """
    # 1. 将用户的 query 转化为 768 维向量 (调用你之前写好的 get_embedding)
    query_vec = get_embedding(query)

    # 2. 将数据转换为 numpy 数组方便计算
    query_np = np.array(query_vec)
    db_np = np.array(chunk_embeddings)

    # 3. 请在这里补全 NumPy 代码：
    # 计算 query_np 与 db_np 中每一个向量的余弦相似度
    similarities = np.dot(db_np, query_np) / (np.linalg.norm(db_np, axis=1) * np.linalg.norm(query_np) + 1e-10)  # 加上一个小常数避免除零

    # 4. 请在这里补全代码：
    # 找出相似度最高的 k 个索引，并返回对应的文本块和分数
    top_k_indices = np.argsort(similarities)[-k:][::-1]  # 获取相似度最高的 k 个索引
    top_k_chunks = [chunk_texts[i] for i in top_k_indices]
    top_k_scores = [similarities[i] for i in top_k_indices]
    return list(zip(top_k_chunks, top_k_scores))


def generate_rag_prompt(query: str, retrieved_chunks: list[tuple[str, float]]) -> str:
    """
    组装 RAG 的最终 Prompt
    """
    # 1. 从 retrieved_chunks 中提取纯文本内容，并将它们拼接成一个长字符串
    context_text = "\n".join([chunk for chunk, score in retrieved_chunks])

    # 2. 将 context_text 和 query 填入一个合理的 Prompt 模板中
    prompt = (f"请根据以下提供的上下文信息回答问题：\n\n上下文信息:\n{context_text}\n\n问题: {query}\n\n请给出详细的回答。"
              f"请仅根据以下提供的上下文信息回答问题。如果上下文中没有包含足以回答该问题的信息，请直接回答'我不知道'，绝不要盲目编造事实。")
    return prompt




# 准备一小段测试语料
corpus = (
    "在深度学习中，Transformer架构是革命性的。"
    "它完全抛弃了RNN和CNN，仅依赖自注意力机制来计算输入和输出的表示。"
    "它能够进行全局依赖建模，捕捉长距离的上下文关系，这使得它在自然语言处理任务中表现出色。"
    "Transformer架构的优势在于其高度的并行化能力和更好的长距离依赖建模能力。"
    "这种设计使得模型在训练时高度可并行化，极大地提升了效率。"
)

# 测试切分效果
chunks = list(overlap_text_splitter(corpus, chunk_size=15,chunk_overlap=5))
embeddings_list = [get_embedding(chunk) for chunk in chunks]

# 测试检索效果
query = "Transformer架构的优势是什么？"
top_k_results = retrieve_top_k(query, chunks, embeddings_list, k=5)
print("检索结果：")
for idx, (chunk, score) in enumerate(top_k_results):
    print(f"Top {idx+1}: '{chunk}' (相似度: {score:.4f})")

# 测试 RAG Prompt 生成
rag_prompt = generate_rag_prompt(query, top_k_results)
print("\n生成的 RAG Prompt：")
print(rag_prompt)

# 调用 Ollama 生成回答
# 修改 URL 为完整路径
url = "http://10.160.108.2:11434/v1/completions"
payload = {
    "model": "qwen3-vl:8b",
    "prompt": rag_prompt
}

response = requests.post(url, json=payload, timeout=30.0)
response.raise_for_status()

# 兼容接口返回的结构较深，通常在 choices[0].text 中
result = response.json()
answer = result.get("choices", [{}])[0].get("text", "")
print("\n生成的回答：")
print(answer)