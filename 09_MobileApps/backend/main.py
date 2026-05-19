from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from model_service import predict_image

app = FastAPI(title="Coral Health AI Mobile Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/api/predict")
async def predict(
    image: UploadFile = File(...),
    model_type: str = Form("ensemble"),
    gradcam_enabled: str = Form("true"),
) -> dict:
    _ = gradcam_enabled
    image_bytes = await image.read()
    return predict_image(image_bytes, model_type)
