# OpenAI Constants

Configuration settings and prompt instructions for OpenAI integration.

## Configuration Settings

```python
from htk.lib.openai.constants import HTK_OPENAI_SYSTEM_PROMPT_MODEL
```

**HTK_OPENAI_SYSTEM_PROMPT_MODEL**
- Model identifier for system prompt generation
- Default: `None` (must be configured in settings)
- Examples: `'gpt-4'`, `'gpt-3.5-turbo'`, etc.

## Prompt Instructions

```python
from htk.lib.openai.constants import (
    OPENAI_PROMPT_INSTRUCTION_FORMAT__TARGET_READING_GRADE_LEVEL,
    OPENAI_PROMPT_INSTRUCTION__EXPECTED_RESPONSE_FORMAT,
    OPENAI_PROMPT_INSTRUCTION__JSON_RESPONSE,
)
```

### Reading Level Instruction

**OPENAI_PROMPT_INSTRUCTION_FORMAT__TARGET_READING_GRADE_LEVEL**
- Template for specifying target reading grade level in prompts
- Format: `'Target reading grade level: {target_reading_grade_level}'`
- Use: Fill in the placeholder with desired grade level (e.g., 8, 10, 12)

### Response Format Instructions

**OPENAI_PROMPT_INSTRUCTION__EXPECTED_RESPONSE_FORMAT**
- Instruction text indicating response format section
- Text: `'Expected response format:'`
- Precedes format specifications in system prompts

**OPENAI_PROMPT_INSTRUCTION__JSON_RESPONSE**
- Strict instruction for JSON-only responses
- Ensures response is valid JSON that can be parsed with `json.loads()`
- Useful for structured data extraction and API responses

## Example Usage

```python
from htk.lib.openai.constants import (
    OPENAI_PROMPT_INSTRUCTION_FORMAT__TARGET_READING_GRADE_LEVEL,
    OPENAI_PROMPT_INSTRUCTION__JSON_RESPONSE,
)

# Build prompt with reading level
reading_level_instruction = OPENAI_PROMPT_INSTRUCTION_FORMAT__TARGET_READING_GRADE_LEVEL.format(
    target_reading_grade_level=8
)

# Create system prompt with JSON requirement
system_prompt = f"""You are a helpful assistant.
{OPENAI_PROMPT_INSTRUCTION__JSON_RESPONSE}
"""
```

## Configuration in settings.py

```python
HTK_OPENAI_SYSTEM_PROMPT_MODEL = 'gpt-4'
```
