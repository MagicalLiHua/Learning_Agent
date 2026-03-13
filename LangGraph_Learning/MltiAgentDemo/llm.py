from langchain_ollama import ChatOllama

# 初始化本地大语言模型
llm = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b", reasoning=False)

chat_model = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b", reasoning=False)