from state import State
from langchain_core.messages import AIMessage
from loguru import logger


async def reimburse_node(state: State) -> State:
    logger.info("执行报销处理 Agent...")

    # 这里可以接入 OCR 工具提取发票信息
    result = "您的餐补发票已成功提交，系统正在提取发票抬头和金额，即将进入审批流。"

    return State(
        messages=state.messages + [AIMessage(content=result)],
        type="reimburse",
        phase="gather"
    )