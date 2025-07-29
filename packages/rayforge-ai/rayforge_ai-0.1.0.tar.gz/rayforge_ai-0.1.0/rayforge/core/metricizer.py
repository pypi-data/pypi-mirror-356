import csv
import json
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional

from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, mean_absolute_error
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer

from rayforge.core.model_runner import run_inference
from rayforge.utils.logger import get_logger

logger = get_logger()

class Metricizer:
    def __init__(self):
        self.supported_metrics = {
            "accuracy": self._accuracy,
            "f1": self._f1,
            "bleu": self._bleu,
            "rouge": self._rouge,
            "mse": self._mse,
            "mae": self._mae
        }

    def evaluate(self, model_info: dict, dataset_path: str, metric: str = "accuracy") -> float:
        """Evaluate a model on a dataset with the given metric."""
        metric = metric.lower()
        if metric not in self.supported_metrics:
            raise ValueError(f"Unsupported metric: {metric}. Supported: {list(self.supported_metrics)}")

        logger.info(f"Evaluating model '{model_info['id']}' with metric '{metric}'")
        data = self._load_dataset(dataset_path)
        preds, labels = [], []

        for input_text, expected_label in data:
            try:
                output = run_inference(model_info, input_text)
                prediction = self._extract_prediction(output)
                preds.append(prediction)
                labels.append(expected_label)
            except Exception as e:
                logger.warning(f"Error running prediction on input '{input_text}': {e}")
                preds.append("ERROR")
                labels.append(expected_label)

        return round(self.supported_metrics[metric](preds, labels), 4)

    def _load_dataset(self, path: str) -> List[Tuple[str, str]]:
        """Load input-label pairs from CSV or JSON file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Dataset file not found: {path}")

        logger.info(f"Loading dataset: {path}")
        data = []
        if path.suffix == ".csv":
            with open(path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "input" in row and "label" in row:
                        data.append((row["input"], row["label"]))
        elif path.suffix == ".json":
            with open(path) as f:
                items = json.load(f)
                for item in items:
                    if "input" in item and "label" in item:
                        data.append((item["input"], item["label"]))
        else:
            raise ValueError("Only .csv and .json formats are supported.")
        return data

    def _extract_prediction(self, output) -> str:
        """Normalize various output types to a comparable string."""
        if isinstance(output, str):
            return output.strip()

        elif isinstance(output, dict):
            if "label" in output:
                return output["label"]
            elif "generated_text" in output:
                return output["generated_text"]
            return json.dumps(output)

        elif isinstance(output, list):
            first = output[0]
            if isinstance(first, dict):
                return first.get("label") or first.get("generated_text") or str(first)
            return str(first)

        return str(output)

    # ========= Metric Implementations ==========

    def _accuracy(self, preds: List[str], labels: List[str]) -> float:
        return accuracy_score(labels, preds)

    def _f1(self, preds: List[str], labels: List[str]) -> float:
        return f1_score(labels, preds, average="weighted", zero_division=0)

    def _bleu(self, preds: List[str], labels: List[str]) -> float:
        return np.mean([
            sentence_bleu([ref.split()], hyp.split()) if isinstance(hyp, str) and isinstance(ref, str) else 0
            for hyp, ref in zip(preds, labels)
        ])

    def _rouge(self, preds: List[str], labels: List[str]) -> float:
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
        scores = [
            scorer.score(ref, hyp)["rougeL"].fmeasure
            if isinstance(hyp, str) and isinstance(ref, str) else 0
            for hyp, ref in zip(preds, labels)
        ]
        return np.mean(scores)

    def _mse(self, preds: List[str], labels: List[str]) -> float:
        preds_float = [float(p) if self._is_number(p) else 0 for p in preds]
        labels_float = [float(l) if self._is_number(l) else 0 for l in labels]
        return mean_squared_error(labels_float, preds_float)

    def _mae(self, preds: List[str], labels: List[str]) -> float:
        preds_float = [float(p) if self._is_number(p) else 0 for p in preds]
        labels_float = [float(l) if self._is_number(l) else 0 for l in labels]
        return mean_absolute_error(labels_float, preds_float)

    def _is_number(self, value) -> bool:
        try:
            float(value)
            return True
        except:
            return False
