from sentence_transformers import SentenceTransformer, util

# 1. 加载一个支持中文的预训练模型
# 'paraphrase-multilingual-MiniLM-L12-v2' 是一个性价比极高的多语言模型
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 2. 定义你的句子
texts = [
    '我喜欢吃菠萝',          # 句子 0
    '菠萝是我最喜欢吃的水果',   # 句子 1
    '我喜欢用菠萝手机'        # 句子 2
]

# 3. 将句子转换为向量 (Encoding)
# 这一步就是你说的“浓缩”过程，每个句子会变成一个 384 维的向量
embeddings = model.encode(texts)

print("--- 语义相似度计算结果 ---")

# 4. 计算并打印两两之间的相似度
# 我们计算 句子0 分别与 句子1、句子2 的相似度
sim_0_1 = util.cos_sim(embeddings[0], embeddings[1])
sim_0_2 = util.cos_sim(embeddings[0], embeddings[2])
sim_1_2 = util.cos_sim(embeddings[1], embeddings[2])

print(f"句子 [0] vs [1]: {sim_0_1.item():.4f}  (喜欢吃菠萝 vs 菠萝是水果)")
print(f"句子 [0] vs [2]: {sim_0_2.item():.4f}  (喜欢吃菠萝 vs 菠萝手机)")
print(f"句子 [1] vs [2]: {sim_1_2.item():.4f}  (菠萝是水果 vs 菠萝手机)")