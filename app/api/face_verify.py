from fastapi import APIRouter, UploadFile, File, Form
from PIL import Image
import io
from app.services.face_service import verify_face_from_image

router = APIRouter()

@router.post("/verify-face")
async def verify_face(user_id: str = Form(...), image: UploadFile = File(...)):
    if image.content_type not in ["image/jpeg", "image/png"]:
        return {"success": False, "message": "Gunakan format JPEG atau PNG."}

    image_bytes = await image.read()
    pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    result = verify_face_from_image(user_id, pil_image)
    return result
