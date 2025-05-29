# Conversation ID Feature Implementation

## Overview

This feature enables the LLM Workflow Engine to handle conversation IDs from OpenAI's chat completion API. When enabled, the system will:

1. Check OpenAI responses for a `conversation_id` field
2. Store the conversation ID for the current conversation thread  
3. Include the conversation ID in subsequent requests within the same conversation

## Configuration

Add the following to your configuration file:

```yaml
backend_options:
  send_conversation_id: true  # Enable the feature (default: false)
```

Or set it to `false` to disable (which is the default):

```yaml
backend_options:
  send_conversation_id: false
```

If the option is not present in your config file, it defaults to `false`.

## How it Works

### When Feature is Enabled (`send_conversation_id: true`)

1. **Outgoing Requests**: If a conversation has a stored conversation_id from a previous response, it will be included in the request to OpenAI via `model_kwargs.extra_body.conversation_id`

2. **Incoming Responses**: The system checks OpenAI responses for:
   - `response_metadata.conversation_id` field
   - Extracts and stores the conversation_id for future use in the same conversation thread

3. **Conversation Tracking**: Each internal conversation maintains its own external conversation_id mapping

### When Feature is Disabled (`send_conversation_id: false` or not set)

- No conversation_id processing occurs
- Requests and responses are handled normally without conversation_id fields
- No performance impact

## Implementation Details

### Files Modified

- `lwe/core/constants.py`: Added default config option
- `config.sample.yaml`: Added configuration documentation  
- `lwe/backends/api/backend.py`: Added conversation_id tracking and coordination
- `lwe/backends/api/request.py`: Added conversation_id injection and extraction
- `lwe/backends/api/conversation_storage_manager.py`: Added external conversation_id tracking
- `lwe/plugins/provider_chat_openai.py`: Added response handlers for conversation_id

### Key Components

1. **Configuration**: `backend_options.send_conversation_id` boolean flag
2. **Request Enhancement**: Automatic conversation_id injection when available
3. **Response Processing**: Automatic conversation_id extraction from OpenAI responses
4. **State Management**: Per-conversation tracking of external conversation IDs

## OpenAI Provider Specific

This feature is specifically designed for the `provider_chat_openai` provider. Other providers will ignore conversation_id handling even when the feature is enabled.

## Backward Compatibility

This implementation is fully backward compatible:
- Default behavior is unchanged (feature disabled)
- Existing configurations work without modification
- No API changes to existing methods
- All existing tests continue to pass

## Security Considerations

- Conversation IDs are only processed for recognized OpenAI provider responses
- No sensitive data is logged beyond debug-level conversation_id values
- Feature can be completely disabled if not needed

## Testing

The implementation includes comprehensive tests for:
- Configuration option handling
- Request conversation_id injection
- Response conversation_id extraction  
- Provider-specific response handling
- Feature disabled/enabled behavior
- Integration with existing conversation management

All existing functionality remains intact and tested.