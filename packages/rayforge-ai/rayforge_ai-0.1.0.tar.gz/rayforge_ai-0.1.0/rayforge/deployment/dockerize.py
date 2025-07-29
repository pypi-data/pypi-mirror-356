import subprocess
import os
from pathlib import Path

from rayforge.utils.logger import get_logger

logger = get_logger()

DOCKERFILE_TEMPLATE = """
# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \\
    pip install -r requirements.txt

CMD ["uvicorn", "rayforge.deployment.serve_fastapi:app", "--host", "0.0.0.0", "--port", "7860"]
"""

STREAMLIT_CMD = """
CMD ["streamlit", "run", "rayforge/deployment/gui_streamlit.py", "--server.port=8501", "--server.enableCORS=false"]
"""

def generate_dockerfile(use_streamlit: bool = False):
    dockerfile = Path("Dockerfile")
    if dockerfile.exists():
        logger.info("✅ Dockerfile already exists.")
        return

    logger.info("🛠 Generating Dockerfile...")
    content = DOCKERFILE_TEMPLATE
    if use_streamlit:
        content = content.replace('CMD ["uvicorn"', STREAMLIT_CMD.strip())

    dockerfile.write_text(content)
    logger.success("Dockerfile created.")

def build_docker_image(image_name: str = "rayforge:latest"):
    logger.info("🔨 Building Docker image...")
    try:
        subprocess.run(["docker", "build", "-t", image_name, "."], check=True)
        logger.success(f"✅ Docker image '{image_name}' built successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Docker build failed: {e}")
        raise

def run_docker_container(image_name: str = "rayforge:latest", port: int = 7860):
    logger.info("🚀 Running Docker container...")
    try:
        subprocess.run([
            "docker", "run", "--rm", "-p", f"{port}:{port}", image_name
        ], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to run container: {e}")
        raise

def dockerize(entry: str = "fastapi"):
    """
    Create Dockerfile and build image.
    entry: "fastapi" or "streamlit"
    """
    use_streamlit = (entry == "streamlit")
    generate_dockerfile(use_streamlit=use_streamlit)
    build_docker_image()
    run_docker_container(port=8501 if use_streamlit else 7860)
