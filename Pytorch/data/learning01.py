import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F


# 1. 定义我们的“图书馆”
class MyMathDataset(Dataset):
    def __init__(self, num_samples=1000):
        super().__init__()
        # 生成 1000 个随机样本，每个样本 2 个特征
        self.x_data = torch.randn(num_samples, 2)

        # 按照隐藏规律生成 y，并加入 0.1 倍的随机噪声模拟真实世界的测量误差
        y1 = self.x_data[:, 0] + 2 * self.x_data[:, 1]
        y2 = self.x_data[:, 0] - self.x_data[:, 1]
        self.y_data = torch.stack([y1, y2], dim=1) + 0.1 * torch.randn(num_samples, 2)

    def __len__(self):
        # 告诉 PyTorch 数据集有多大
        return len(self.x_data)

    def __getitem__(self, idx):
        # 告诉 PyTorch 如何取出第 idx 条数据
        return self.x_data[idx], self.y_data[idx]


# 实例化数据集
dataset = MyMathDataset(num_samples=1000)

# 2. 召唤图书管理员 DataLoader
# batch_size=16 意味着每次抽取 16 条数据算作一小批 (Mini-batch)
# shuffle=True 意味着打乱顺序，防止模型死记硬背数据的排列规律
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

net = nn.Sequential(
    nn.Linear(in_features=2, out_features=4),
    nn.ReLU(),
    nn.Linear(in_features=4, out_features=2)
)

optimizer = torch.optim.SGD(net.parameters(), lr=0.01)

epochs = 100 # 总共把整个数据集看 10 遍

for epoch in range(epochs):
    curr_loss = 0
    # 图书管理员 dataloader 开始一摞一摞地搬书
    for batch_x, batch_y in dataloader:
        optimizer.zero_grad()
        loss = F.mse_loss(net(batch_x), batch_y)
        loss.backward()
        optimizer.step()
        curr_loss += loss.item()

    print(f"Epoch {epoch + 1}/{epochs}, Loss: {curr_loss / len(dataloader):.4f}")

