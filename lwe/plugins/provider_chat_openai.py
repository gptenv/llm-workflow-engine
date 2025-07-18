from langchain_openai import ChatOpenAI

from lwe.core.provider import Provider, PresetValue
from lwe.core import constants


class CustomChatOpenAI(ChatOpenAI):
    @property
    def _llm_type(self):
        """Return type of llm."""
        return "chat_openai"


class ProviderChatOpenai(Provider):
    """
    Access to OpenAI chat models via the OpenAI API
    """

    def default_config(self):
        return {
            "validate_models": True,
        }

    def setup(self):
        self.log.info(
            f"Setting up Provider Chat OpenAI plugin, running with backend: {self.backend.name}"
        )
        super().setup()
        self.validate_models = self.config.get("plugins.provider_chat_openai.validate_models")

    def handle_non_streaming_response(self, response):
        """Handle non-streaming response and extract conversation_id if present."""
        # Check if conversation_id feature is enabled
        send_conversation_id = self.config.get("backend_options.send_conversation_id", False)
        if send_conversation_id:
            self.log.debug("Checking response for conversation_id at root level")
            
            # Try multiple ways to access the raw response data with conversation_id at root level
            conversation_id = None
            
            # Method 1: Direct attribute access (current approach)
            if hasattr(response, "conversation_id"):
                conversation_id = response.conversation_id
                self.log.debug(f"Found conversation_id via direct attribute: {conversation_id}")
            
            # Method 2: Check if response has raw response data or additional attributes
            elif hasattr(response, "raw") and hasattr(response.raw, "conversation_id"):
                conversation_id = response.raw.conversation_id
                self.log.debug(f"Found conversation_id in raw response: {conversation_id}")
                
            # Method 3: Check response_metadata for raw JSON data
            elif hasattr(response, "response_metadata"):
                # Look for raw response data in metadata
                if "conversation_id" in response.response_metadata:
                    conversation_id = response.response_metadata["conversation_id"]
                    self.log.debug(f"Found conversation_id in response_metadata: {conversation_id}")
                # Also check for nested raw response
                elif "raw" in response.response_metadata and isinstance(response.response_metadata["raw"], dict):
                    raw_data = response.response_metadata["raw"]
                    if "conversation_id" in raw_data:
                        conversation_id = raw_data["conversation_id"]
                        self.log.debug(f"Found conversation_id in raw metadata: {conversation_id}")
            
            # Method 4: Check additional_kwargs (sometimes used by LangChain for extra fields)
            elif hasattr(response, "additional_kwargs") and "conversation_id" in response.additional_kwargs:
                conversation_id = response.additional_kwargs["conversation_id"]
                self.log.debug(f"Found conversation_id in additional_kwargs: {conversation_id}")
            
            # If we found a conversation_id, store it for extraction
            if conversation_id:
                response._conversation_id = conversation_id
                self.log.debug(f"Stored conversation_id for extraction: {conversation_id}")
            else:
                self.log.debug("No conversation_id found in response at any level")
                
        return response

    def handle_streaming_chunk(self, chunk, previous_chunks):
        """Handle streaming chunk and extract conversation_id from metadata if present."""
        # Check if conversation_id feature is enabled
        send_conversation_id = self.config.get("backend_options.send_conversation_id", False)
        if send_conversation_id and hasattr(chunk, "conversation_id"):
            conversation_id = chunk.conversation_id
            self.log.debug(f"Found conversation_id in streaming chunk: {conversation_id}")
            # Store it in the chunk for later extraction
            chunk._conversation_id = conversation_id

        # Return the content as expected by the existing system
        if hasattr(chunk, "content"):
            return chunk.content
        return chunk

    @property
    def capabilities(self):
        return {
            "chat": True,
            "validate_models": self.validate_models,
        }

    @property
    def default_model(self):
        return constants.API_BACKEND_DEFAULT_MODEL

    @property
    def static_models(self):
        return {
            "gpt-3.5-turbo": {
                "max_tokens": 16384,
            },
            "gpt-3.5-turbo-16k": {
                "max_tokens": 16384,
            },
            "gpt-3.5-turbo-0613": {
                "max_tokens": 4096,
            },
            "gpt-3.5-turbo-16k-0613": {
                "max_tokens": 16384,
            },
            "gpt-3.5-turbo-1106": {
                "max_tokens": 16384,
            },
            "gpt-3.5-turbo-0125": {
                "max_tokens": 16384,
            },
            "gpt-4": {
                "max_tokens": 8192,
            },
            "gpt-4-32k": {
                "max_tokens": 32768,
            },
            "gpt-4-0613": {
                "max_tokens": 8192,
            },
            "gpt-4-32k-0613": {
                "max_tokens": 32768,
            },
            "gpt-4-turbo": {
                "max_tokens": 131072,
            },
            "gpt-4-turbo-2024-04-09": {
                "max_tokens": 131072,
            },
            "gpt-4-turbo-preview": {
                "max_tokens": 131072,
            },
            "gpt-4-1106-preview": {
                "max_tokens": 131072,
            },
            "gpt-4-0125-preview": {
                "max_tokens": 131072,
            },
            "gpt-4o": {
                "max_tokens": 131072,
            },
            "chatgpt-4o-latest": {
                "max_tokens": 131072,
            },
            "gpt-4o-2024-05-13": {
                "max_tokens": 131072,
            },
            "gpt-4o-2024-08-06": {
                "max_tokens": 131072,
            },
            "gpt-4o-2024-11-20": {
                "max_tokens": 131072,
            },
            "gpt-4o-mini": {
                "max_tokens": 131072,
            },
            "gpt-4o-mini-2024-07-18": {
                "max_tokens": 131072,
            },
            "gpt-4.1": {
                "max_tokens": 1047576,
            },
            "gpt-4.1-2025-04-14": {
                "max_tokens": 1047576,
            },
            "gpt-4.1-mini": {
                "max_tokens": 1047576,
            },
            "gpt-4.1-mini-2025-04-14": {
                "max_tokens": 1047576,
            },
            "gpt-4.1-nano": {
                "max_tokens": 1047576,
            },
            "gpt-4.1-nano-2025-04-14": {
                "max_tokens": 1047576,
            },
            "gpt-4.5-preview": {
                "max_tokens": 131072,
            },
            "gpt-4.5-preview-2025-02-27": {
                "max_tokens": 131072,
            },
            "o1-preview": {
                "max_tokens": 131072,
            },
            "o1-preview-2024-09-12": {
                "max_tokens": 131072,
            },
            "o1-mini": {
                "max_tokens": 131072,
            },
            "o1-mini-2024-09-12": {
                "max_tokens": 131072,
            },
            "o1": {
                "max_tokens": 204800,
            },
            "o1-2024-12-17": {
                "max_tokens": 204800,
            },
            # TODO: These are not chat models, how to support?
            # "o1-pro": {
            #     "max_tokens": 204800,
            # },
            # "o1-pro-2025-03-19": {
            #     "max_tokens": 204800,
            # },
            "o3-mini": {
                "max_tokens": 204800,
            },
            "o3-mini-2025-01-31": {
                "max_tokens": 204800,
            },
            "o3": {
                "max_tokens": 204800,
            },
            "o3-2025-04-16": {
                "max_tokens": 204800,
            },
            "o4-mini": {
                "max_tokens": 204800,
            },
            "o4-mini-2025-04-16": {
                "max_tokens": 204800,
            },
        }

    def prepare_messages_method(self):
        return self.prepare_messages_for_llm_chat

    def llm_factory(self):
        return CustomChatOpenAI

    def customization_config(self):
        return {
            "verbose": PresetValue(bool),
            "model_name": PresetValue(str, options=self.available_models),
            "temperature": PresetValue(float, min_value=0.0, max_value=2.0),
            "reasoning_effort": PresetValue(
                str, options=["low", "medium", "high"], include_none=True
            ),
            "openai_api_base": PresetValue(str, include_none=True),
            "openai_api_key": PresetValue(str, include_none=True, private=True),
            "openai_organization": PresetValue(str, include_none=True, private=True),
            "request_timeout": PresetValue(int),
            "max_retries": PresetValue(int, 1, 10),
            "n": PresetValue(int, 1, 10),
            "max_tokens": PresetValue(int, include_none=True),
            "top_p": PresetValue(float, min_value=0.0, max_value=1.0),
            "presence_penalty": PresetValue(float, min_value=-2.0, max_value=2.0),
            "frequency_penalty": PresetValue(float, min_value=-2.0, max_value=2.0),
            "seed": PresetValue(int, include_none=True),
            "logprobs": PresetValue(bool, include_none=True),
            "top_logprobs": PresetValue(int, min_value=0, max_value=20, include_none=True),
            "logit_bias": dict,
            "stop": PresetValue(str, include_none=True),
            "tools": None,
            "tool_choice": None,
            "model_kwargs": {
                "response_format": dict,
                "user": PresetValue(str),
            },
        }
