import torch
import torch.nn as nn # 引入神经网络模块

# 1. 数据变成了行向量 (代表 1个样本，包含 2个特征)
# 注意：在真实训练中，x 通常是我们的输入数据（比如图片的像素），它是固定的，不需要求导。
# 真正需要求导和更新的是神经网络里面的权重！所以这里去掉了 requires_grad=True
# x = torch.tensor([[1.0, 1.0]])
# y_target = torch.tensor([[10.0, 10.0]])

# 给它 4 个样本，目标是让网络学到：输出就是输入的 2 倍！
x = torch.tensor([[1.0, 1.0],
                  [2.0, 2.0],
                  [3.0, 3.0],
                  [4.0, 4.0]])

y_target = torch.tensor([[2.0, 2.0],
                         [4.0, 4.0],
                         [6.0, 6.0],
                         [8.0, 8.0]])

# 构建一个真正的多层前馈神经网络 (MLP)
net = nn.Sequential(
    nn.Linear(in_features=2, out_features=4), # 第一层：把2维特征升维到4维，提取更多信息
    nn.ReLU(),                                # 激活函数：注入非线性魔法！
    nn.Linear(in_features=4, out_features=2)  # 第二层：把4维特征降维回2维，输出预测结果
)

optimizer = torch.optim.SGD(net.parameters(), lr=1e-2)

for i in range(100):
    optimizer.zero_grad()

    output = net(x)

    loss = ((output - y_target) ** 2).mean()
    loss.backward()

    optimizer.step()

    print(f"Loss: {loss}, output: {output.data}")