# Adeptiv-AI LLM Response Evaluator SDK

A powerful, async-first Python SDK for evaluating and testing LLM (Large Language Model) outputs with comprehensive conversation support and intelligent sampling.

## Features

- **Async-First Architecture**: Built for high-performance async operations
- **Multi-Turn Conversations**: Support for sequential conversation testing
- **Session Management**: Anonymous sessions with optional custom aliases
- **Intelligent Sampling**: Configurable sampling ratios for cost optimization
- **Robust Error Handling**: Built-in retry logic and comprehensive validation
- **Flexible Context**: Support for retrieved chunks and system context
- **Enterprise Security**: API key + client secret authentication

## Installation

```bash
pip install adeptiv-ai-evaluator-sdk
```

## Quick Start

### Multi-Turn Conversation Testing

```python
from model_eval.adeptiv_ai_evaluator import LLMSequentialestCase, LLMResponseTestCase

async def test_conversation():
    client = AsyncEvaluatorClient(
        api_key="your_api_key",
        client_secret="your_client_secret",
    )
    
    await client.connect()

    test_cases  = [
            LLMResponseTestCase(
                query="I need help with my order",
                llm_response="I'd be happy to help you with your order. Could you please provide your order number?"
            ),
            LLMResponseTestCase(
                query="My order number is #12345",
                llm_response="Thank you! I found your order #12345. It was shipped yesterday and should arrive tomorrow."
            )
        ]

    # Create conversation test case
    conversation = LLMSequentialestCase(
        test_cases=test_cases,
        bot_role="customer_support_agent",
        role_description="Helpful customer support agent for e-commerce platform",
        model_name="gpt-4"
    )
    
    # Validate and process conversation
    conversation.validate()
    
    # Send each exchange for evaluation
    result = await client.send_output(conversation)
    print(f"Exchange evaluated: {result['status']}")

    await client.close()
```

#### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `api_key` | `str` | Required | Your Adeptiv-AI API key |
| `client_secret` | `str` | Required | Your Adeptiv-AI client secret |

#### Methods

##### `connect() -> Dict`
Establishes connection to Adeptiv-AI service and creates session.

**Returns:**
```python
{
    "is_connected": True,
    "project_id": "your_project_id"
}
```

**Parameters:**
- `test_case`: LLMResponseTestCase object containing query and response data

**Returns:**
```python
{
    "status": "success",
    "api_response": {...}
}
```

##### `close()`
Cleans up resources and disconnects from service.

### LLMResponseTestCase

Data class representing a single LLM interaction test case.

#### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | `str` | ✅ | The input query/prompt |
| `llm_response` | `str` | ✅ | The LLM's response |
| `retrieved_chunks` | `List[str]` | ❌ | Retrieved context chunks (for RAG) |
| `system_context` | `List[str]` | ❌ | System prompts/context |

### LLMSequentialestCase

Data class for multi-turn conversation testing.

#### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `test_cases` | `List[LLMResponseTestCase]` | ✅ | List of conversation exchanges |
| `app_role` | `str` | ✅ | Role of the AI assistant |
| `role_description` | `str` |❌ | Detailed role description |
| `prompt_instructions` | `str` |❌ | Prompt Instructions|
| `model_name` | `str` | ❌ | Model identifier (default: "gpt-4") |


### Error Handling

The SDK includes comprehensive error handling:

```python
try:
    result = await client.send_output(test_case)
    if result["status"] == "error":
        print(f"Evaluation failed: {result['details']}")
except RuntimeError as e:
    print(f"Connection error: {e}")
except ValueError as e:
    print(f"Validation error: {e}")
```

## Use Cases

- **Model Quality Assessment**: Evaluate response quality, accuracy, and relevance
- **Conversation Flow Testing**: Test multi-turn dialogue capabilities
- **RAG System Evaluation**: Assess retrieval-augmented generation performance
- **A/B Testing**: Compare different model versions or configurations
- **Production Monitoring**: Real-time evaluation of live AI systems
- **Compliance & Safety**: Monitor for bias, toxicity, and safety issues

## Environment Variables

You can also configure the client using environment variables:

```bash
export ADEPTIV_API_KEY="your_api_key"
export ADEPTIV_CLIENT_SECRET="your_client_secret"
```

## Requirements

- Python 3.7+
- aiohttp
- logging (built-in)
- dataclasses (built-in)
- typing (built-in)
- uuid (built-in)
- time (built-in)
- os (built-in)
- random (built-in)

## Security

- All communications use HTTPS
- API keys and client secrets are required for authentication
- Custom headers support for additional security layers
- Session isolation for multi-tenant applications

## Support

- **Documentation**: 
- **GitHub Issues**: 
- **Email Support**: [contact@adeptiv-ai.com](mailto:contact@adeptiv-ai.com)

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Adeptiv-AI** - Advancing AI evaluation and safety through intelligent automation.