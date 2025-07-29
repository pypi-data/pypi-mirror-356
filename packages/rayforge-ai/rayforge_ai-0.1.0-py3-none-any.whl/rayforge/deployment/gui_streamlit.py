import streamlit as st
from rayforge.core.forge_engine import Forge
from rayforge.utils.logger import get_logger

logger = get_logger()
forge = Forge()

# === Sidebar Configuration ===
st.set_page_config(page_title="RayForge UI", layout="centered")
st.sidebar.title("🔧 RayForge Control Panel")

model_id = st.sidebar.text_input("Model ID (Hugging Face, OpenAI, Replicate, local path)", value="distilbert-base-uncased-finetuned-sst-2-english")
source = st.sidebar.selectbox("Source", ["huggingface", "openai", "replicate", "local"])
use_stream = st.sidebar.toggle("Enable Streaming", value=False)
run_button = st.sidebar.button("🚀 Load Model")

# === Session State ===
if "model_info" not in st.session_state:
    st.session_state.model_info = None

# === Load Model ===
if run_button:
    try:
        st.session_state.model_info = forge.pull(model_id, source=source)
        st.success(f"Model '{model_id}' loaded successfully!")
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        logger.error(e)

# === Main Area ===
st.title("🤖 RayForge: Universal AI Model Runner")

if st.session_state.model_info:
    model_info = st.session_state.model_info

    st.markdown(f"**🧠 Model:** `{model_info['id']}`")
    st.markdown(f"**📦 Source:** `{model_info['source']}`")
    st.markdown(f"**🧪 Task:** `{model_info['task']}`")

    input_text = st.text_area("✍️ Enter input for your model:", height=150, placeholder="Type something like: 'Translate this to French'...")
    selected_task = st.text_input("Task override (optional)", value=model_info["task"])
    submit = st.button("🎯 Run Inference")

    if submit and input_text:
        try:
            with st.spinner("Running..."):
                if use_stream:
                    chunks = []
                    for token in forge.run(model_info, input_text, task=selected_task, stream=True):
                        chunks.append(token)
                        st.code("".join(chunks), language="text")
                else:
                    result = forge.run(model_info, input_text, task=selected_task)
                    st.success("✅ Inference completed!")
                    st.json(result if isinstance(result, dict) else {"output": result})
        except Exception as e:
            st.error(f"❌ Error: {e}")
            logger.error(e)
else:
    st.info("📌 Load a model using the sidebar to begin.")
