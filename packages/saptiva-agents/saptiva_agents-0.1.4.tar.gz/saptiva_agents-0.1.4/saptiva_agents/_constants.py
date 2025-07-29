import os

from dotenv import load_dotenv

load_dotenv()

SAPTIVA_BASE_URL = "https://api.saptiva.com/v1"
SAPTIVA_API_KEY = os.getenv('SAPTIVA_API_KEY', None)
LLAMA_MODEL = "llama3.3:70b"
GEMMA_MODEL = "gemma3:27b"
DEEPSEEK_R1_MODEL = "deepseek-r1:70b"
PHI4_MODEL = "huihui_ai/phi4-abliterated:14b-fp16"
QWEN_MODEL = "qwen2.5:72b-instruct"
DEEPSEEK_V3_MODEL = "deepseek-v3:671b"
TEXT_MODEL_LIST = ["llama3.3:70b", "qwen2.5:72b-instruct"]
MULTIMODAL_MODEL_LIST = ["gemma3:27b"]
DEFAULT_LANG = 'es'
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9
DEFAULT_SEED = 42
CONTENT_CHARS_MAX = 600
SYSTEM_PROMPT = (f"Eres un asistente de inteligencia artificial experto y servicial. Puedes llamar 'tools' "
                 f"para ayudar al usuario.")
DEFAULT_MODEL_INFO = {
    "vision": True,
    "function_calling": True,
    "json_output": False,
    "family": "unknown",
}

# Logs Constants
ROOT_LOGGER_NAME = "saptiva_agents.core"
"""str: Logger name used for structured event logging"""

EVENT_LOGGER_NAME = "saptiva_agents.core.events"
"""str: Logger name used for structured event logging"""

TRACE_LOGGER_NAME = "saptiva_agents.core.trace"
"""str: Logger name used for developer intended trace logging. The content and format of this log should not be depended upon."""

JSON_DATA_CONTENT_TYPE = "application/json"
"""JSON data content type"""

# TODO: what's the correct content type? There seems to be some disagreement over what it should be
PROTOBUF_DATA_CONTENT_TYPE = "application/x-protobuf"
"""Protobuf data content type"""