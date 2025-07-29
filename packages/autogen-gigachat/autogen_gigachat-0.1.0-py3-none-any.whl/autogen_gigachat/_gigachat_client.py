import asyncio
import inspect
import json
import logging
import math
import os
import re
import uuid
import warnings
from asyncio import Task
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Type,
    Union,
    cast,
)

from autogen_core import (
    EVENT_LOGGER_NAME,
    TRACE_LOGGER_NAME,
    CancellationToken,
    Component,
    FunctionCall,
    Image,
)
from autogen_core.logging import LLMCallEvent, LLMStreamEndEvent, LLMStreamStartEvent
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    ChatCompletionTokenLogprob,
    CreateResult,
    LLMMessage,
    ModelCapabilities,
    ModelInfo,
    RequestUsage,
    SystemMessage,
    UserMessage,
    validate_model_info,
)
from autogen_core.models._types import FinishReasons, FunctionExecutionResultMessage
from autogen_core.tools import Tool, ToolSchema
from gigachat import GigaChat
from gigachat.models import (
    Chat,
    Function,
    FunctionCall as GigaFunctionCall,
    FunctionParameters,
    Messages,
    MessagesRole,
    Storage,
    ChatCompletion,
    ChatCompletionChunk,
)

from gigachat.settings import Settings
from gigachat.settings import SCOPE

from pydantic import BaseModel, SecretStr
from typing_extensions import Self, Unpack

from . import _model_info

from .config import (
    GigachatClientConfiguration,
    GigachatClientConfigurationConfigModel,
)

logger = logging.getLogger(EVENT_LOGGER_NAME)
trace_logger = logging.getLogger(TRACE_LOGGER_NAME)

gigachat_init_kwargs = set(inspect.getfullargspec(Settings).kwonlyargs)

create_kwargs = set(Settings.__annotations__.keys()) | set(
    ("timeout", "stream")
)

# Only single choice allowed
disallowed_create_args = set(["stream", "messages", "function_call", "functions", "n"])
required_create_args: Set[str] = set(["model"])

USER_AGENT_HEADER_NAME = "User-Agent"

def _gigachat_client_from_config(config: Mapping[str, Any]) -> GigaChat:
    gigachat_config = {k: v for k, v in config.items() if k in gigachat_init_kwargs}
    return GigaChat(**gigachat_config)

def _create_args_from_config(config: Mapping[str, Any]) -> Dict[str, Any]:
    create_args = {k: v for k, v in config.items() if k in create_kwargs}
    create_args_keys = set(create_args.keys())
    if not required_create_args.issubset(create_args_keys):
        raise ValueError(f"Required create args are missing: {required_create_args - create_args_keys}")
    if disallowed_create_args.intersection(create_args_keys):
        raise ValueError(f"Disallowed create args are present: {disallowed_create_args.intersection(create_args_keys)}")
    return create_args

def system_message_to_gigachat(message: SystemMessage) -> Messages:
    return Messages(
        role=MessagesRole.SYSTEM,
        content=message.content,
        )

# TODO: Handle attachments
def user_message_to_gigachat(message: UserMessage) -> Sequence[Messages]:
    if isinstance(message.content, str):
        return Messages(
            role=MessagesRole.USER,
            content=message.content,
        )
    else:
        raise ValueError(f"Unknown content type")

def assistant_message_to_gigachat(message: AssistantMessage) -> Sequence[Messages]:
    if isinstance(message.content, list):
        return [
            Messages(
                role=MessagesRole.ASSISTANT,
                function_call=GigaFunctionCall(name=x.name, arguments=json.loads(x.arguments))
                ) for x in message.content
            ]
    else:
        return Messages(
            content=message.content,
            role=MessagesRole.ASSISTANT,
        )

def function_result_to_json(content: str) -> str:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return json.dumps(content, ensure_ascii=False)

def tool_message_to_gigachat(message: FunctionExecutionResultMessage) -> Sequence[Messages]:
    return [Messages(content=function_result_to_json(x.content), role=MessagesRole.FUNCTION, name=x.name) for x in message.content]


def to_gigachat_type(message: LLMMessage) -> Sequence[Messages]:
    if isinstance(message, SystemMessage):
        return [system_message_to_gigachat(message)]
    elif isinstance(message, UserMessage):
        return user_message_to_gigachat(message)
    elif isinstance(message, AssistantMessage):
        return [assistant_message_to_gigachat(message)]
    else:
        return tool_message_to_gigachat(message)

def convert_tools(
    tools: Sequence[Tool | ToolSchema],
) -> List[Function]:
    result: List[Function] = []
    for tool in tools:
        if isinstance(tool, Tool):
            tool_schema = tool.schema
        else:
            assert isinstance(tool, dict)
            tool_schema = tool
        
        result.append(
            Function(
                name=tool_schema["name"],
                description=tool_schema.get("description"),
                parameters=(
                        cast(FunctionParameters, tool_schema["parameters"]) if "parameters" in tool_schema else {}
                        ),
            )
        )
    # Check if all tools have valid names.
    for tool_param in result:
        assert_valid_name(tool_param.name)
    
    return result

def normalize_stop_reason(stop_reason: str | None) -> FinishReasons:
    if stop_reason is None:
        return "unknown"

    # Convert to lower case
    stop_reason = stop_reason.lower()

    KNOWN_STOP_MAPPINGS: Dict[str, FinishReasons] = {
        "stop": "stop",
        "length": "length",
        "function_call": "function_calls",
        "blacklist": "content_filter",
        "error": "stop",
    }

    return KNOWN_STOP_MAPPINGS.get(stop_reason, "unknown")

def pass_token_to_gigachat(config_args: Dict[str,object], token: str) -> None:
        config_args["credentials"] = None
        config_args["user"] = None
        config_args["password"] = None
        if token.startswith("giga-user-"):
            user, password = token.replace("giga-user-", "", 1).split(":")
            config_args["user"] = user
            config_args["password"] = password
        elif token.startswith("giga-cred-"):
            parts = token.replace("giga-cred-", "", 1).split(":")
            config_args["credentials"] = parts[0]
            config_args["scope"] = parts[1] if len(parts) > 1 else SCOPE
        elif token.startswith("giga-auth-"):
            config_args["access_token"] = token.replace("giga-auth-", "", 1)

def assert_valid_name(name: str) -> str:
    """
    Ensure that configured names are valid, raises ValueError if not.

    For munging LLM responses use _normalize_name to ensure LLM specified names don't break the API.
    """
    if not re.match(r"^[a-zA-Z0-9_-]+$", name):
        raise ValueError(f"Invalid name: {name}. Only letters, numbers, '_' and '-' are allowed.")
    if len(name) > 64:
        raise ValueError(f"Invalid name: {name}. Name must be less than 64 characters.")
    return name

def normalize_name(name: str) -> str:
    """
    LLMs sometimes ask functions while ignoring their own format requirements, this function should be used to replace invalid characters with "_".

    Prefer _assert_valid_name for validating user configuration or input
    """
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name)[:64]

def _add_usage(usage1: RequestUsage, usage2: RequestUsage) -> RequestUsage:
    return RequestUsage(
        prompt_tokens=usage1.prompt_tokens + usage2.prompt_tokens,
        completion_tokens=usage1.completion_tokens + usage2.completion_tokens,
    )

def flatten(obj):
    if isinstance(obj, list):
        for item in obj:
            yield from flatten(item)
    else:
        yield obj

class GigachatChatCompletionClient(ChatCompletionClient, Component[GigachatClientConfigurationConfigModel]):
    
    component_type = "model"
    component_config_schema = GigachatClientConfigurationConfigModel
    component_provider_override = "autogen_gigachat.GigachatChatCompletionClient"
    
    def __init__(self, **kwargs: Unpack[GigachatClientConfiguration]):
        if "model" not in kwargs:
            raise ValueError("model is required for GigachatChatCompletionClient")

        self._raw_config: Dict[str, Any] = dict(kwargs).copy()
        copied_args = dict(kwargs).copy()
        
        # TODO: Only for tests
        copied_args["verify_ssl_certs"]=False
        copied_args["verbose"]=True
        
        model_info: Optional[ModelInfo] = None
        if "model_info" in kwargs:
            model_info = kwargs["model_info"]
            del copied_args["model_info"]
        
        if "api_key" not in copied_args and "GIGACHAT_API_KEY" in os.environ:
                copied_args["api_key"] = os.environ["GIGACHAT_API_KEY"]
        
        if "api_key" in copied_args:
            pass_token_to_gigachat(config_args=copied_args, token=copied_args["api_key"])
        
        if model_info is None:
            try:
                self._model_info = _model_info.get_info(copied_args["model"])
            except KeyError as err:
                raise ValueError("model_info is required when model name is not a valid Gigachat model") from err
        elif model_info is not None:
            self._model_info = model_info

        # Validate model_info, check if all required fields are present
        validate_model_info(self._model_info)

        self._resolved_model: Optional[str] = None
        if "model" in kwargs:
            self._resolved_model = _model_info.resolve_model_class(kwargs["model"])

        if (
            not self._model_info["json_output"]
            and "response_format" in kwargs
            and (
                isinstance(kwargs["response_format"], dict)
                and kwargs["response_format"]["type"] == "json_object"
            )
        ):
            raise ValueError("Model does not support JSON output.")
        
        self._create_args = _create_args_from_config(copied_args)
        self._client = _gigachat_client_from_config(self._create_args)
        
        # TODO: default_headers to _client.context
        
        self._total_usage = RequestUsage(prompt_tokens=0, completion_tokens=0)
        self._actual_usage = RequestUsage(prompt_tokens=0, completion_tokens=0)
    
    @classmethod
    def create_from_config(cls, config: Dict[str, Any]) -> ChatCompletionClient:
        return GigachatChatCompletionClient(**config)
    
    def _rstrip_last_assistant_message(self, messages: Sequence[LLMMessage]) -> Sequence[LLMMessage]:
        """
        Remove the last assistant message if it is empty.
        """
        if isinstance(messages[-1], AssistantMessage):
            if isinstance(messages[-1].content, str):
                messages[-1].content = messages[-1].content.rstrip()

        return messages
    
    def _process_create_args(
        self,
        messages: Sequence[LLMMessage],
        tools: Sequence[Tool | ToolSchema],
        json_output: Optional[bool | type[BaseModel]],
        extra_create_args: Mapping[str, Any],
    ) -> Chat:
        # Make sure all extra_create_args are valid
        extra_create_args_keys = set(extra_create_args.keys())
        if not create_kwargs.issuperset(extra_create_args_keys):
            raise ValueError(f"Extra create args are invalid: {extra_create_args_keys - create_kwargs}")

        # Copy the create args and overwrite anything in extra_create_args
        create_args = self._create_args.copy()
        create_args.update(extra_create_args)

        if not self.model_info.get("multiple_system_messages", False):
            # Some models accept only one system message(or, it will read only the last one)
            # So, merge system messages into one (if multiple and continuous)
            system_message_content = ""
            _messages: List[LLMMessage] = []
            _first_system_message_idx = -1
            _last_system_message_idx = -1
            # Index of the first system message for adding the merged system message at the correct position
            for idx, message in enumerate(messages):
                if isinstance(message, SystemMessage):
                    if _first_system_message_idx == -1:
                        _first_system_message_idx = idx
                    elif _last_system_message_idx + 1 != idx:
                        # That case, system message is not continuous
                        # Merge system messages only continues system messages
                        raise ValueError(
                            "Multiple and Not continuous system messages are not supported if model_info['multiple_system_messages'] is False"
                        )
                    system_message_content += message.content + "\n"
                    _last_system_message_idx = idx
                else:
                    _messages.append(message)
            system_message_content = system_message_content.rstrip()
            if system_message_content != "":
                system_message = SystemMessage(content=system_message_content)
                _messages.insert(_first_system_message_idx, system_message)
            messages = _messages

        if self.model_info["function_calling"] is False and len(tools) > 0:
            raise ValueError("Model does not support function calling")
        
        gigachat_messages_nested = [to_gigachat_type(message) for message in messages]
        
        gigachat_messages = flatten(gigachat_messages_nested)
        
        chatSettings = Chat(
            model=create_args["model"],
            messages = gigachat_messages,
            # TODO: function_call if single tool
            function_call="auto" if tools and len(tools) > 0 else None,
            # TODO: If len(tools) > 6?
            functions= convert_tools(tools) if tools and len(tools) > 0 else None,
            temperature=create_args.get("temperature"),
            top_p=create_args.get("top_p"),
            n = create_args.get("n"),
            stream=create_args.get("stream"),
            max_tokens=create_args.get("max_tokens"),
            repetition_penalty=create_args.get("repetition_penalty"),
            update_interval=create_args.get("update_interval"),
            profanity_check=create_args.get("profanity_check"),
            flags=create_args.get("flags")
            )
        
        if create_args.get("is_stateful",False):
            chatSettings.storage = Storage(
                is_stateful=True,
                limit=create_args.get("storage_limit"),
                )
        
        return chatSettings
    
    async def create(
        self,
        messages: Sequence[LLMMessage],
        *,
        tools: Sequence[Tool | ToolSchema] = [],
        json_output: Optional[bool | type[BaseModel]] = None,
        extra_create_args: Mapping[str, Any] = {},
        cancellation_token: Optional[CancellationToken] = None,
    ) -> CreateResult:
        
        create_params: Chat  = self._process_create_args(
            messages,
            tools,
            json_output,
            extra_create_args,
        )
        
        future = asyncio.ensure_future(
            self._client.achat(create_params)
        )
        
        if cancellation_token is not None:
            cancellation_token.link_future(future)
        result: ChatCompletion = await future
        
        usage = RequestUsage(
            # TODO backup token counting
            prompt_tokens=result.usage.prompt_tokens if result.usage.prompt_tokens is not None else 0,
            completion_tokens=(result.usage.completion_tokens if result.usage.completion_tokens is not None else 0),
        )

        logger.info(
            LLMCallEvent(
                messages=[m.dict() for m in create_params.messages],
                response=result.dict(),
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
            )
        )
        
        if self._resolved_model is not None:
            if self._resolved_model != result.model.split(":")[0]:
                warnings.warn(
                    f"Resolved model mismatch: {self._resolved_model} != {result.model}. "
                    "Model mapping in autogen_ext.models.openai may be incorrect.",
                    stacklevel=2,
                )
                
        # Limited to a single choice currently.
        choice = result.choices[0]

            
        # Detect whether it is a function call or not.
        content: Union[str, List[FunctionCall]]
        thought: str | None = None
        if choice.message.function_call is not None:
            if choice.finish_reason != "function_call":
                warnings.warn(
                    f"Finish reason mismatch: {choice.finish_reason} != function_call "
                    "when function_call are present. Finish reason may not be accurate. "
                    "This may be due to the API used that is not returning the correct finish reason.",
                    stacklevel=2,
                )
            if choice.message.content is not None and choice.message.content != "":
                # Put the content in the thought field.
                thought = choice.message.content
            content = []

            if not isinstance(choice.message.function_call.arguments, str):
                warnings.warn(
                    f"Tool call function arguments field is not a string: {choice.message.function_call.arguments}."
                    "This is unexpected and may due to the API used not returning the correct type. "
                    "Attempting to convert it to string.",
                    stacklevel=2,
                )
                if isinstance(choice.message.function_call.arguments, dict):
                    choice.message.function_call.arguments = json.dumps(choice.message.function_call.arguments)
            content.append(
                FunctionCall(
                    id=f"call_{uuid.uuid4()}",
                    arguments=choice.message.function_call.arguments,
                    name=normalize_name(choice.message.function_call.name),
                )
            )
            finish_reason = "function_calls"
        else:
            # if not tool_calls, then it is a text response and we populate the content and thought fields.
            finish_reason = choice.finish_reason
            content = choice.message.content or ""
        
        response = CreateResult(
            finish_reason=normalize_stop_reason(finish_reason),
            content=content,
            usage=usage,
            cached=False,
            logprobs=None,
            thought=thought,
        )

        self._total_usage = _add_usage(self._total_usage, usage)
        self._actual_usage = _add_usage(self._actual_usage, usage)

        return response
    
    async def create_stream(
        self,
        messages: Sequence[LLMMessage],
        *,
        tools: Sequence[Tool | ToolSchema] = [],
        json_output: Optional[bool | type[BaseModel]] = None,
        extra_create_args: Mapping[str, Any] = {},
        cancellation_token: Optional[CancellationToken] = None,
        max_consecutive_empty_chunk_tolerance: int = 0,
        include_usage: Optional[bool] = None,
    ) -> AsyncGenerator[Union[str, CreateResult], None]:
        create_params = self._process_create_args(
            messages,
            tools,
            json_output,
            extra_create_args,
        )
        
        create_params.stream = True
        
        chunks = self._client.astream(create_params)

        # Prepare data to process streaming chunks.
        chunk: ChatCompletionChunk | None = None
        stop_reason = None
        maybe_model = None
        content_deltas: List[str] = []
        thought_deltas: List[str] = []
        full_tool_calls: Dict[int, FunctionCall] = {}
        logprobs: Optional[List[ChatCompletionTokenLogprob]] = None

        empty_chunk_warning_has_been_issued: bool = False
        empty_chunk_warning_threshold: int = 10
        empty_chunk_count = 0
        first_chunk = True
        is_reasoning = False

        # Process the stream of chunks.
        async for chunk in chunks:
            if first_chunk:
                first_chunk = False
                # Emit the start event.
                logger.info(
                    LLMStreamStartEvent(
                        messages=cast(List[Dict[str, Any]], create_params.messages),
                    )
                )

            # Set the model from the latest chunk.
            maybe_model = chunk.model

            # Empty chunks has been observed when the endpoint is under heavy load.
            #  https://github.com/microsoft/autogen/issues/4213
            if len(chunk.choices) == 0:
                empty_chunk_count += 1
                if not empty_chunk_warning_has_been_issued and empty_chunk_count >= empty_chunk_warning_threshold:
                    empty_chunk_warning_has_been_issued = True
                    warnings.warn(
                        f"Received more than {empty_chunk_warning_threshold} consecutive empty chunks. Empty chunks are being ignored.",
                        stacklevel=2,
                    )
                continue
            else:
                empty_chunk_count = 0

            if len(chunk.choices) > 1:
                # This is a multi-choice chunk, we need to warn the user.
                warnings.warn(
                    f"Received a chunk with {len(chunk.choices)} choices. Only the first choice will be used.",
                    UserWarning,
                    stacklevel=2,
                )

            # Set the choice to the first choice in the chunk.
            choice = chunk.choices[0]

            # for liteLLM chunk usage, do the following hack keeping the pervious chunk.stop_reason (if set).
            # set the stop_reason for the usage chunk to the prior stop_reason
            stop_reason = choice.finish_reason if chunk.usage is None and stop_reason is None else stop_reason
            maybe_model = chunk.model

            # First try get content
            if choice.delta.content:
                content_deltas.append(choice.delta.content)
                if len(choice.delta.content) > 0:
                    yield choice.delta.content
                # NOTE: for OpenAI, tool_calls and content are mutually exclusive it seems, so we can skip the rest of the loop.
                # However, this may not be the case for other APIs -- we should expect this may need to be updated.
                continue
            # Otherwise, get tool calls
            if choice.delta.function_call is not None:
                tool_call_chunk = choice.delta
                idx = choice.index
                if idx not in full_tool_calls:
                    # We ignore the type hint here because we want to fill in type when the delta provides it
                    full_tool_calls[idx] = FunctionCall(id="", arguments="", name="")

                    full_tool_calls[idx].id += f"call_{uuid.uuid4()}"

                if tool_call_chunk.function_call is not None:
                    if tool_call_chunk.function_call.name is not None:
                        full_tool_calls[idx].name += tool_call_chunk.function_call.name
                    if tool_call_chunk.function_call.arguments is not None:
                        full_tool_calls[idx].arguments += tool_call_chunk.function_call.arguments

        # Finalize the CreateResult.

        # We need to get the model from the last chunk, if available.
        model = maybe_model or create_params.create_args["model"]

        # Because the usage chunk is not guaranteed to be the last chunk, we need to check if it is available.
        if chunk and chunk.usage:
            prompt_tokens = chunk.usage.prompt_tokens
            completion_tokens = chunk.usage.completion_tokens
        else:
            prompt_tokens = 0
            completion_tokens = 0
        usage = RequestUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
        )

        # Detect whether it is a function call or just text.
        content: Union[str, List[FunctionCall]]
        thought: str | None = None
        # Determine the content and thought based on what was collected
        if full_tool_calls:
            # This is a tool call response
            content = list(full_tool_calls.values())
            if content_deltas:
                # Store any text alongside tool calls as thoughts
                thought = "".join(content_deltas)
        else:
            # This is a text response (possibly with thoughts)
            if content_deltas:
                content = "".join(content_deltas)
            else:
                warnings.warn(
                    "No text content or tool calls are available. Model returned empty result.",
                    stacklevel=2,
                )
                content = ""

            # Set thoughts if we have any reasoning content.
            if thought_deltas:
                thought = "".join(thought_deltas).lstrip("<think>").rstrip("</think>")

        # Create the result.
        result = CreateResult(
            finish_reason=normalize_stop_reason(stop_reason),
            content=content,
            usage=usage,
            cached=False,
            logprobs=logprobs,
            thought=thought,
        )

        # Log the end of the stream.
        logger.info(
            LLMStreamEndEvent(
                response=result.model_dump(),
                prompt_tokens=usage.prompt_tokens,
                completion_tokens=usage.completion_tokens,
            )
        )

        # Update the total usage.
        self._total_usage = _add_usage(self._total_usage, usage)
        self._actual_usage = _add_usage(self._actual_usage, usage)

        # Yield the CreateResult.
        yield result

    async def close(self) -> None:
        await self._client.close()
    
    def actual_usage(self) -> RequestUsage:
        return self._actual_usage

    def total_usage(self) -> RequestUsage:
        return self._total_usage

    def count_tokens(self, messages: Sequence[LLMMessage], *, tools: Sequence[Tool | ToolSchema] = []) -> int:
        return 
    
    def remaining_tokens(self, messages: Sequence[LLMMessage], *, tools: Sequence[Tool | ToolSchema] = []) -> int:
        token_limit = _model_info.get_token_limit(self._create_args["model"])
        return token_limit - self.count_tokens(messages, tools=tools)
    
    @property
    def capabilities(self) -> ModelCapabilities:  # type: ignore
        warnings.warn(
            "capabilities is deprecated, use model_info instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._model_info

    @property
    def model_info(self) -> ModelInfo:
        return self._model_info
    
    def __getstate__(self) -> Dict[str, Any]:
        state = self.__dict__.copy()
        state["_client"] = None
        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        self.__dict__.update(state)
        self._client = _gigachat_client_from_config(state["_raw_config"])

    def _to_config(self) -> GigachatClientConfigurationConfigModel:
        copied_config = self._raw_config.copy()
        return GigachatClientConfigurationConfigModel(**copied_config)

    @classmethod
    def _from_config(cls, config: GigachatClientConfigurationConfigModel) -> Self:
        copied_config = config.model_copy().model_dump(exclude_none=True)

        # Handle api_key as SecretStr
        if "api_key" in copied_config and isinstance(config.api_key, SecretStr):
            copied_config["api_key"] = config.api_key.get_secret_value()

        return cls(**copied_config)
    