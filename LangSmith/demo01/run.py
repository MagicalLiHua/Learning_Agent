import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
# 读取env配置
dotenv.load_dotenv()
# 构建 prompt 模板
template = """
    使用中文回答下面的问题：
    问题: {question}
    """
prompt = ChatPromptTemplate.from_template(template)

# 设置本地模型，不使用深度思考
model = ChatOllama(base_url="http://10.160.108.2:11434", model="qwen3-vl:8b")

# 创建 Chain
chain = prompt | model

# 打印结果
print(chain.invoke({"question": "什么是LangChain?"}))