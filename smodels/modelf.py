import torch
import torch.nn as nn

class SelfAttention(nn.Module):
    def __init__(self, in_channels):
        super(SelfAttention, self).__init__()
        self.query_conv = nn.Conv2d(in_channels, in_channels // 8, 1)
        self.key_conv = nn.Conv2d(in_channels, in_channels // 8, 1)
        self.value_conv = nn.Conv2d(in_channels, in_channels, 1)
        self.gamma = nn.Parameter(torch.zeros(1))

    def forward(self, x):
        batch_size, C, width, height = x.size()
        proj_query = self.query_conv(x).view(batch_size, -1, width * height).permute(0, 2, 1)
        proj_key = self.key_conv(x).view(batch_size, -1, width * height)
        energy = torch.bmm(proj_query, proj_key)
        attention = torch.softmax(energy, dim=-1)
        proj_value = self.value_conv(x).view(batch_size, -1, width * height)

        out = torch.bmm(proj_value, attention.permute(0, 2, 1))
        out = out.view(batch_size, C, width, height)
        out = self.gamma * out + x
        return out


# 条件生成器
class Generator(nn.Module):
    def __init__(self, latent_dim=100, feature_maps=64):
        super(Generator, self).__init__()
        self.latent_dim = latent_dim
        self.feature_maps = feature_maps

        # 编码器：将输入图像编码为特征
        self.encoder = nn.Sequential(
            # 80x80 -> 40x40
            nn.Conv2d(1, feature_maps, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            # 40x40 -> 20x20
            nn.Conv2d(feature_maps, feature_maps * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # 20x20 -> 10x10
            nn.Conv2d(feature_maps * 2, feature_maps * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # 10x10 -> 5x5
            nn.Conv2d(feature_maps * 4, feature_maps * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 8),
            nn.LeakyReLU(0.2, inplace=True)
        )

        # 噪声初始处理
        self.noise_processor = nn.Sequential(
            nn.Linear(latent_dim, 5 * 5 * feature_maps * 4),
            nn.BatchNorm1d(feature_maps * 4 * 25),
            nn.LeakyReLU(0.2, inplace=True)
        )

        # 生成器主干网络
        self.decoder = nn.Sequential(
            # 5x5 -> 10x10
            nn.ConvTranspose2d(feature_maps * 12, feature_maps * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 4),
            nn.LeakyReLU(0.2, inplace=True),
            # 10x10 -> 20x20
            nn.ConvTranspose2d(feature_maps * 4, feature_maps * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 2),
            nn.LeakyReLU(0.2, inplace=True),
            # 自注意力层
            SelfAttention(feature_maps * 2),
            # 20x20 -> 40x40
            nn.ConvTranspose2d(feature_maps * 2, feature_maps, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps),
            nn.LeakyReLU(0.2, inplace=True),
            # 40x40 -> 80x80
            nn.ConvTranspose2d(feature_maps, 1, 4, 2, 1, bias=False),
            nn.Tanh()
        )

    def forward(self, z, condition_img):
        # 编码输入图像
        condition_features = self.encoder(condition_img)  # [batch, feature_maps*8, 5, 5]

        # 处理噪声
        noise_features = self.noise_processor(z)  # [batch, feature_maps*4*25]
        noise_features = noise_features.view(-1, self.feature_maps * 4, 5, 5)

        # 融合条件特征和噪声特征
        combined_features = torch.cat([condition_features, noise_features], dim=1)  # [batch, feature_maps*12, 5, 5]

        # 生成风格化图像
        output = self.decoder(combined_features)
        return output

# 生成器

# 判别器
class Discriminator(nn.Module):
    def __init__(self, feature_maps=64):
        super(Discriminator, self).__init__()
        self.feature_maps = feature_maps

        self.main = nn.Sequential(
            # 80x80 -> 40x40
            nn.Conv2d(1, feature_maps, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),

            # 40x40 -> 20x20
            nn.Conv2d(feature_maps, feature_maps * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 2),
            nn.LeakyReLU(0.2, inplace=True),

            # 20x20 -> 10x10
            nn.Conv2d(feature_maps * 2, feature_maps * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 4),
            nn.LeakyReLU(0.2, inplace=True),

            # 10x10 -> 5x5
            nn.Conv2d(feature_maps * 4, feature_maps * 8, 4, 2, 1, bias=False),
            nn.BatchNorm2d(feature_maps * 8),
            nn.LeakyReLU(0.2, inplace=True),
        )

        # 自注意力层
        self.self_attention = SelfAttention(feature_maps * 2)

        # 输出层
        self.classifier = nn.Sequential(
            nn.Conv2d(feature_maps * 8, 1, 5, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.main[0:2](x)  # 到40x40
        x = self.main[2:5](x)  # 到20x20
        x = self.self_attention(x)  # 添加自注意力
        x = self.main[5:](x)  # 到5x5
        x = self.classifier(x)
        return x.view(-1, 1)

# 使用示例
generator = Generator(latent_dim=100, feature_maps=64)
discriminator = Discriminator(feature_maps=64)