from setuptools import setup, find_packages
import pathlib

root = pathlib.Path(__file__).parent
long_description = (root / "README.md").read_text(encoding="utf-8")

setup(
    name="rayforge-ai",
    version="0.1.0",
    description="Universal Python framework to download, run, and metricize AI models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rayken AI",
    author_email="founder@rayken.ai",
    url="https://github.com/rayken-ai/rayforge",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=[
        "transformers>=4.38.0",
        "torch>=2.2.0",
        "huggingface_hub>=0.20.0",
        "openai>=1.24.0",
        "replicate>=0.25.0",
        "fastapi>=0.110.0",
        "uvicorn[standard]>=0.29.0",
        "streamlit>=1.34.0",
        "typer[all]>=0.12.3",
        "python-dotenv>=1.0.1",
        "pandas>=2.2.0",
        "scikit-learn>=1.4.0",
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
        "requests>=2.31.0",
        "tqdm>=4.66.0",
        "aiohttp>=3.9.0",
        "pydantic>=2.6.0",
        "tabulate>=0.9.0"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "rayforge=rayforge.cli.cli:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": ["pytest", "ruff"],
    },
    license="MIT",
    zip_safe=False,
)
