import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from .generator import Generator
from .discriminator import Discriminator

class GAN:
    def __init__(self, img_size=80, latent_dim=100, lr=0.0002, batch_size=64):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.generator = Generator(input_dim=latent_dim, img_size=img_size).to(self.device)
        self.discriminator = Discriminator(img_size=img_size).to(self.device)
        self.optimizer_G = optim.Adam(self.generator.parameters(), lr=lr, betas=(0.5, 0.999))
        self.optimizer_D = optim.Adam(self.discriminator.parameters(), lr=lr, betas=(0.5, 0.999))
        self.criterion = nn.BCELoss()

    def train(self, dataloader, epochs=50):
        for epoch in range(epochs):
            for i, (imgs, _) in enumerate(dataloader):
                valid = torch.ones(imgs.size(0), 1).to(self.device)
                fake = torch.zeros(imgs.size(0), 1).to(self.device)

                # Train Generator
                self.optimizer_G.zero_grad()
                z = torch.randn(imgs.size(0), 100, 1, 1).to(self.device)
                gen_imgs = self.generator(z)
                g_loss = self.criterion(self.discriminator(gen_imgs), valid)
                g_loss.backward()
                self.optimizer_G.step()

                # Train Discriminator
                self.optimizer_D.zero_grad()
                real_loss = self.criterion(self.discriminator(imgs.to(self.device)), valid)
                fake_loss = self.criterion(self.discriminator(gen_imgs.detach()), fake)
                d_loss = (real_loss + fake_loss) / 2
                d_loss.backward()
                self.optimizer_D.step()

                if i % 100 == 0:
                    print(f"[Epoch {epoch}/{epochs}] [Batch {i}/{len(dataloader)}] [D loss: {d_loss.item()}] [G loss: {g_loss.item()}]")

    def generate(self, num_samples=1):
        z = torch.randn(num_samples, 100, 1, 1).to(self.device)
        return self.generator(z).detach().cpu()