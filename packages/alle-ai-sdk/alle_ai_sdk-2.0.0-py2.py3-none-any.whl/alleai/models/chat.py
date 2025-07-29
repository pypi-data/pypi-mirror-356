# alleai/models/chat.py
from typing import List, Dict, Optional, TypedDict, Literal, Any
from ..core.exceptions import InvalidRequestError
from ..core.utils import handle_errors
from .base import BaseModel


# TypedDict definitions for nested structures
class Content(TypedDict):
    type: Literal["text", "audio_url", "image_url", "video_url"]
    text: Optional[str]
    url: Optional[str]


class Message(TypedDict):
    system: Optional[List[Content]]
    user: Optional[List[Content]]
    assistants: Optional[Dict[str, List[Content]]]


class Comparison(TypedDict):
    type: Literal["text", "audio_url", "image_url", "video_url"]
    models: List[str]


class Combination(TypedDict):
    type: Literal["text", "audio_url", "image_url", "video_url"]
    models: List[str]


class ResponseFormat(TypedDict):
    type: Literal["text", "audio_url", "image_url", "video_url"]
    model_specific: Optional[
        Dict[str, Literal["text", "audio_url", "image_url", "video_url"]]
    ]


class ChatCompletionParams(TypedDict):
    models: List[str]
    messages: List[Message]
    web_search: Optional[bool]
    comparison: Optional[List[Comparison]]
    combination: Optional[List[Combination]]
    response_format: ResponseFormat
    temperature: Optional[float]
    max_tokens: Optional[int]
    frequency_penalty: Optional[float]
    presence_penalty: Optional[float]
    stream: Optional[bool]


class Chat(BaseModel):
    """Handles chat-related requests to the AlleAI platform, including completions, combinations, and comparison.

    Examples:
        Basic usage with a single model:
            >>> from alleai.core import AlleAIClient
            >>> client = AlleAIClient(api_key="your-api-key")
            >>> response = client.chat.completion({
            ...     "models": ["grok"],
            ...     "messages": [{"user": [{"type": "text", "text": "Hello!"}]}],
            ...     "response_format": {"type": "text"}
            ... })
            >>> print(response)
    """

    def _validate_params(self, params: ChatCompletionParams) -> None:
        """Validate common parameters for chat-related API requests.

        Args:
            params (ChatCompletionParams): The parameters to validate.

        Raises:
            InvalidRequestError: If required parameters are missing or invalid.
        """
        # Validate models (required)
        if (
            "models" not in params
            or not isinstance(params["models"], list)
            or len(params["models"]) == 0
        ):
            raise InvalidRequestError(
                message="models must be a non-empty array of strings",
                code="INVALID_MODELS",
            )
        if not all(isinstance(m, str) for m in params["models"]):
            raise InvalidRequestError(
                message="all elements in models must be strings",
                code="INVALID_MODELS_FORMAT",
            )

        # Validate messages (required)
        if (
            "messages" not in params
            or not isinstance(params["messages"], list)
            or len(params["messages"]) == 0
        ):
            raise InvalidRequestError(
                message="messages must be a non-empty array", code="INVALID_MESSAGES"
            )
        for i, msg in enumerate(params["messages"]):
            if not isinstance(msg, dict):
                raise InvalidRequestError(
                    message=f"messages[{i}] must be an object",
                    code="INVALID_MESSAGE_FORMAT",
                )
            valid_keys = {"system", "user", "assistants"}
            if not any(key in msg for key in valid_keys):
                raise InvalidRequestError(
                    message=f"messages[{i}] must have at least one of: system, user, assistants",
                    code="MISSING_MESSAGE_CONTENT",
                )
            for key in {"system", "user"}:
                if key in msg and msg[key]:
                    if not isinstance(msg[key], list):
                        raise InvalidRequestError(
                            message=f"{key} must be an array of content objects",
                            code="INVALID_CONTENT_FORMAT",
                        )
                    for j, content in enumerate(msg[key]):
                        if "type" not in content:
                            raise InvalidRequestError(
                                message=f"{key}[{j}] must be an object with a 'type' property",
                                code="MISSING_CONTENT_TYPE",
                            )
                        valid_types = {"text", "audio_url", "image_url", "video_url"}
                        if content["type"] not in valid_types:
                            raise InvalidRequestError(
                                message=f"{key}[{j}].type must be one of: {', '.join(valid_types)}",
                                code="INVALID_CONTENT_TYPE",
                            )
            if "assistants" in msg and msg["assistants"]:
                if not isinstance(msg["assistants"], dict):
                    raise InvalidRequestError(
                        message="assistants must be an object mapping models to content arrays",
                        code="INVALID_ASSISTANTS_FORMAT",
                    )
                for k, contents in msg["assistants"].items():
                    if not isinstance(contents, list):
                        raise InvalidRequestError(
                            message=f"assistants value for key '{k}' must be an array",
                            code="INVALID_ASSISTANT_CONTENT",
                        )
                    for j, content in enumerate(contents):
                        if "type" not in content:
                            raise InvalidRequestError(
                                message=f"assistants value[{j}] must be an object with a 'type' property",
                                code="MISSING_ASSISTANT_CONTENT_TYPE",
                            )
                        valid_types = {"text", "audio_url", "image_url", "video_url"}
                        if content["type"] not in valid_types:
                            raise InvalidRequestError(
                                message=f"assistants value[{j}].type must be one of: {', '.join(valid_types)}",
                                code="INVALID_ASSISTANT_CONTENT_TYPE",
                            )

    @handle_errors
    def completions(self, params: ChatCompletionParams) -> Dict[str, Any]:
        """Generate a chat completion with multiple models.

        Args:
            params (ChatCompletionParams): Parameters for the chat completion. Required:
                - models: List of model names (e.g., ["gpt-4", "grok", "gemini"]).
                - messages: List of message objects, each with optional keys:
                    - system: System messages (e.g., [{"type": "text", "text": "You are a helper"}]).
                    - user: User messages (e.g., [{"type": "text", "text": "Hello"}]).
                    - assistants: Assistant responses keyed by model name (e.g., {"grok": [{"type": "text", "text": "Hi"}]}).
                - response_format: Desired output format, with:
                    - type: "text", "audio_url", "image_url", or "video_url".
                    - model_specific: Optional per-model response types (e.g., {"grok": "text"}).

            Optional:
                - web_search: Enable web search context, default: False.
                - comparison: compare with type and models.
                - combination: Combinations with type and models.
                - temperature: Sampling temperature (0.0 to 2.0), default: 1.0.
                - max_tokens: Maximum tokens in the response.
                - frequency_penalty: Penalty for frequent words (-2.0 to 2.0), default: 0.0.
                - presence_penalty: Penalty for repeated topics (-2.0 to 2.0), default: 0.0.
                - stream: Stream the response, default: False.

        Returns:
            dict: API response with results from each model, structured according to response_format.

        Raises:
            InvalidRequestError: If required parameters are missing or invalid.

        Examples:
            >>> from alleai.core import AlleAIClient
            >>> from dotenv import load_dotenv
            >>> import os
            >>>
            >>> # Load environment variables from .env file
            >>> load_dotenv()
            >>>
            >>> # Get API key from .env
            >>> # Ensure ALLEAI_API_KEY is set in your .env file
            >>> api_key = os.getenv("ALLEAI_API_KEY")
            >>>
            >>> # Initialize client with API key
            >>> client = AlleAIClient(api_key=api_key)
            >>> chat = client.chat.completions({
            ...     "models": ["gpt-4o","o4-mini"],
            ...     "messages": [
            ...         {
            ...             "system": [
            ...                 {
            ...                     "type": "text",
            ...                     "text": "You are a helpful assistant."
            ...                 }
            ...             ]
            ...         },
            ...         {
            ...             "user": [
            ...                 {
            ...                     "type": "text",
            ...                     "text": "tell me about photosynthesis?"
            ...                 }
            ...             ]
            ...         }
            ...     ],
            ...     "temperature": 0.7,
            ...     "max_tokens": 2000,
            ...     "top_p": 1,
            ...     "frequency_penalty": 0.2,
            ...     "presence_penalty": 0.3,
            ...     "stream": False,
            ... })
            >>> print(chat)
        """
        self._validate_params(params)
        return self._make_request("post", "/chat/completions", params)

    @handle_errors
    def combination(self, params: ChatCompletionParams) -> Dict[str, Any]:
        """Generate a combined output from multiple AI models based on the provided messages.

        This method returns a unified response synthesized from multiple AI models rather than individual responses.

        Args:
            params (ChatCompletionParams): Parameters for the combination. Required:
                - models: List of model names to combine outputs from (e.g., ["gpt-4", "grok"]).
                - messages: List of message objects, each with optional keys:
                    - system: System messages (e.g., [{"type": "text", "text": "You are a helper"}]).
                    - user: User messages (e.g., [{"type": "text", "text": "Hello"}]).
                    - assistants: Assistant responses keyed by model name (e.g., {"grok": [{"type": "text", "text": "Hi"}]}).
                - response_format: Desired output format, with:
                    - type: "text", "audio_url", "image_url", or "video_url".
                    - model_specific: Optional per-model response types (e.g., {"grok": "text"}).

            Optional:
                - web_search: Enable web search context, default: False.
                - comparison: compare with type and models.
                - combination: Combinations with type and models.
                - temperature: Sampling temperature (0.0 to 2.0), default: 1.0.
                - max_tokens: Maximum tokens in the response.
                - frequency_penalty: Penalty for frequent words (-2.0 to 2.0), default: 0.0.
                - presence_penalty: Penalty for repeated topics (-2.0 to 2.0), default: 0.0.
                - stream: Stream the response, default: False.

        Returns:
            dict: API response with a combined result, structured according to response_format.

        Raises:
            InvalidRequestError: If required parameters are missing or invalid.
        """
        self._validate_params(params)
        param_copy = params.copy()
        param_copy["combination"] = True
        return self._make_request("post", "/chat/combination", param_copy)

    @handle_errors
    def comparison(self, params: ChatCompletionParams) -> Dict[str, Any]:
        """Generate focused model-to-model comparisons using the AlleAI platform.

        This method shares the same parameter structure as completions(), but serves a distinct purpose:
        while completions() can return both individual responses and comparisons, comparison() specializes
        in delivering only the comparative analysis between models. This optimization is valuable when your
        application needs to analyze differences between model responses without processing individual outputs.

        Args:
            params (ChatCompletionParams): Standard completion parameters as used in completions(), including:
                - models: List[str] - Models to compare (e.g., ["gpt-4", "grok"])
                - messages: List[Message] - The conversation context
                - response_format: ResponseFormat - Output format specification
                - temperature, max_tokens, etc. - Standard generation parameters
                
                The comparison parameter is required for this endpoint:
                - comparison: List[Comparison] - Specifies comparison configurations
                    - type: Literal["text", "audio_url", "image_url", "video_url"]
                    - models: List[str] - Models to include in comparison

        Returns:
            Dict[str, Any]: A structured comparison response containing:
                - Comparative analysis between specified models
                - Key differences and similarities in model outputs
                - Model-specific insights based on the comparison type

        Note:
            This endpoint is optimized for comparison workflows. For individual model responses
            alongside comparisons, use the completions() endpoint instead.

        See completions() method documentation for detailed parameter descriptions and options.

        Examples:
            >>> from alleai.core import AlleAIClient
            >>> from dotenv import load_dotenv
            >>> import os
            >>>
            >>> # Load environment variables from .env file
            >>> load_dotenv()
            >>>
            >>> # Get API key from .env
            >>> # Ensure ALLEAI_API_KEY is set in your .env file
            >>> api_key = os.getenv("ALLEAI_API_KEY")
            >>>
            >>> # Initialize client with API key
            >>> client = AlleAIClient(api_key=api_key)
            >>> comparison = client.chat.comparison({
            ...     "models": ["gpt-4o", "o4-mini"],
            ...     "messages": [
            ...         {
            ...             "system": [
            ...                 {
            ...                     "type": "text",
            ...                     "text": "You are a helpful assistant."
            ...                 }
            ...             ]
            ...         },
            ...         {
            ...             "user": [
            ...                 {
            ...                     "type": "text",
            ...                     "text": "Compare the approaches to async programming in Python and JavaScript."
            ...                 }
            ...             ]
            ...         }
            ...     ],
            ...     "comparison": [
            ...         {
            ...             "type": "text",
            ...             "models": ["gpt-4o", "o4-mini"]
            ...         }
            ...     ],
            ...     "temperature": 0.7,
            ...     "max_tokens": 2000,
            ...     "frequency_penalty": 0.2,
            ...     "presence_penalty": 0.3,
            ...     "stream": False,
            ... })
            >>> print(comparison)
        """
        self._validate_params(params)
        param_copy = params.copy()
        param_copy["comparison"] = True
        return self._make_request("post", "/chat/comparison", param_copy)

    @handle_errors
    def search(self, params: ChatCompletionParams) -> Dict[str, Any]:
        """Generate AI responses enhanced with real-time web search results.

        This method shares the same parameter structure as completions(), but specializes in
        web-augmented responses. While completions() can incorporate web search when web_search=True,
        this dedicated endpoint optimizes for search-enhanced responses. It automatically integrates
        relevant web information into the model's response without returning separate search results.

        Args:
            params (ChatCompletionParams): Standard completion parameters as used in completions(), including:
                - models: List[str] - Models to generate responses (e.g., ["gpt-4", "grok"])
                - messages: List[Message] - The conversation context
                - response_format: ResponseFormat - Output format specification
                - temperature, max_tokens, etc. - Standard generation parameters
                
                Note: web_search parameter is automatically set to True for this endpoint

        Returns:
            Dict[str, Any]: A structured response containing:
                - AI-generated content enriched with web search results
                - Seamlessly integrated web information in the response
                - Citations and references when applicable

        Note:
            This endpoint is optimized for web-enhanced responses. For separate model responses
            and web search results, use the completions() endpoint with web_search=True instead.

        See completions() method documentation for detailed parameter descriptions and options.

        Examples:
            >>> from alleai.core import AlleAIClient
            >>> from dotenv import load_dotenv
            >>> import os
            >>>
            >>> # Load environment variables from .env file
            >>> load_dotenv()
            >>>
            >>> # Get API key from .env
            >>> api_key = os.getenv("ALLEAI_API_KEY")
            >>>
            >>> # Initialize client with API key
            >>> client = AlleAIClient(api_key=api_key)
            >>> search_response = client.chat.search({
            ...     "models": ["gpt-4o"],
            ...     "messages": [
            ...         {
            ...             "system": [
            ...                 {
            ...                     "type": "text",
            ...                     "text": "You are a helpful assistant with access to current information."
            ...                 }
            ...             ]
            ...         },
            ...         {
            ...             "user": [
            ...                 {
            ...                     "type": "text",
            ...                     "text": "What are the latest developments in quantum computing as of 2024?"
            ...                 }
            ...             ]
            ...         }
            ...     ],
            ...     "temperature": 0.7,
            ...     "max_tokens": 2000,
            ...     "response_format": {"type": "text"}
            ... })
            >>> print(search_response)
        """
        # Ensure web_search is enabled
        params_copy = params.copy()
        params_copy["web_search"] = True

        self._validate_params(params_copy)
        return self._make_request("post", "/ai/web-search", params_copy)
