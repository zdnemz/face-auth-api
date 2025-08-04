import numpy as np
from PIL import Image
from typing import List
import os
from .face_embedding_model import get_embedding, cosine_similarity, choose_best_embedding

THRESHOLD = 0.6
EMBEDDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "embeddings")

def verify_face_from_image(user_id: str, image: Image.Image) -> dict:
    emb_path = os.path.join(EMBEDDINGS_DIR, f"{user_id}.npy")

    if not os.path.exists(emb_path):
        return {"success": False, "message": "Embedding tidak ditemukan.", "score": None}

    registered_emb = np.load(emb_path)

    try:
        current_emb = get_embedding(image)
        score = cosine_similarity(registered_emb, current_emb)
        result = bool(score > THRESHOLD)
        
        return {
            "success": result,
            "message": "✅ Verifikasi berhasil." if result else "❌ Wajah tidak cocok.",
            "score": float(score)
        }
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}", "score": None}
    
def register_user(user_id: str, images: List[Image.Image]) -> dict:
    best_embedding, best_index = choose_best_embedding(images)

    os.makedirs(EMBEDDINGS_DIR, exist_ok=True)
    emb_path = os.path.join(EMBEDDINGS_DIR, f"{user_id}.npy")
    np.save(emb_path, best_embedding)

    return {
        "user_id": user_id,
        "embedding_saved_at": emb_path,
        "best_image_index": best_index
    }
