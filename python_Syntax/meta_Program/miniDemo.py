import asyncio
import functools

# ==========================================
# 1. 元编程 (Metaclass)：实现 Agent 的自动注册
# ==========================================
agent_registry = {}


class AgentMeta(type):
    # TODO 1: 拦截类的创建过程。只要有类使用这个元类，就把它自动存入 agent_registry 字典中。
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        agent_registry[name] = cls
        return cls


# ==========================================
# 2. 装饰器 (Decorator)：实现工具的日志记录
# ==========================================
# TODO 2: 写一个带参数的装饰器（或者普通装饰器），在被装饰的函数执行前后打印：
# "[日志] 开始执行..." 和 "[日志] 执行完毕..."
def log_tool_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("[日志] 开始执行...")
        result = func(*args, **kwargs)
        print("[日志] 执行完毕...")
        return result
    return wrapper


# ==========================================
# 3. 基础框架类 (融合异步、生成器与 __getattr__)
# ==========================================
class BaseAgent(metaclass=AgentMeta):
    def __init__(self, role: str):
        self.role = role

    # TODO 3: 元编程 (__getattr__) 动态属性拦截
    # 拦截用户对不存在方法的调用（例如 agent.write_code(lines=100)）
    # 在内部打印出被调用的 方法名 和 参数，模拟将其打包为 Prompt。
    def __getattr__(self, name):
        def func(*args, **kwargs):
            print(f"[{self.role}] 准备将指令发给 LLM: 方法名={name}, 参数={kwargs}")
        return func

    # TODO 4: 异步 (Asyncio) + 生成器 (Generator) 模拟流式输出
    # 模拟调用 LLM API。接收一个 prompt，使用 asyncio.sleep(0.5) 模拟网络延迟。
    # 把一句话（比如 "这是一段来自大模型的流式回复"）拆成一个个字，用 yield 异步产出。
    async def stream_chat(self, prompt: str):
        response = "这是一段来自大模型的流式回复"
        for char in response:
            await asyncio.sleep(0.3)  # 模拟网络延迟
            yield char  # 异步生成器产出一个字符


# ==========================================
# 4. 业务代码 (模拟用户使用你的框架)
# ==========================================
class CoderAgent(BaseAgent):
    pass


class PMAgent(BaseAgent):
    pass


# 用刚才写的装饰器包装一个普通函数，假装这是一个给 Agent 用的 Tool
@log_tool_execution
def search_web(query: str):
    print(f"正在搜索: {query}")


async def main():
    print("1. 检查注册表:", agent_registry)

    # 实例化一个 Coder
    coder = CoderAgent(role="Senior Python Developer")

    print("\n2. 测试装饰器:")
    search_web("如何写好元编程")

    print("\n3. 测试动态方法拦截:")
    # 调用一个根本不存在的方法，测试你的 __getattr__
    coder.write_api_server(framework="FastAPI", port=8000)

    print("\n4. 测试异步与生成器 (流式输出):")
    # 使用 async for 接收异步生成器产出的数据
    async for chunk in coder.stream_chat("请写一段 Hello World"):
        print(chunk, end="", flush=True)
    print()

# 运行主程序
asyncio.run(main())