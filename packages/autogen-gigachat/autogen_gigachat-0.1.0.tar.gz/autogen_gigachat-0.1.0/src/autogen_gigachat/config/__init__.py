from typing import Dict, List, Optional, Union

from autogen_core.models._model_client import ModelInfo, ModelCapabilities
from pydantic import BaseModel, SecretStr
from typing_extensions import Required, TypedDict

class JSONSchema(TypedDict, total=False):
    name: Required[str]
    """The name of the response format. Must be a-z, A-Z, 0-9, or contain underscores and
    dashes, with a maximum length of 64."""
    description: str
    """A description of what the response format is for, used by the model to determine
    how to respond in the format."""
    schema: Dict[str, object]
    """The schema for the response format, described as a JSON Schema object."""
    strict: Optional[bool]
    """Whether to enable strict schema adherence when generating the output.
    If set to true, the model will always follow the exact schema defined in the
    `schema` field. Only a subset of JSON Schema is supported when `strict` is
    `true`. To learn more, read the
    [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs).
    """

class CreateArguments(TypedDict, total=False):
    temperature: Optional[float]
    top_p: Optional[float]
    n: Optional[int]
    stream: Optional[bool]
    max_tokens: Optional[int]
    repetition_penalty: Optional[float]
    update_interval: Optional[float]
    flags: Optional[List[str]]
    is_stateful: Optional[bool]
    storage_limit: Optional[int]

class GigachatClientConfiguration(CreateArguments, total=False):
    model: str
    api_key: Optional[str]
    base_url: Optional[str]
    auth_url: Optional[str]
    scope: Optional[str]
    profanity_check: Optional[bool]
    timeout: Union[float, None]
    max_retries: int
    model_capabilities: ModelCapabilities  # type: ignore
    model_info: ModelInfo
    default_headers: Dict[str, str] | None
    
    verify_ssl_certs: Optional[bool]
    ca_bundle_file: Optional[str] = None
    cert_file: Optional[str] = None
    key_file: Optional[str] = None
    key_file_password: Optional[str] = None
    
    verbose: Optional[bool]

# Pydantic equivalents of the above TypedDicts
class CreateArgumentsConfigModel(BaseModel):
    temperature: float | None = None
    top_p: float | None = None
    n: int | None = None
    stream: bool | None = None
    max_tokens: int | None = None
    repetition_penalty: float | None = None
    update_interval: float | None = None
    flags: List[str] | None = None
    is_stateful: bool | None = None
    storage_limit: int | None = None

class GigachatClientConfigurationConfigModel(CreateArgumentsConfigModel):
    model: str
    api_key: SecretStr | None = None
    base_url: str | None = None
    auth_url: str | None = None
    scope: str | None = None
    profanity_check: bool | None = None
    timeout: float | None = None
    max_retries: int | None = None
    model_capabilities: ModelCapabilities | None = None  # type: ignore
    model_info: ModelInfo | None = None
    default_headers: Dict[str, str] | None = None
    
    verify_ssl_certs: bool | None = None
    ca_bundle_file:  str | None = None
    cert_file: str | None = None
    key_file: str | None = None
    key_file_password: str | None = None
    
    verbose: bool | None = None
