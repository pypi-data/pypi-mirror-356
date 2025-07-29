import logging
from rich.console import Console
from rich.logging import RichHandler

# Singleton console
_console = Console()

def get_logger(name="rayforge"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = RichHandler(console=_console, markup=True, show_path=False)
        formatter = logging.Formatter(
            "[%(name)s] [%(levelname)s] %(message)s", datefmt="[%X]"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

def init_logging(level="INFO"):
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(level=numeric_level, handlers=[
        RichHandler(console=_console, markup=True, show_path=False)
    ])
