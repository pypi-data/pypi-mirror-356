from transformers import pipeline
import torch
import numpy as np
import onnxruntime
import tensorflow as tf

from rayforge.utils.logger import get_logger

logger = get_logger()


def run_inference(model_info: dict, input_data: str, task: str = None):
    """
    Run inference based on the model_info structure.

    Args:
        model_info (dict): returned from pull()
        input_data (str): user input
        task (str, optional): override task

    Returns:
        str | dict | list: prediction output
    """
    task = task or model_info.get("task")
    fmt = model_info.get("format")
    source = model_info.get("source", "huggingface")

    if source == "huggingface":
        return _run_transformers_pipeline(model_info, input_data, task)

    elif fmt == "pytorch":
        return _run_pytorch_model(model_info["model"], input_data)

    elif fmt == "onnx":
        return _run_onnx_model(model_info["model"], input_data)

    elif fmt == "tensorflow":
        return _run_tf_model(model_info["model"], input_data)

    else:
        raise ValueError(f"Unsupported format: {fmt}")


# ==== Hugging Face Transformers ====

def _run_transformers_pipeline(model_info, input_text, task):
    try:
        pipe = pipeline(
            task=task,
            model=model_info["model"],
            tokenizer=model_info["tokenizer"],
            device=-1  # CPU for now
        )
        logger.info(f"Running HF pipeline: {task}")
        result = pipe(input_text)
        return result[0] if isinstance(result, list) and len(result) == 1 else result
    except Exception as e:
        logger.error(f"Pipeline inference failed: {e}")
        raise


# ==== PyTorch Models ====

def _run_pytorch_model(model, input_text):
    try:
        logger.info("Running PyTorch model (manual forward pass)")
        model.eval()
        with torch.no_grad():
            if hasattr(model, "forward_text"):
                return model.forward_text(input_text)
            elif isinstance(input_text, str):
                input_tensor = torch.tensor([ord(c) for c in input_text], dtype=torch.float32).unsqueeze(0)
                output = model(input_tensor)
                return output.tolist()
            else:
                raise TypeError("Unsupported input format for PyTorch model.")
    except Exception as e:
        logger.error(f"PyTorch inference failed: {e}")
        raise


# ==== ONNX Models ====

def _run_onnx_model(session: onnxruntime.InferenceSession, input_text):
    try:
        logger.info("Running ONNX model")
        input_name = session.get_inputs()[0].name
        input_array = np.array([[ord(c) for c in input_text]], dtype=np.float32)
        output = session.run(None, {input_name: input_array})
        return output[0].tolist()
    except Exception as e:
        logger.error(f"ONNX inference failed: {e}")
        raise


# ==== TensorFlow Models ====

def _run_tf_model(model, input_text):
    try:
        logger.info("Running TensorFlow model")
        input_tensor = tf.convert_to_tensor([[ord(c) for c in input_text]], dtype=tf.float32)
        output = model(input_tensor)
        if isinstance(output, (list, tuple)):
            return [o.numpy().tolist() for o in output]
        else:
            return output.numpy().tolist()
    except Exception as e:
        logger.error(f"TF inference failed: {e}")
        raise