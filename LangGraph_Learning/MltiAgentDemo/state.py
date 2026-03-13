from pydantic import BaseModel, Field
from typing import Any

class State(BaseModel):
    # 存放对话历史，允许传入字符串或 LangChain 的 Message 对象
    messages: list[Any] = Field(default_factory=list)
    # 用于记录分配给哪个 Agent (recommend / customer_service / reimburse)
    type: str = ""
    # 控制流程的状态，默认是分发阶段 (dispatch -> gather -> done)
    phase: str = "dispatch"