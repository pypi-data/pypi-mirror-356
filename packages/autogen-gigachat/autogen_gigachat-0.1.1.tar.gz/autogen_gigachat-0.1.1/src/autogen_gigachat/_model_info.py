import logging
from typing import Dict

from autogen_core import EVENT_LOGGER_NAME, TRACE_LOGGER_NAME
from autogen_core.models import ModelFamily, ModelInfo

logger = logging.getLogger(EVENT_LOGGER_NAME)
trace_logger = logging.getLogger(TRACE_LOGGER_NAME)

_MODEL_INFO: Dict[str, ModelInfo] = {
    "GigaChat": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": False,
    },
    "GigaChat-preview": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": False,
    },
    "GigaChat-2": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": False,
    },
    "GigaChat-Pro": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": False,
    },
    "GigaChat-Pro-preview": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": False,
    },
    "GigaChat-2-Pro": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": False,
    },
    "GigaChat-Max": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": False,
    },
    "GigaChat-Max-preview": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": False,
    },
    "GigaChat-2-Max": {
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        "structured_output": True,
        "multiple_system_messages": False,
    }
}

_MODEL_TOKEN_LIMITS: Dict[str, int] = {
    "GigaChat": 32000,
    "GigaChat-preview": 128000,
    "GigaChat-2": 128000,
    "GigaChat-Pro": 32000,
    "GigaChat-Pro-preview": 128000,
    "GigaChat-2-Pro": 128000,
    "GigaChat-Max": 32000,
    "GigaChat-Max-preview": 128000,
    "GigaChat-2-Max": 128000,
}

GIGACHAT_API_BASE_URL = "https://gigachat.devices.sberbank.ru/api/v1/"


def resolve_model_class(model: str) -> str:
    return model.split(":")[0]

def get_info(model: str) -> ModelInfo:
    # If call it, that mean is that the config does not have custom model_info
    resolved_model = resolve_model_class(model)
    model_info: ModelInfo = _MODEL_INFO.get(
        resolved_model,
        {
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "family": "FAILED",
            "structured_output": False,
        },
    )
    if model_info.get("family") == "FAILED":
        raise ValueError("model_info is required when model name is not a valid Gigachat model")

    return model_info


def get_token_limit(model: str) -> int:
    resolved_model = resolve_model_class(model)
    return _MODEL_TOKEN_LIMITS[resolved_model]
