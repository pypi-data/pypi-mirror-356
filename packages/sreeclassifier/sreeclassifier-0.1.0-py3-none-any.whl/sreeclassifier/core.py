# sreeclassifier/core.py

import torch
from torchvision import models, transforms
from PIL import Image
import os

class ImageClassifier:
    def __init__(self, model_name='vit_b_16'):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model(model_name).to(self.device)
        self.model.eval()
        self.transform = self._build_transform()
        self.labels = self._load_labels()

    def _load_model(self, model_name):
        if model_name == 'vit_b_16':
            model = models.vit_b_16(pretrained=True)
        else:
            raise ValueError(f"Unsupported model: {model_name}")
        return model

    def _build_transform(self):
        return transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            )
        ])

    def _load_labels(self):
        path = os.path.join(os.path.dirname(__file__), "imagenet_classes.txt")
        with open(path) as f:
            return [line.strip() for line in f.readlines()]

    def predict(self, image_path, topk=1):
        image = Image.open(image_path).convert("RGB")
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            output = self.model(img_tensor)
            probs = torch.nn.functional.softmax(output[0], dim=0)
            topk_probs, topk_indices = torch.topk(probs, topk)
            return [(self.labels[i], round(p.item(), 4)) for i, p in zip(topk_indices, topk_probs)]
