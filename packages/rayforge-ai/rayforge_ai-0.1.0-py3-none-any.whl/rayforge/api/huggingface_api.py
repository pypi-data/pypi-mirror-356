from huggingface_hub import (
    HfApi,
    ModelFilter,
    ModelSearchArguments,
    snapshot_download,
    model_info,
    upload_folder,
    hf_hub_download,
    RepositoryNotFoundError,
)
from pathlib import Path
from typing import Optional
import json
import os
import time
from rayforge.utils.logger import get_logger

logger = get_logger()
api = HfApi()

# Optional: cache directory
CACHE_FILE = Path(".rayforge_cache/hf_search_cache.json")
CACHE_TTL = 3600  # seconds

def _cache_results(key: str, results: list):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    cache = {}
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r") as f:
            try:
                cache = json.load(f)
            except:
                cache = {}
    cache[key] = {"time": time.time(), "results": results}
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def _load_cached(key: str):
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r") as f:
            try:
                cache = json.load(f)
                if key in cache:
                    entry = cache[key]
                    if time.time() - entry["time"] < CACHE_TTL:
                        return entry["results"]
            except:
                return None
    return None

def search_models(query: str = "", task: Optional[str] = None, tag: Optional[str] = None, limit: int = 10):
    """
    Search Hugging Face models by query, task, or tag.
    Uses lightweight caching for performance.
    """
    key = f"{query}|{task}|{tag}|{limit}"
    cached = _load_cached(key)
    if cached:
        logger.info(f"Loaded cached results for query: {query}")
        return cached

    logger.info(f"Searching HF Hub: query='{query}', task='{task}', tag='{tag}'")
    try:
        filters = ModelFilter(task=task, tags=[tag] if tag else None)
        results = api.list_models(search=query, filter=filters, sort="downloads", limit=limit)
        models = [
            {
                "id": m.modelId,
                "downloads": m.downloads,
                "likes": m.likes,
                "tags": m.tags,
                "pipeline_tag": m.pipeline_tag,
                "lastModified": m.lastModified,
            }
            for m in results
        ]
        _cache_results(key, models)
        return models
    except Exception as e:
        logger.error(f"HF search failed: {e}")
        return []

def get_trending_models(limit: int = 5):
    """Shortcut to get trending models by download count."""
    return search_models(query="", task=None, limit=limit)

def get_available_tasks():
    """Return all supported HF pipeline task tags."""
    return list(ModelSearchArguments.pipeline_tag.__args__)

def get_model_card(model_id: str) -> Optional[str]:
    """Return the model card README."""
    try:
        info = model_info(model_id)
        return info.cardData.get("description", None)
    except Exception as e:
        logger.error(f"Failed to get model card for {model_id}: {e}")
        return None

def check_model_exists(model_id: str) -> bool:
    """Check if a model exists on HF Hub."""
    try:
        model_info(model_id)
        return True
    except RepositoryNotFoundError:
        return False
    except Exception as e:
        logger.error(f"Failed to validate model existence: {e}")
        return False

def download_snapshot(model_id: str, cache_dir: str = ".rayforge_cache/hf_models") -> str:
    """Downloads the full model snapshot and returns the path."""
    try:
        path = snapshot_download(model_id, cache_dir=cache_dir, local_files_only=False)
        logger.info(f"Downloaded snapshot to {path}")
        return path
    except Exception as e:
        logger.error(f"Failed to download snapshot: {e}")
        raise

def get_model_metadata(model_id: str) -> dict:
    """Fetch all available metadata from Hugging Face Hub."""
    try:
        info = model_info(model_id)
        return {
            "id": info.modelId,
            "author": info.author,
            "tags": info.tags,
            "downloads": info.downloads,
            "likes": info.likes,
            "pipeline_tag": info.pipeline_tag,
            "siblings": [s.rfilename for s in info.siblings],
            "cardData": info.cardData,
            "created_at": info.createdAt.isoformat(),
            "last_modified": info.lastModified.isoformat(),
        }
    except Exception as e:
        logger.error(f"Failed to fetch metadata: {e}")
        return {}

def upload_model_from_folder(
    folder_path: str,
    repo_id: str,
    token: str,
    private: bool = True,
    commit_message: str = "Initial RayForge upload",
):
    """
    Upload a model folder to HF Hub.
    Requires a valid access token and write permissions.
    """
    try:
        logger.info(f"Uploading folder '{folder_path}' to repo '{repo_id}'")
        upload_folder(
            folder_path=folder_path,
            repo_id=repo_id,
            token=token,
            private=private,
            commit_message=commit_message,
        )
        logger.info("Upload complete.")
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise
