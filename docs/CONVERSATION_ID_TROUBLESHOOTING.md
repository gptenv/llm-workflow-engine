# Conversation ID Feature Troubleshooting Guide

The conversation_id feature allows LWE to send and receive conversation IDs with custom OpenAI-compatible APIs to maintain conversation continuity.

## Quick Setup

1. **Enable the feature** in your config:
```yaml
backend_options:
  send_conversation_id: true
```

2. **Ensure you're using the OpenAI provider**:
```yaml
# Your provider should be provider_chat_openai
model:
  default_preset: your_preset_name  # Using OpenAI provider
```

3. **Set your custom API base URL**:
```yaml
model_customizations:
  openai_api_base: "https://your-custom-api-endpoint.com/v1"
```

## How It Works

### Sending conversation_id
When a conversation_id exists, LWE adds it to the request:
```json
{
  "model": "gpt-4",
  "messages": [...],
  "conversation_id": "conv-abc123"  // Added to extra_body
}
```

### Receiving conversation_id
LWE extracts conversation_id from responses in this priority order:
1. `message._conversation_id` (direct attribute)
2. `message.response_metadata["conversation_id"]` (LangChain metadata)
3. `message.additional_kwargs["conversation_id"]` (most common for custom APIs)

## Troubleshooting

### Enable Debug Logging
Add to your config to see conversation_id processing:
```yaml
logging:
  level: DEBUG
```

Look for these log messages:
- `Adding conversation_id to request: <id>`
- `Extracted conversation_id from additional_kwargs: <id>`
- `Storing external conversation_id for conversation <id>: <external_id>`

### Test Scenario
1. **First message**: LWE sends request without conversation_id
   - Your API should return a conversation_id in the response
   - LWE should extract and store it

2. **Second message**: LWE sends request with stored conversation_id
   - Your API should use it to continue the same conversation thread

### Common Issues

**Issue**: "conversation_id not being sent"
- Check: Is `send_conversation_id: true` in config?
- Check: Are you using `provider_chat_openai`?

**Issue**: "conversation_id not being extracted"
- Check: Does your API return conversation_id in the response?
- Check: Debug logs for extraction attempts
- Most likely: Your API returns it in `additional_kwargs`

**Issue**: "New thread created each time"
- Check: Is conversation_id being extracted from first response?
- Check: Is the same conversation_id being sent in subsequent requests?

### Test Your Setup

Run this diagnostic to verify your configuration:

```python
from lwe.core.config import Config

config = Config()
send_enabled = config.get("backend_options.send_conversation_id", False)
print(f"send_conversation_id enabled: {send_enabled}")

if not send_enabled:
    print("❌ Add 'backend_options.send_conversation_id: true' to your config")
else:
    print("✅ Configuration looks correct")
```

## Custom API Requirements

Your custom OpenAI-compatible API should:

1. **Accept conversation_id** in requests (will be in extra_body)
2. **Return conversation_id** in responses (preferably in additional_kwargs)
3. **Use conversation_id** to maintain conversation state/history

Example response format that works:
```json
{
  "choices": [{
    "message": {
      "role": "assistant", 
      "content": "Hello!"
    }
  }],
  "conversation_id": "conv-abc123"  // This gets mapped to additional_kwargs
}
```