from datetime import date
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from loguru import logger


@tool
def get_today() -> str:
    """
    获取当前系统日期

    Returns:
        str: 今天的日期字符串，格式为 yyyy-MM-dd
    """
    logger.info("执行工具：get_today")
    return date.today().isoformat()


# 设置本地模型，不使用深度思考
llm = ChatOllama(base_url="http://10.160.108.2:11434",model="qwen3-vl:8b")
# 将工具绑定到语言模型
llm_with_tools = llm.bind_tools([get_today])
# 用户提问
question_list = ["你是谁？","今天是几号？"]
for question in question_list:
    logger.info(f"用户问题：{question}")
    # 调用语言模型处理用户问题
    ai_msg = llm_with_tools.invoke(question)
    logger.info(f"LLM回复：{ai_msg}")
    # 检查是否有工具调用
    if ai_msg.tool_calls:
        logger.info(ai_msg.tool_calls)
        # 获取第一个工具调用信息
        tool_call = ai_msg.tool_calls[0]
        # 执行对应的工具函数并获取结果
        tool_result = locals()[tool_call["name"]].invoke(tool_call["args"])
        logger.info(f"调用工具结果：{tool_result}")
    else:
        # 直接输出语言模型的回答
        logger.info(f"LLM 直接作答：{ai_msg.content}")