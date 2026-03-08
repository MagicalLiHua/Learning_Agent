from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama

# 设置本地模型，不使用深度思考
model = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b")

# 问题列表
questions = [
    "什么是LangChain？",
    "Python的生成器是做什么的？",
    "解释一下Docker和Kubernetes的关系"
]
# 批量调用大模型
response = model.batch(questions)
for q, r in zip(questions, response):
    print(f"问题：{q}\n回答：{r}\n")