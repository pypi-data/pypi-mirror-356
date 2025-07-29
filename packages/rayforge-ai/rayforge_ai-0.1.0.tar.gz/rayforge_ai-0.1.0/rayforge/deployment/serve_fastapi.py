from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import uvicorn
from typing import Generator

from rayforge.core.forge_engine import Forge
from rayforge.utils.logger import get_logger

logger = get_logger()

app = FastAPI(
    title="RayForge Model Server",
    description="Serve any model pulled by Forge as a REST API.",
    version="1.0.0"
)

# Global Forge context and loaded model
forge = Forge()
model_info = {}

# === Pydantic Input Schema ===

class InferenceInput(BaseModel):
    input: str
    task: str | None = None
    stream: bool = False

class ReplicateInput(BaseModel):
    input: dict
    stream: bool = False

# === Endpoints ===

@app.get("/")
def root():
    return {
        "message": f"✅ Model '{model_info.get('id', 'none')}' is ready.",
        "task": model_info.get("task", "unknown"),
        "source": model_info.get("source", "unknown")
    }

@app.get("/meta")
def meta():
    return forge.describe(model_info)

@app.post("/predict")
def predict(data: InferenceInput):
    """
    Standard inference call. Accepts input string + optional task override.
    """
    try:
        logger.info(f"Received input: {data.input[:50]}...")
        result = forge.run(model_info, data.input, task=data.task, stream=False)
        return {"output": result}
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/replicate")
def replicate(data: ReplicateInput):
    """
    Run prediction using Replicate-compatible input dictionary.
    """
    if model_info.get("source") != "replicate":
        raise HTTPException(status_code=400, detail="Model is not from Replicate.")
    try:
        result = forge.run(model_info, data.input, stream=False)
        return {"output": result}
    except Exception as e:
        logger.error(f"Replicate prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stream")
def stream(data: InferenceInput):
    """
    Stream output tokens from supported models (OpenAI/Replicate).
    """
    try:
        logger.info(f"Streaming input: {data.input[:50]}...")

        def generate() -> Generator[str, None, None]:
            for chunk in forge.run(model_info, data.input, task=data.task, stream=True):
                yield chunk

        return StreamingResponse(generate(), media_type="text/plain")
    except Exception as e:
        logger.error(f"Streaming failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === Entrypoint ===

def serve_model(loaded_model_info: dict, port: int = 7860):
    """
    Serve the given model on the specified port.
    Should be called from CLI or script.
    """
    global model_info
    model_info = loaded_model_info
    logger.info(f"Starting FastAPI server for model '{model_info['id']}' on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
