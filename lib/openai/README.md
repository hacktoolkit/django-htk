# OpenAI Integration

Chat completions and AI capabilities.

## Quick Start

```python
from htk.lib.openai.adapter import chat_completion

response = chat_completion([
    {'role': 'user', 'content': 'What is Python?'}
])
```

## System Prompts

```python
from htk.lib.openai.models.system_prompt import BaseOpenAISystemPrompt

prompt = BaseOpenAISystemPrompt.objects.create(
    name='helpful_assistant',
    content='You are a helpful assistant...'
)
```

## Configuration

```python
# settings.py
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
```

## Related Modules

- `htk.lib.google` - Alternative AI services
