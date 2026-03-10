from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.utilities import PythonREPL
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama
from loguru import logger


def debug_print(x):
    """
    调试打印函数，用于在链式调用中输出中间结果

    参数:
        x: 任意类型的输入值，将被打印并原样返回

    返回值:
        与输入值x相同的值
    """
    logger.info(f"中间结果:{x}")
    return x


# 创建Python REPL工具实例，用于执行生成的Python代码
tool = PythonREPL()

# 初始化Ollama语言模型，使用qwen3:8b模型
llm = ChatOllama(base_url="http://10.160.108.2:11434",model="qwen3-vl:8b")

# 定义聊天提示模板，包含系统指令和用户问题占位符
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你只返回纯净的 Python 代码，不要解释。代码必须是单行或多行 print。"),
        ("human", "{question}")
    ]
)

# 创建调试节点，用于在链式调用中插入调试信息输出
debug_node = RunnableLambda(debug_print)

# 创建字符串输出解析器，用于解析模型输出
parser = StrOutputParser()

# 构建处理链：提示模板 -> 语言模型 -> 调试输出 -> 输出解析 -> 代码执行
chain = prompt | llm | debug_node | parser | RunnableLambda(lambda code: tool.run(code))

# 执行链式调用，计算1到100的整数总和
result = chain.invoke({"question": "计算1到100的整数总和"})
logger.info(result)