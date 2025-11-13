# Openai

## Classes
- **`OpenAIResult`** (openai/models/result.py) - Model to store the results of OpenAI API calls
- **`BaseOpenAISystemPrompt`** (openai/models/system_prompt.py) - Model to store OpenAI system prompts for reuse

## Functions
- **`chat_completion`** (openai/adapter.py) - Wrapper for OpenAI's chat completion API (`chat.completions.create`)
- **`response_parameters_instructions`** (openai/models/system_prompt.py) - Instructions to set the ChatGPT model to return a response in a specific format.
- **`rendered_content`** (openai/models/system_prompt.py) - Rendered content of the system prompt.
