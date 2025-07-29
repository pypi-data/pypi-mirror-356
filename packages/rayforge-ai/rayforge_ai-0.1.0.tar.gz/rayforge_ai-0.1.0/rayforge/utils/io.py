import csv
import json
from pathlib import Path
from typing import List, Tuple, Optional, Union
from datetime import datetime

from rayforge.utils.logger import get_logger

logger = get_logger()

# === File Loader ===

def load_dataset(path: Union[str, Path]) -> List[Tuple[str, str]]:
    """
    Load a labeled dataset from CSV or JSON.
    Returns list of (input, label) tuples.
    """
    path = Path(path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    ext = path.suffix.lower()
    logger.info(f"Loading dataset: {path}")

    if ext == ".csv":
        return _load_csv(path)
    elif ext == ".json":
        return _load_json(path)
    else:
        raise ValueError("Unsupported dataset format. Must be .csv or .json.")

def _load_csv(path: Path) -> List[Tuple[str, str]]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = [(row["input"], row["label"]) for row in reader if "input" in row and "label" in row]
    logger.info(f"Loaded {len(data)} rows from CSV")
    return data

def _load_json(path: Path) -> List[Tuple[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        records = json.load(f)
    data = [(item["input"], item["label"]) for item in records if "input" in item and "label" in item]
    logger.info(f"Loaded {len(data)} rows from JSON")
    return data

# === Output Saver ===

def save_predictions(preds: List[Tuple[str, str, str]], out_path: str = None) -> str:
    """
    Save predictions as CSV. Each entry: (input, true_label, predicted_label)
    """
    out_dir = Path("rayforge_outputs")
    out_dir.mkdir(exist_ok=True)
    if not out_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = out_dir / f"predictions_{timestamp}.csv"
    else:
        out_path = Path(out_path)

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["input", "true_label", "predicted_label"])
        writer.writerows(preds)

    logger.info(f"Saved predictions to {out_path}")
    return str(out_path)

# === Generic Text/JSON Utilities ===

def read_text(path: str) -> str:
    path = Path(path)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_text(content: str, path: str):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Wrote text to {path}")

def save_json(obj: dict, path: str):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    logger.info(f"Saved JSON to {path}")

def load_json(path: str) -> dict:
    path = Path(path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# === Safe Path Utilities ===

def safe_path(name: str, ext: str = "txt", base_dir: str = "rayforge_outputs") -> Path:
    """
    Create a safe path with timestamp.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{name}_{timestamp}.{ext}"
    path = Path(base_dir) / safe_name
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
