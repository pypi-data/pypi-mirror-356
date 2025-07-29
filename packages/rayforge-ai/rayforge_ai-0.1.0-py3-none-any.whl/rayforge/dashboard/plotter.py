import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Dict, Optional
from pathlib import Path

from rayforge.utils.logger import get_logger

logger = get_logger()

def plot_metrics(metrics: Dict[str, float], title: str = "Model Metrics", save_path: Optional[str] = None):
    """
    Plot a bar chart of model metrics.
    Args:
        metrics (dict): {"accuracy": 0.85, "f1": 0.78}
        title (str): chart title
        save_path (str): optional file path to save
    """
    if not metrics:
        logger.warning("No metrics to plot.")
        return

    names = list(metrics.keys())
    values = list(metrics.values())

    plt.figure(figsize=(8, 5))
    sns.barplot(x=names, y=values, palette="pastel")
    plt.ylim(0, 1.0)
    plt.title(title)
    plt.ylabel("Score")
    plt.xlabel("Metric")
    for i, v in enumerate(values):
        plt.text(i, v + 0.01, f"{v:.2f}", ha="center")

    _render_or_save(save_path, title)

def plot_confusion_matrix(cm: np.ndarray, labels: List[str], title: str = "Confusion Matrix", save_path: Optional[str] = None):
    """
    Plot confusion matrix heatmap.
    Args:
        cm (np.ndarray): square confusion matrix
        labels (list): class names
    """
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    _render_or_save(save_path, title)

def plot_trend(metric_values: List[float], metric_name: str = "accuracy", save_path: Optional[str] = None):
    """
    Plot line graph showing metric change across runs.
    """
    plt.figure(figsize=(8, 5))
    sns.lineplot(x=list(range(1, len(metric_values) + 1)), y=metric_values, marker="o", color="teal")
    plt.title(f"{metric_name.title()} Over Time")
    plt.xlabel("Run")
    plt.ylabel(metric_name.title())
    plt.ylim(0, 1.0)
    for i, val in enumerate(metric_values):
        plt.text(i + 1, val + 0.01, f"{val:.2f}", ha="center")

    _render_or_save(save_path, metric_name)

# === Render helper ===

def _render_or_save(path: Optional[str], title: str):
    if path:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path, bbox_inches="tight")
        logger.success(f"Saved plot to {path}")
    else:
        plt.tight_layout()
        plt.show()
    plt.close()
