import os
import torch
import torch.optim as optim
import torchvision.utils as vutils
from torch.utils.data import DataLoader
from torchvision import transforms
from PIL import Image
from smodels.modelf import Generator
from smodels.modelf import Discriminator
import torch.nn as nn

# 创建保存模型和样本的目录
os.makedirs("tmodels", exist_ok=True)
os.makedirs("tsamples", exist_ok=True)

# 定义设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 数据集加载
class FontDataset(torch.utils.data.Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.image_paths = [os.path.join(data_dir, img) for img in os.listdir(data_dir)]

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('L')  # 转换为灰度图像
        if self.transform:
            image = self.transform(image)
        return image




# 训练代码
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
os.makedirs("tmodels", exist_ok=True)
os.makedirs("tsamples", exist_ok=True)

# 数据预处理
transform = transforms.Compose([
    transforms.Resize((80, 80)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# 加载数据集
data_dir = "save_folder/id_2"
dataset = FontDataset(data_dir, transform=transform)
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

# 初始化模型
generator = Generator(latent_dim=100, feature_maps=64).to(device)
discriminator = Discriminator(feature_maps=64).to(device)

# 优化器和损失函数
adversarial_loss = nn.BCELoss()
optimizer_G = optim.Adam(generator.parameters(), lr=0.0002, betas=(0.5, 0.999))
optimizer_D = optim.Adam(discriminator.parameters(), lr=0.0002, betas=(0.5, 0.999))

# 训练参数
num_epochs = 200
sample_interval = 500

# 训练循环
for epoch in range(num_epochs):
    for i, real_imgs in enumerate(dataloader):
        batch_size = real_imgs.shape[0]
        real_imgs = real_imgs.to(device)
        valid = torch.ones(batch_size, 1).to(device)
        fake = torch.zeros(batch_size, 1).to(device)

        # 训练判别器
        optimizer_D.zero_grad()
        z = torch.randn(batch_size, 100).to(device)
        gen_imgs = generator(z, real_imgs).detach()
        real_loss = adversarial_loss(discriminator(real_imgs), valid)
        fake_loss = adversarial_loss(discriminator(gen_imgs), fake)
        d_loss = (real_loss + fake_loss) / 2
        d_loss.backward()
        optimizer_D.step()

        # 训练生成器
        optimizer_G.zero_grad()
        gen_imgs = generator(z, real_imgs)
        g_loss = adversarial_loss(discriminator(gen_imgs), valid)
        g_loss.backward()
        optimizer_G.step()

        if i % 100 == 0:
            print(f"[Epoch {epoch}/{num_epochs}] [Batch {i}/{len(dataloader)}] "
                  f"[D loss: {d_loss.item()}] [G loss: {g_loss.item()}]")

        if i % sample_interval == 0:
            with torch.no_grad():
                z = torch.randn(25, 100).to(device)
                gen_imgs = generator(z, real_imgs[:25]).cpu()
                vutils.save_image(gen_imgs, f"tsamples/epoch_{epoch}_batch_{i}.png", normalize=True, nrow=5)

    if epoch % 50 == 0:
        torch.save(generator.state_dict(), f"tmodels/generator_epoch_{epoch}.pth")
        torch.save(discriminator.state_dict(), f"tmodels/discriminator_epoch_{epoch}.pth")

torch.save(generator.state_dict(), "tmodels/generator_final.pth")
torch.save(discriminator.state_dict(), "tmodels/discriminator_final.pth")