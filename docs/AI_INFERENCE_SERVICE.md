# AI Inference Service Integration

## Overview

DEV-O integrates with an external AI inference service that wraps **Mistral 7B** model. This service handles all LLM inference requests for the CrewAI multi-agent system.

## Service Details

- **Host**: `34.136.165.200`
- **Port**: `7000`
- **Model**: Mistral 7B
- **Base URL**: `http://34.136.165.200:7000`

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# AI Service (External AI Inference Service - Mistral 7B)
AI_SERVICE_URL=http://34.136.165.200:7000
AI_SERVICE_API_KEY=                          # Optional: Add if service requires authentication
AI_SERVICE_MODEL=mistral-7b
AI_SERVICE_TIMEOUT=120                       # Request timeout in seconds
AI_SERVICE_MAX_INPUT_TOKENS=4096            # Maximum input context length
AI_SERVICE_MAX_OUTPUT_TOKENS=2048           # Maximum output generation length
```

### Token Limits

The Mistral 7B model has the following token constraints:

- **Maximum Input Tokens**: 4096 tokens (~3000 words)
  - This is the maximum context length the model can process
  - Includes system prompts, user messages, and conversation history
  - If exceeded, older messages are automatically truncated

- **Maximum Output Tokens**: 2048 tokens (~1500 words)
  - This is the maximum length of generated responses
  - Limits how much code/text each agent can produce per task
  - Ensures responses complete within reasonable time

### How It Works

1. **CrewAI Request**: When a user sends a project request, the CrewAI pipeline starts
2. **Agent Execution**: Each agent (Product Owner, Backend Dev, Frontend Dev, QA) makes LLM calls
3. **Token Management**: 
   - Input is automatically chunked if it exceeds 4096 tokens
   - Output is limited to 2048 tokens per request
   - Multiple requests are made for large code generation tasks
4. **Response Streaming**: Generated content streams back through WebSocket to frontend

## API Expectations

The external inference service should implement an OpenAI-compatible API with these endpoints:

### POST `/v1/completions` or `/v1/chat/completions`

**Request:**
```json
{
  "model": "mistral-7b",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Generate a Python function..."}
  ],
  "max_tokens": 2048,
  "temperature": 0.7,
  "stream": false
}
```

**Response:**
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "mistral-7b",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "def example():\n    pass"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 100,
    "total_tokens": 150
  }
}
```

## Error Handling

The system includes robust error handling for inference service issues:

- **Connection Errors**: Automatic retry with exponential backoff
- **Timeout Errors**: Request times out after 120 seconds (configurable)
- **Rate Limits**: Respects 429 status codes with retry-after headers
- **Token Limit Errors**: Automatically truncates input or requests smaller chunks

## Continuation on Failure

If an agent fails due to inference service issues (timeout, connection error, etc.), the continuation mechanism allows resuming:

1. Failed agent is marked in session context
2. User sees "Continue" button in UI
3. Clicking continue retries the failed agent
4. Successfully completed agents are skipped

## Monitoring

Monitor these aspects of the inference service:

- **Response Times**: Should average < 5 seconds per request
- **Token Usage**: Track prompt_tokens and completion_tokens
- **Error Rates**: Monitor 5xx errors and timeouts
- **Queue Depth**: If service has request queuing

## Testing Connection

Test the connection to the inference service:

```bash
# Test basic connectivity
curl http://34.136.165.200:7000/health

# Test inference endpoint
curl -X POST http://34.136.165.200:7000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-7b",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 50
  }'
```

## Troubleshooting

### Service Unreachable

If the service is unreachable:
1. Check network connectivity to `34.136.165.200`
2. Verify port `7000` is accessible
3. Check firewall rules
4. Verify service is running on the remote machine

### Token Limit Exceeded

If you see "maximum context length exceeded" errors:
1. Reduce `AI_SERVICE_MAX_INPUT_TOKENS` in configuration
2. Implement more aggressive conversation history truncation
3. Break large tasks into smaller subtasks

### Slow Responses

If responses are slow:
1. Check service load on `34.136.165.200`
2. Increase `AI_SERVICE_TIMEOUT` if needed
3. Monitor GPU utilization on inference server
4. Consider implementing response caching

## Future Enhancements

Potential improvements:

- **Load Balancing**: Multiple inference service instances
- **Caching**: Cache common prompts/responses
- **Batch Processing**: Batch multiple small requests
- **Streaming**: Implement streaming responses for real-time feedback
- **Fallback Models**: Automatic fallback to smaller/faster models
