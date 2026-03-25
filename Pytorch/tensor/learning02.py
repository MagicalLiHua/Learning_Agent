import torch

# 假设 W 是固定的参数，x 是我们需要求导的变量
W = torch.tensor([[2.0, 1.0],
                  [0.0, 3.0]])

# 加上 requires_grad=True，告诉 PyTorch：“请帮我追踪 x 的梯度”
x = torch.tensor([[1.0],
                  [1.0]], requires_grad=True)

# 1. 前向计算 (Forward Pass)
y = W @ x

# 2. 计算一个标量损失 (Loss)
# 在机器学习中，我们通常需要一个标量（0维张量）来评估模型的表现。
# 这里我们简单地把 y 里面的所有元素加起来，得到一个标量 L
L = y.sum()
print("标量 L 的值:", L)

# 在上面代码的最后，如果我想让 PyTorch 自动帮我完成这个求导过程（术语叫反向传播），并把算出来的偏导数打印出来，你应该调用哪个函数？算出来的偏导数又会存储在 x 的哪个属性里面呢？
L.backward()
print(x.grad)

# 设定学习率
lr = 1e-3

# 暂停梯度追踪，安全地进行参数更新
with torch.no_grad():
    # 待填写的更新代码
    x -= lr * x.grad

print("更新后的 x:\n", x)