太棒了！我们直接使用目前业界最流行的 **`sentence-transformers`** 库。它封装了复杂的 Transformer 计算，让你可以像调用函数一样轻松地把句子变成向量并计算相似度。

### 第一步：安装必要的库

在你的终端（Terminal）里运行：

```bash
pip install -U sentence-transformers

```

### 第二步：编写 Python 代码

这段代码会下载一个支持中文的小型预训练模型，并将你的三个句子进行两两比对。

```python
from sentence_transformers import SentenceTransformer, util

# 1. 加载一个支持中文的预训练模型
# 'paraphrase-multilingual-MiniLM-L12-v2' 是一个性价比极高的多语言模型
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 2. 定义你的句子
texts = [
    '我喜欢吃苹果',          # 句子 0
    '苹果是我最喜欢吃的水果',   # 句子 1
    '我喜欢用苹果手机'        # 句子 2
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

print(f"句子 [0] vs [1]: {sim_0_1.item():.4f}  (喜欢吃苹果 vs 苹果是水果)")
print(f"句子 [0] vs [2]: {sim_0_2.item():.4f}  (喜欢吃苹果 vs 苹果手机)")
print(f"句子 [1] vs [2]: {sim_1_2.item():.4f}  (苹果是水果 vs 苹果手机)")

```

---

### 代码逻辑拆解

1. **`model.encode(texts)`**：这是最核心的一步。它内部完成了：
* 将文本切分为 **Tokens**。
* 通过 Transformer 层提取**上下文特征**。
* 执行 **Mean Pooling（平均池化）**，将所有 Token 的特征聚合成一个固定维度的向量。


2. **`util.cos_sim`**：执行**余弦相似度**计算。结果在 -1 到 1 之间，越接近 1 表示语义越相似。

### 预期结果分析

当你运行这段代码后，你会发现：

* **0 和 1 的得分最高**（通常在 0.8 以上），因为它们都在讨论“吃苹果”这件事。
* **0 和 2 的得分明显较低**，虽然都有“苹果”和“喜欢”，但模型识别出“吃”和“手机”属于完全不同的语义领域。

---

### 进阶：如果你想看这个“浓缩”后的向量长什么样

你可以打印 `embeddings[0].shape`，你会看到类似 `(384,)` 的结果。如果你直接 `print(embeddings[0])`，你会看到一串密密麻麻的数字，这就是那个句子在 AI 眼中的**“数字灵魂”**。

你需要我解释一下代码中那个 `384` 维度的数字具体代表什么含义吗？