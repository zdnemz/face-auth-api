from fastapi import APIRouter, UploadFile, File, Form
from PIL import Image
import io
from typing import List
from app.services.face_service import register_user

router = APIRouter()

@router.post("/register-face")
async def register_face(user_id: str = Form(...), images: List[UploadFile] = File(...)):
    if len(images) < 5:
        return {"success": False, "message": "Minimal 5 gambar diperlukan."}

    pil_images = []
    for image in images:
        if image.content_type not in ["image/jpeg", "image/png"]:
            return {"success": False, "message": f"{image.filename} bukan JPEG/PNG"}
        img_bytes = await image.read()
        pil = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        pil_images.append(pil)

    result = register_user(user_id, pil_images)
    return {"success": True, "message": "Registrasi berhasil", "result": result}
