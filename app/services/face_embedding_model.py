import numpy as np
import torch
from PIL import Image
from typing import List
import torchvision.transforms as transforms
from facenet_pytorch import InceptionResnetV1

# Load FaceNet model
model = InceptionResnetV1(pretrained='vggface2').eval()

def get_embedding(image: Image.Image) -> np.ndarray:
    transform = transforms.Compose([
        transforms.Resize((160, 160)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5])
    ])
    img_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        embedding = model(img_tensor)
    return embedding.squeeze().numpy()

def choose_best_embedding(images: List[Image.Image]) -> np.ndarray:
    embeddings = [get_embedding(img) for img in images]
    n = len(embeddings)
    similarities = np.zeros(n)

    for i in range(n):
        sims = [
            np.dot(embeddings[i], embeddings[j]) / (np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j]))
            for j in range(n) if j != i
        ]
        similarities[i] = np.mean(sims)

    best_idx = int(np.argmax(similarities))
    return embeddings[best_idx], best_idx

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Hitung cosine similarity antara dua embedding wajah"""
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot / (norm1 * norm2)
