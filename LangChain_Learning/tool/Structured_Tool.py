from langchain_core.tools import StructuredTool
from loguru import logger
from pydantic import BaseModel, Field


class FieldInfo(BaseModel):
    """
    定义加法运算所需的参数信息
    """
    a: int = Field(description="第1个参数")
    b: int = Field(description="第2个参数")


def add_number(a: int, b: int) -> int:
    """
    两个整数相加
    """
    return a + b


func = StructuredTool.from_function(
    func=add_number,
    name="Add",
    description="两个整数相加",
    args_schema=FieldInfo
)
logger.info(f"name = {func.name}")
logger.info(f"description = {func.description}")
logger.info(f"args = {func.args}")

res = func.invoke({"a": 1, "b": 2})
logger.info(res)