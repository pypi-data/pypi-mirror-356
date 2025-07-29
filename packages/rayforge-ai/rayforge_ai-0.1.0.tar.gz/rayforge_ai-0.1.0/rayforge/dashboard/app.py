import typer
from pathlib import Path
from typing import Optional

from rayforge.core.forge_engine import Forge
from rayforge.dashboard.plotter import plot_metrics
from rayforge.deployment.serve_fastapi import serve_model
from rayforge.deployment.gui_streamlit import st
from rayforge.deployment.dockerize import dockerize
from rayforge.utils.io import load_dataset, save_predictions

app = typer.Typer()
forge = Forge()

@app.command()
def pull(
    model_id: str,
    source: str = typer.Option("huggingface", help="Model source: huggingface, openai, replicate, local")
):
    """Pull and cache a model."""
    model_info = forge.pull(model_id, source)
    typer.secho(f"✅ Pulled model: {model_info['id']} from {model_info['source']}", fg=typer.colors.GREEN)

@app.command()
def run(
    model_id: str,
    input_text: Optional[str] = typer.Option(None, help="Single input string"),
    file: Optional[Path] = typer.Option(None, help="CSV/JSON file with input-label pairs"),
    task: Optional[str] = typer.Option(None, help="Optional task override"),
    source: str = typer.Option("huggingface", help="Source of model"),
    stream: bool = False
):
    """Run inference on input or dataset file."""
    model_info = forge.pull(model_id, source)
    if input_text:
        output = forge.run(model_info, input_text, task=task, stream=stream)
        typer.echo(output)
    elif file:
        data = load_dataset(file)
        predictions = []
        for inp, label in data:
            out = forge.run(model_info, inp, task=task)
            predictions.append((inp, label, out))
        out_path = save_predictions(predictions)
        typer.secho(f"✅ Predictions saved to: {out_path}", fg=typer.colors.GREEN)
    else:
        typer.secho("❌ Must provide either --input-text or --file", fg=typer.colors.RED)

@app.command()
def serve(
    model_id: str,
    source: str = typer.Option("huggingface"),
    port: int = 7860
):
    """Serve model with FastAPI"""
    model_info = forge.pull(model_id, source)
    serve_model(model_info, port)

@app.command()
def gui():
    """Launch Streamlit UI"""
    typer.echo("Launching Streamlit...")
    st.run("rayforge/deployment/gui_streamlit.py")

@app.command()
def docker(entry: str = "fastapi"):
    """Dockerize with either FastAPI or Streamlit"""
    dockerize(entry=entry)

@app.command()
def plot(metric: str = "accuracy"):
    """Plot example metric values across runs"""
    values = [0.72, 0.79, 0.83, 0.88]
    plot_metrics({f"{metric}_{i}": v for i, v in enumerate(values)}, title=f"{metric.title()} Across Runs")

if __name__ == "__main__":
    app()
