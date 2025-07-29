# ⚡ RayForge

**RayForge** is a universal AI model launcher: download, run, and evaluate models from Hugging Face, OpenAI, Replicate, or your own local code — all from one Python library, CLI, GUI, or API.

> Think of it as `transformers`, `openai`, `replicate`, and `wandb` combined — but fully pluggable and open.

---

## 🚀 Features

- 🔌 **Multi-provider support**: Hugging Face, OpenAI, Replicate, local models
- 🔁 **Auto-wrapper**: Standard interface for any model type
- 📈 **Metric logging**: Accuracy, BLEU, custom metrics, and visualizations
- 🧪 **Streamlit GUI**, 🧠 **FastAPI backend**, 💻 **Typer CLI**
- 📦 Ready for packaging, serving, and research

---

## 📦 Installation

```bash
pip install rayforge
````

Or from source:

```bash
git clone https://github.com/RaykenAI/rayforge.git
cd rayforge
pip install -e .
```

---

## 🧠 Usage

### CLI

```bash
rayforge pull --model-id gpt2 --source huggingface
rayforge run --model-id gpt2 --input-text "The future of AI is"
```

### Python

```python
from rayforge.core.forge_engine import Forge

forge = Forge()
model = forge.pull("gpt2", source="huggingface")
output = forge.run(model, "The future of AI is")
print(output)
```

### GUI

```bash
python main.py  # or set RAYFORGE_MODE=gui
```

### FastAPI

```bash
RAYFORGE_MODE=serve RAYFORGE_MODEL_ID=gpt2 RAYFORGE_MODEL_SOURCE=huggingface python main.py
```

---

## ⚙️ .env Configuration

**Create a `.env` file at your project root:**

```env
# Launch mode: cli, gui, serve
RAYFORGE_MODE=gui

# Default model to serve (for FastAPI mode)
RAYFORGE_MODEL_ID=gpt-4
RAYFORGE_MODEL_SOURCE=openai
RAYFORGE_PORT=7860

# 🔐 Required for OpenAI
OPENAI_API_KEY=sk-...
```

> ❗ `.env` is ignored in `.gitignore` to protect secrets. **You must create your own locally.**

---

## 🛠 Development Guide

### Run tests

```bash
pytest tests/
```

### Lint

```bash
ruff rayforge
```

### Build package

```bash
python -m build
```

---

## 🚀 Release via GitHub Actions

Push a tag like:

```bash
git tag v0.1.0
git push origin v0.1.0
```

> Automatically builds and uploads to PyPI.

---

## 📚 Folder Structure

```txt
rayforge/
├── core/             ← Forge engine and runners
├── models/           ← Wrappers, loaders
├── providers/        ← OpenAI, HF, Replicate APIs
├── utils/            ← Logging, IO, constants
├── dashboard/        ← Matplotlib/Seaborn plotting
├── deployment/       ← GUI + FastAPI servers
├── cli/              ← Typer CLI
└── tests/            ← Pytest modules
```

---

## 📜 License

MIT License © Rayken AI

---

## 🔗 Links

* PyPI: https://pypi.org/project/rayforge
* GitHub: [https://github.com/RaykenAI/rayforge](https://github.com/RaykenAI/rayforge)
