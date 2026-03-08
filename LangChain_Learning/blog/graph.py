from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableParallel
from loguru import logger

# 设置本地模型，不使用深度思考
model = ChatOllama(base_url="http://10.160.108.2:11434",model="qwen3-vl:8b")

# 并行链1提示词
prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
    ("human", "请简短介绍什么是{topic}")
])
# 并行链1解析器
parser1 = StrOutputParser()
# 并行链1：生成中文结果
chain1 = prompt1 | model | parser1

# 并行链2提示词
prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，请用英文简短回答"),
    ("human", "请简短介绍什么是{topic}")
])
# 并行链2解析器
parser2 = StrOutputParser()

# 并行链2：生成英文结果
chain2 = prompt2 | model | parser2

# 创建并行链,用于同时执行多个语言处理链
parallel_chain = RunnableParallel({
    "chinese": chain1,
    "english": chain2
})
# 将并行链的计算图绘制为PNG图片并保存
# parallel_chain.get_graph().draw_png("chain.png")
# 打印并行链的ASCII图形表示
parallel_chain.get_graph().print_ascii()
# 调用复合链
# result = parallel_chain.invoke({"topic": "langchain"})
# logger.info(f"最终结果:{result}")