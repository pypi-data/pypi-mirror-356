from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai.types.completion import Completion
from typing import Optional, List
from rayforge.utils.logger import get_logger
from dotenv import load_dotenv
load_dotenv()
import os
logger = get_logger()

# Initialize client with API key from env var
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    raise RuntimeError("OPENAI_API_KEY not found in environment.") from e

def list_models() -> List[str]:
    """Return all available OpenAI model IDs."""
    try:
        models = client.models.list()
        return [m.id for m in models.data]
    except Exception as e:
        logger.error(f"Model listing failed: {e}")
        return []

def chat_completion(prompt: str, model: str = "gpt-4", temperature: float = 0.7, max_tokens: int = 512) -> str:
    """Use OpenAI Chat Completions (GPT-4 / GPT-3.5)."""
    try:
        logger.info(f"Running chat completion with {model}")
        response: ChatCompletion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Chat completion failed: {e}")
        return f"Error: {e}"

def text_completion(prompt: str, model: str = "text-davinci-003", temperature: float = 0.7, max_tokens: int = 512) -> str:
    """Use legacy text completion models."""
    try:
        logger.info(f"Running text completion with {model}")
        response: Completion = client.completions.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error(f"Text completion failed: {e}")
        return f"Error: {e}"

def chat_stream(prompt: str, model: str = "gpt-4", temperature: float = 0.7):
    """Stream chat tokens from OpenAI API."""
    try:
        logger.info(f"Streaming chat from {model}")
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            stream=True
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        logger.error(f"Stream failed: {e}")
        yield f"Error: {e}"

def generate_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """Generate a dense embedding vector for given text."""
    try:
        logger.info(f"Generating embedding with {model}")
        embedding = client.embeddings.create(model=model, input=text)
        return embedding.data[0].embedding
    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        return []

def moderate_content(text: str) -> dict:
    """Run moderation check and return result dict."""
    try:
        logger.info("Running moderation check")
        result = client.moderations.create(input=text).results[0]
        return {
            "flagged": result.flagged,
            "categories": result.categories,
            "scores": result.category_scores
        }
    except Exception as e:
        logger.error(f"Moderation failed: {e}")
        return {"error": str(e)}

def tokens_used(prompt: str, model: str = "gpt-3.5-turbo") -> int:
    """Estimate token usage for a prompt using tiktoken."""
    try:
        import tiktoken
        enc = tiktoken.encoding_for_model(model)
        return len(enc.encode(prompt))
    except Exception as e:
        logger.error(f"Token counting failed: {e}")
        return -1
