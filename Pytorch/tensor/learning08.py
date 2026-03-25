import torch
import torch.nn as nn

# 这是一个 4x2 的矩阵，代表 4 个样本 (Batch Size = 4)
x = torch.tensor([[1.0, 1.0],
                  [2.0, 0.0],
                  [0.0, 3.0],
                  [2.0, 2.0]])

# 这是对应的 4x2 的目标矩阵 (按照上面的隐藏规律计算得出)
y_target = torch.tensor([[3.0,  0.0],
                         [2.0,  2.0],
                         [6.0, -3.0],
                         [6.0,  0.0]])

# 2. 定义网络和优化器
net = nn.Sequential(
    nn.Linear(in_features=2, out_features=4),
    nn.ReLU(),
    nn.Linear(in_features=4, out_features=2)
)

optimizer = torch.optim.SGD(net.parameters(), lr=0.01)

# 3. 训练循环 (完全没改！只是增加了点迭代次数，因为找规律比死记硬背难)
for i in range(10000):
    optimizer.zero_grad()

    # 自动并行处理 4 个样本
    output = net(x)

    # 计算 4 个样本的平均均方误差 (MSE)
    loss = ((output - y_target) ** 2).mean()

    loss.backward()
    optimizer.step()

    if (i + 1) % 100 == 0:
        print(f"迭代 {i + 1}, Loss: {loss.item():.4f}")

# 4. 【大考时刻】给它一个从来没见过的数据！
print("\n=== 考试开始 ===")
test_x = torch.tensor([[3.0, 1.0]])  # 没在训练集里出现过
net.eval()
with torch.no_grad():  # 测试时不需要计算梯度
    prediction = net(test_x)

print(f"预测输出: {prediction.data.numpy()}")