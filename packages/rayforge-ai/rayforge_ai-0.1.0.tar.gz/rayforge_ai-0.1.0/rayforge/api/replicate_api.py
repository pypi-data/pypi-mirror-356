import os
import requests
import time
from typing import Optional, List
from rayforge.utils.logger import get_logger

logger = get_logger()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
REPLICATE_BASE_URL = "https://api.replicate.com/v1"
HEADERS = {
    "Authorization": f"Token {REPLICATE_API_TOKEN}",
    "Content-Type": "application/json"
}

if not REPLICATE_API_TOKEN:
    raise RuntimeError("REPLICATE_API_TOKEN must be set as an environment variable.")

def list_models(limit: int = 20) -> List[str]:
    """List public models (paginated)."""
    try:
        url = f"{REPLICATE_BASE_URL}/models?limit={limit}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return [f"{m['owner']}/{m['name']}" for m in response.json()["results"]]
    except Exception as e:
        logger.error(f"Failed to list Replicate models: {e}")
        return []

def get_model_info(owner: str, name: str) -> dict:
    """Get metadata for a specific model."""
    try:
        url = f"{REPLICATE_BASE_URL}/models/{owner}/{name}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch model info: {e}")
        return {}

def get_latest_version(owner: str, name: str) -> str:
    """Get the latest version ID of a model."""
    try:
        info = get_model_info(owner, name)
        return info.get("latest_version", {}).get("id")
    except Exception as e:
        logger.error(f"Could not get version for {owner}/{name}: {e}")
        return ""

def run_prediction(owner: str, name: str, inputs: dict, stream: bool = False, polling: float = 1.0) -> dict:
    """Run a prediction on a given model with inputs."""
    try:
        version = get_latest_version(owner, name)
        logger.info(f"Running prediction on {owner}/{name} [{version}]")
        url = f"{REPLICATE_BASE_URL}/predictions"
        payload = {
            "version": version,
            "input": inputs
        }
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        prediction = response.json()

        if not stream:
            return wait_for_prediction(prediction["id"], polling=polling)
        else:
            return stream_prediction(prediction["id"], polling=polling)
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        return {"error": str(e)}

def wait_for_prediction(prediction_id: str, polling: float = 1.0) -> dict:
    """Poll a prediction until it finishes."""
    try:
        url = f"{REPLICATE_BASE_URL}/predictions/{prediction_id}"
        while True:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            status = data.get("status")
            logger.info(f"Prediction status: {status}")
            if status in ["succeeded", "failed", "canceled"]:
                return data
            time.sleep(polling)
    except Exception as e:
        logger.error(f"Polling error: {e}")
        return {"error": str(e)}

def stream_prediction(prediction_id: str, polling: float = 1.0):
    """Stream prediction output (chunked or progressive)."""
    try:
        url = f"{REPLICATE_BASE_URL}/predictions/{prediction_id}"
        seen_output = ""
        while True:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            status = data.get("status")
            output = data.get("output", "")

            # Stream new content only
            if isinstance(output, str) and output.startswith(seen_output):
                new_output = output[len(seen_output):]
                seen_output = output
                yield new_output

            elif isinstance(output, list) and output:
                yield output

            if status in ["succeeded", "failed", "canceled"]:
                break
            time.sleep(polling)
    except Exception as e:
        logger.error(f"Streaming failed: {e}")
        yield f"[ERROR] {e}"

def cancel_prediction(prediction_id: str) -> bool:
    """Cancel a running prediction."""
    try:
        url = f"{REPLICATE_BASE_URL}/predictions/{prediction_id}/cancel"
        response = requests.post(url, headers=HEADERS)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Cancel failed: {e}")
        return False

def download_prediction_output(prediction: dict, dest_folder: str = "rayforge_outputs") -> List[str]:
    """Download output files from prediction if available."""
    try:
        os.makedirs(dest_folder, exist_ok=True)
        outputs = prediction.get("output", [])
        if isinstance(outputs, str):
            outputs = [outputs]

        saved_paths = []
        for i, url in enumerate(outputs):
            response = requests.get(url)
            fname = f"{dest_folder}/output_{i}.png" if url.endswith(".png") else f"{dest_folder}/output_{i}.txt"
            with open(fname, "wb") as f:
                f.write(response.content)
            saved_paths.append(fname)
        return saved_paths
    except Exception as e:
        logger.error(f"Failed to download outputs: {e}")
        return []
