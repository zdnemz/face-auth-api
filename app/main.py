from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import face_verify, face_register
import os

app = FastAPI()

# Routing API
app.include_router(face_verify.router, prefix="/api")
app.include_router(face_register.router, prefix="/api")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
