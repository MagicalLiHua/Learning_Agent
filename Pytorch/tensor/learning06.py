import torch
import torch.nn as nn # 引入神经网络模块

# 1. 数据变成了行向量 (代表 1个样本，包含 2个特征)
# 注意：在真实训练中，x 通常是我们的输入数据（比如图片的像素），它是固定的，不需要求导。
# 真正需要求导和更新的是神经网络里面的权重！所以这里去掉了 requires_grad=True
x = torch.tensor([[1.0, 1.0]])
y_target = torch.tensor([[10.0, 10.0]])

# 2. 召唤“积木”：定义一个线性层
# in_features=2 (输入向量长度为2), out_features=2 (输出向量长度为2)
# 这个 layer 就像一个盲盒，它内部自动生成并隐藏了我们需要优化的权重矩阵 W 和偏置 b！
layer = nn.Linear(in_features=2, out_features=2)

optimizer = torch.optim.SGD(layer.parameters(), lr=1e-2)

for i in range(100):
    optimizer.zero_grad()

    output = layer(x)

    loss = ((output - y_target) ** 2).mean()
    loss.backward()

    optimizer.step()

    print(f"Loss: {loss}, output: {output.data}")

    print("训练后的权重 W:\n", layer.weight)
    print("训练后的偏置 b:\n", layer.bias)