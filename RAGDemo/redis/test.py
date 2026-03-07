import os
import dotenv
import dashscope
import redis
import numpy as np
from http import HTTPStatus
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.index_definition import IndexDefinition
from redis.commands.search.query import Query

# ========== 配置 ==========
# 加载 .env 文件中的环境变量
dotenv.load_dotenv()
# 设置通义千问 API Key
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# 定义 Redis 向量索引名称
INDEX_NAME = "embedding_index"
# 设置向量维度，需与所使用的 embedding 模型输出维度一致
VECTOR_DIM = 1024
# 设置向量相似度计算方式为余弦距离
DISTANCE_METRIC = "COSINE"

# ========== 连接 Redis ==========
# 初始化 Redis 客户端连接
# 注意：为了正确存储二进制向量数据，关闭了响应解码功能
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    password=None,
    decode_responses=False  # 存向量要关掉 decode
)


# ========== 创建索引（只执行一次） ==========
def create_index():
    """
    创建 Redis 向量搜索索引。

    如果索引已存在则跳过创建，否则根据预定义的字段结构创建新索引。
    索引包括文本字段和向量字段，使用 HNSW 算法进行向量近似最近邻搜索。
    """
    try:
        # 尝试获取索引信息以判断是否已存在
        redis_client.ft(INDEX_NAME).info()
        print("✅ 索引已存在")
    except Exception:  # 统一捕获异常
        # 创建新的向量索引
        redis_client.ft(INDEX_NAME).create_index(
            [
                TextField("text"),  # 文本字段用于存储原始文本
                VectorField(
                    "embedding",  # 向量字段名
                    "HNSW",  # 使用 HNSW 算法
                    {"TYPE": "FLOAT32", "DIM": VECTOR_DIM, "DISTANCE_METRIC": DISTANCE_METRIC}
                )
            ],
            definition=IndexDefinition(prefix=["doc:"])  # 建议加上前缀
        )
        print("✅ 已创建向量索引")


# ========== 写入一条数据 ==========
def insert_text(text: str):
    """
    调用通义千问 embedding 接口并将文本及其向量表示写入 Redis。

    参数:
        text (str): 需要转换为向量并存储的原始文本内容。
    """
    # 调用多模态 embedding 接口获取文本向量
    resp = dashscope.MultiModalEmbedding.call(
        model="multimodal-embedding-v1",
        input=[{"text": text}]
    )

    if resp.status_code == HTTPStatus.OK:
        # 提取 embedding 向量并转换为字节格式
        embedding = resp.output["embeddings"][0]["embedding"]
        vector = np.array(embedding, dtype=np.float32).tobytes()
        # 构造 Redis 键名
        key = f"doc:{resp.request_id}"
        # 将文本和向量写入 Redis Hash 结构中
        redis_client.hset(key, mapping={
            "text": text,
            "embedding": vector
        })
        print(f"✅ 已写入 Redis，key={key}, 向量维度={len(embedding)}")
    else:
        print(f"❌ 调用失败: {resp.code}, {resp.message}")


# ========== 相似度搜索 ==========
def search_similar(query_text: str, topk: int = 1):
    """
    根据输入文本查询与其最相似的文本列表。

    参数:
        query_text (str): 查询用的文本内容。
        topk (int): 返回最相似结果的数量，默认为 1。
    """
    # 获取查询文本的 embedding 向量
    resp = dashscope.MultiModalEmbedding.call(
        model="multimodal-embedding-v1",
        input=[{"text": query_text}]
    )

    if resp.status_code != HTTPStatus.OK:
        print(f"❌ 查询 embedding 失败: {resp.code}, {resp.message}")
        return

    # 将查询向量转换为字节格式
    query_vector = np.array(
        resp.output["embeddings"][0]["embedding"], dtype=np.float32
    ).tobytes()

    # 构造 KNN 查询语句
    knn_query = f'*=>[KNN {topk} @embedding $vec_param]'
    q = Query(knn_query).sort_by("__embedding_score").paging(0, topk)

    # 执行向量相似性搜索
    search_result = redis_client.ft(INDEX_NAME).search(
        q, query_params={"vec_param": query_vector}
    )

    print(f"🔍 与 '{query_text}' 最相似的 {topk} 条：")
    # 输出匹配结果
    for i, doc in enumerate(search_result.docs, 1):
        print(f"{i}. {doc.text}")


# ========== 使用示例 ==========
if __name__ == "__main__":
    # 创建索引
    create_index()
    # 插入示例数据
    insert_text("我喜欢吃苹果")
    insert_text("苹果是我最喜欢吃的水果")
    insert_text("我喜欢用苹果手机")
    # 相似度搜索
    search_similar("我喜欢用小米")
