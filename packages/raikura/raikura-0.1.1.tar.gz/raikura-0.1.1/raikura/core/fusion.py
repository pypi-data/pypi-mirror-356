import torch
import torch.nn as nn
from transformers import AutoModel, AutoTokenizer
from torchvision import models

class TabularEncoder(nn.Module):
    def __init__(self, input_dim, hidden_dims=[128, 64]):
        super().__init__()
        layers = []
        dims = [input_dim] + hidden_dims
        for i in range(len(dims) - 1):
            layers += [nn.Linear(dims[i], dims[i+1]), nn.ReLU(), nn.BatchNorm1d(dims[i+1])]
        self.encoder = nn.Sequential(*layers)

    def forward(self, x):
        return self.encoder(x)

class TextEncoder(nn.Module):
    def __init__(self, model_name="distilbert-base-uncased", freeze=True):
        super().__init__()
        self.transformer = AutoModel.from_pretrained(model_name)
        if freeze:
            for param in self.transformer.parameters():
                param.requires_grad = False

    def forward(self, input_ids, attention_mask):
        output = self.transformer(input_ids=input_ids, attention_mask=attention_mask)
        return output.last_hidden_state[:, 0, :]  # CLS token

class ImageEncoder(nn.Module):
    def __init__(self, backbone="resnet18", freeze=True):
        super().__init__()
        cnn = getattr(models, backbone)(pretrained=True)
        if freeze:
            for param in cnn.parameters():
                param.requires_grad = False
        self.encoder = nn.Sequential(*list(cnn.children())[:-1])  # remove FC

    def forward(self, x):
        x = self.encoder(x)
        return x.view(x.size(0), -1)

class FusionModel(nn.Module):
    def __init__(self, tabular_dim=16, text_dim=768, image_dim=512, out_dim=2):
        super().__init__()
        self.tabular = TabularEncoder(tabular_dim)
        self.text = TextEncoder()
        self.image = ImageEncoder()
        self.fusion = nn.Sequential(
            nn.Linear(64 + text_dim + image_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, out_dim)
        )

    def forward(self, tab_x, text_ids, text_mask, image_x):
        tab_out = self.tabular(tab_x)
        text_out = self.text(text_ids, text_mask)
        image_out = self.image(image_x)
        combined = torch.cat([tab_out, text_out, image_out], dim=1)
        return self.fusion(combined)
