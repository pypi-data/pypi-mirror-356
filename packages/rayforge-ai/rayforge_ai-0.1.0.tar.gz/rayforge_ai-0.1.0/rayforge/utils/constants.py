from enum import Enum

# === Supported Model Sources ===
MODEL_SOURCES = ["huggingface", "local", "openai", "replicate"]

# === Supported File Extensions ===
MODEL_EXTENSIONS = {
    ".pt": "pytorch",
    ".onnx": "onnx",
    ".pb": "tensorflow"
}

# === Supported HF Tasks ===
HF_SUPPORTED_TASKS = [
    "text-classification",
    "token-classification",
    "text-generation",
    "summarization",
    "translation",
    "question-answering",
]

# === Default Fallbacks ===
DEFAULT_TASK = "text-classification"
DEFAULT_HF_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo"
DEFAULT_REPLICATE_MODEL = "replicate/codegen-2"

# === Metric Mapping ===
TASK_METRIC_MAP = {
    "text-classification": ["accuracy", "f1"],
    "summarization": ["rouge"],
    "translation": ["bleu"],
    "generation": ["bleu", "rouge"],
    "regression": ["mse", "mae"]
}

# === Standard Metrics ===
SUPPORTED_METRICS = ["accuracy", "f1", "bleu", "rouge", "mse", "mae"]

# === Inference Types ===
class ModelFormat(str, Enum):
    TRANSFORMERS = "transformers"
    PYTORCH = "pytorch"
    ONNX = "onnx"
    TENSORFLOW = "tensorflow"
    OPENAI = "openai"
    REPLICATE = "replicate"

# === Optional: Color tags for CLI/debug
LABEL_COLORS = {
    "huggingface": "cyan",
    "local": "green",
    "openai": "magenta",
    "replicate": "yellow",
    "error": "red",
    "success": "green"
}
