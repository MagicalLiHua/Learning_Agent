from typing import TypedDict, Annotated
import operator

# 请补全这个 TypedDict，我们需要它包含两个字段：
# 1. messages: 一个列表，用来存储对话历史。
#    进阶提示：为了让新消息能“追加”到列表中而不是覆盖，我们可以使用 Annotated 和 operator.add。
# 2. step_count: 一个整数，用来记录 Agent 运行的步数。默认应该是每次加 1。

class AgentState(TypedDict):
    """
    定义 Agent 的全局状态
    """
    messages: Annotated[list[str], operator.add]    # 对话历史，新的消息会追加到列表中
    step_count: Annotated[int, operator.add]        # 运行步数，每次调用时加1