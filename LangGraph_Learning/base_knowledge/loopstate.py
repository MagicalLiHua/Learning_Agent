from langgraph.constants import START, END
from langgraph.graph import StateGraph
from loguru import logger
from pydantic import BaseModel


class LoopState(BaseModel):
    """
    循环状态模型类

    Attributes:
        x (int): 状态变量，用于循环计数
    """
    x: int


builder = StateGraph(LoopState)


def increment(state: LoopState) -> LoopState:
    """
    增量函数，将状态中的x值加1

    Args:
        state (LoopState): 包含当前x值的循环状态对象

    Returns:
        LoopState: 返回更新后的循环状态对象，其中x值增加1
    """
    logger.info(f"[increment] 当前 x = {state.x}")
    return LoopState(x=state.x + 1)


builder.add_node("increment", increment)


def is_done(state: LoopState) -> bool:
    """
    判断循环是否结束的条件函数

    Args:
        state (LoopState): 包含当前x值的循环状态对象

    Returns:
        bool: 当x值大于10时返回True，否则返回False
    """
    return state.x > 10


builder.add_conditional_edges("increment", is_done, {
    True: END,
    False: "increment"
})

builder.add_edge(START, "increment")

# 编译图结构
graph = builder.compile()

# 打印图结构
# graph.get_graph().draw_png('./graph.png')

# 初始化循环并执行，直到满足结束条件
logger.info("执行循环直到 x > 10，初始x = 6")
final_state = graph.invoke(LoopState(x=6))
logger.info(f"[最终结果] -> x = {final_state['x']}")