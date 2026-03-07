import time

# 1. 原始语料库（生成器表达式：极省内存）
raw_corpus = (f"这是第 {i} 条原始语料内容..." for i in range(3))

# 2. 预处理器（过滤与清洗生成器）
def preprocessor(corpus):
    for text in corpus:
        # 模拟清洗逻辑
        yield text.replace("原始", "【已清洗】")

# 3. 模拟 LLM 推理引擎（流式输出生成器）
def llm_engine(text):
    print(f"\n--- 模型开始处理: {text} ---")
    tokens = ["我", "是一个", "人工智能", "助手", "。"]
    for token in tokens:
        time.sleep(0.3)  # 模拟推理耗时
        yield token

# 4. 总控中心（使用 yield from 整合）
def ai_agent():
    cleaned_data = preprocessor(raw_corpus)
    for data in cleaned_data:
        # 将推理流直接“穿透”给调用者
        yield from llm_engine(data)

# --- 运行 AI Agent ---
print("开始执行 AI 任务流水线...")
for word in ai_agent():
    print(word, end="", flush=True)