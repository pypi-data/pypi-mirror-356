from pathlib import Path
from typing import Optional, Union, Generator

from rayforge.models.hf_loader import load_hf_model
from rayforge.models.local_loader import load_local_model
from rayforge.core.model_runner import run_inference
from rayforge.core.metricizer import Metricizer
from rayforge.api.openai_api import chat_completion, chat_stream, generate_embedding
from rayforge.api.replicate_api import run_prediction, stream_prediction
from rayforge.utils.logger import get_logger

logger = get_logger()

class Forge:
    def __init__(self, cache_dir: str = "./.rayforge_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    # ========== Model Loaders ==========
    def pull(self, model_name: str, source: str = "huggingface") -> dict:
        """Pull model from supported sources."""
        logger.info(f"Pulling model '{model_name}' from source '{source}'")

        if source == "huggingface":
            return load_hf_model(model_name, self.cache_dir)

        elif source == "local":
            return load_local_model(model_name)

        elif source == "openai":
            logger.info(f"Using OpenAI model '{model_name}' (deferred)")
            return {
                "id": model_name,
                "model": "openai",
                "source": "openai",
                "task": "chat-completion"
            }

        elif source == "replicate":
            logger.info(f"Using Replicate model '{model_name}' (deferred)")
            owner, name = model_name.split("/")
            return {
                "id": model_name,
                "model": "replicate",
                "source": "replicate",
                "owner": owner,
                "name": name,
                "task": "custom"
            }

        else:
            raise ValueError(f"Unsupported source: {source}")

    # ========== Inference Dispatch ==========
    def run(
        self,
        model_info: dict,
        input_data: Union[str, dict],
        task: Optional[str] = None,
        stream: bool = False,
    ) -> Union[str, dict, Generator[str, None, None]]:
        """Run inference on any supported model."""
        task = task or model_info.get("task", "custom")
        source = model_info.get("source")

        if source == "huggingface" or source == "local":
            return run_inference(model_info, input_data, task)

        elif source == "openai":
            if stream:
                return chat_stream(input_data, model=model_info["id"])
            else:
                return chat_completion(input_data, model=model_info["id"])

        elif source == "replicate":
            if not isinstance(input_data, dict):
                raise TypeError("Replicate models require input_data to be a dict.")
            if stream:
                return stream_prediction(run_prediction(model_info["owner"], model_info["name"], input_data, stream=True)["id"])
            else:
                return run_prediction(model_info["owner"], model_info["name"], input_data)

        else:
            raise ValueError(f"Unknown source '{source}' for inference.")

    # ========== Metric Evaluation ==========
    def evaluate(self, model_info: dict, dataset_path: str, metric: str = "accuracy") -> float:
        """Evaluate model using supported metrics on labeled dataset."""
        logger.info(f"Evaluating model {model_info['id']} with metric '{metric}'")
        metricizer = Metricizer()
        return metricizer.evaluate(model_info, dataset_path, metric)

    # ========== Embedding (Optional) ==========
    def embed(self, text: str, model: str = "text-embedding-ada-002") -> list:
        """Generate embedding vector using OpenAI."""
        logger.info(f"Generating embedding for text input: {text[:50]}")
        return generate_embedding(text, model=model)

    # ========== Utilities ==========
    def describe(self, model_info: dict) -> dict:
        """Return basic summary of loaded model."""
        return {
            "id": model_info.get("id"),
            "source": model_info.get("source", "huggingface"),
            "task": model_info.get("task", "unknown"),
            "path": model_info.get("path", None),
            "format": model_info.get("format", "transformers" if model_info.get("tokenizer") else "custom")
        }
