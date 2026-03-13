from state import State
from langchain_core.messages import AIMessage
from loguru import logger


async def customer_service_node(state: State) -> State:
    logger.info("执行外卖客服 Agent...")

    # 这里可以接入查询外卖订单的 API，目前先用 Mock 数据返回
    result = "您的外卖退款申请已收到，我们正在为您处理，预计1-3个工作日退回原账户。"

    # 状态更新：将结果追加到 messages，并将阶段修改为 gather 让 Supervisor 收集
    return State(
        messages=state.messages + [AIMessage(content=result)],
        type="customer_service",
        phase="gather"
    )