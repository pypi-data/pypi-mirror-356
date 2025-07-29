import typer
from pathlib import Path
from typing import Optional

from rayforge.core.forge_engine import Forge
from rayforge.dashboard.plotter import plot_metrics
from rayforge.utils.io import load_dataset, save_predictions
from rayforge.deployment.serve_fastapi import serve_model
from rayforge.deployment.dockerize import dockerize
from rayforge.utils.logger import get_logger

app = typer.Typer(help="🧠 RayForge CLI: The universal AI model runner.", rich_markup_mode="markdown")
logger = get_logger()
forge = Forge()

# === Commands ===

@app.command("pull")
def pull_model(
    model_id: str = typer.Argument(..., help="Model name or path."),
    source: str = typer.Option("huggingface", help="Source: huggingface, openai, replicate, local")
):
    """🔍 Pull a model from HuggingFace, OpenAI, Replicate, or local path."""
    model = forge.pull(model_id, source)
    typer.secho(f"✅ Model '{model['id']}' loaded from {model['source']}.", fg=typer.colors.GREEN)

@app.command("run")
def run_model(
    model_id: str = typer.Argument(..., help="Model to use for inference."),
    input_text: Optional[str] = typer.Option(None, "--input", "-i", help="Single input text string."),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Path to CSV/JSON input-label dataset."),
    task: Optional[str] = typer.Option(None, "--task", help="Optional task override."),
    source: str = typer.Option("huggingface", "--source", "-s", help="Model source."),
    stream: bool = typer.Option(False, "--stream", "-S", help="Enable token streaming (OpenAI/Replicate only).")
):
    """⚙️ Run inference on text or dataset."""
    model = forge.pull(model_id, source)

    if input_text:
        typer.secho("🔁 Running inference on input text...", fg="cyan")
        result = forge.run(model, input_text, task=task, stream=stream)
        typer.echo(result)
    elif file:
        typer.secho(f"📂 Running batch inference on file: {file.name}", fg="cyan")
        data = load_dataset(file)
        preds = [(inp, label, forge.run(model, inp, task)) for inp, label in data]
        path = save_predictions(preds)
        typer.secho(f"✅ Saved predictions: {path}", fg="green")
    else:
        typer.secho("❌ Provide either `--input` or `--file`.", fg="red")

@app.command("serve")
def serve(
    model_id: str = typer.Argument(...),
    source: str = typer.Option("huggingface", help="Model source"),
    port: int = typer.Option(7860, help="Port to serve FastAPI app.")
):
    """🌐 Serve the model via FastAPI REST API."""
    model = forge.pull(model_id, source)
    serve_model(model, port)

@app.command("gui")
def launch_gui():
    """🧪 Launch the Streamlit UI for RayForge."""
    import subprocess
    subprocess.run(["streamlit", "run", "rayforge/deployment/gui_streamlit.py"])

@app.command("dockerize")
def dockerize_model(
    mode: str = typer.Option("fastapi", "--entry", help="Choose FastAPI or Streamlit.")
):
    """🐳 Build and optionally run Docker image."""
    dockerize(entry=mode)

@app.command("plot")
def plot_metric(
    metric: str = typer.Option("accuracy", help="Metric name to plot"),
    values: str = typer.Option("0.70,0.76,0.81,0.85", help="Comma-separated metric values")
):
    """📊 Plot metric trend over multiple runs."""
    vals = [float(v.strip()) for v in values.split(",")]
    plot_metrics({f"{metric}_{i}": val for i, val in enumerate(vals)}, title=f"{metric.title()} Over Time")

@app.command("metrics")
def show_metrics(
    model_id: str,
    source: str = typer.Option("huggingface")
):
    """📈 Print model task, metrics, and description."""
    model = forge.pull(model_id, source)
    info = forge.describe(model)
    for k, v in info.items():
        typer.echo(f"{k.title()}: {v}")

@app.command("version")
def version():
    """🔢 Print the current RayForge version."""
    typer.echo("🚀 RayForge v0.1.0")

# === Dev Tools ===

@app.command("test")
def run_tests():
    """🧪 Run unit tests."""
    typer.echo("Running pytest...")
    import subprocess
    subprocess.run(["pytest", "tests/"])

@app.command("lint")
def lint_code():
    """🧼 Lint the codebase with Ruff."""
    import subprocess
    subprocess.run(["ruff", "check", "rayforge", "--fix"])

if __name__ == "__main__":
    app()
