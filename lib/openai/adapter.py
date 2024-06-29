# Python Standard Library Imports
import json

# HTK Imports
from htk.utils import htk_setting

from openai import OpenAI


class OpenAIAdapter:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = htk_setting('HTK_OPENAI_API_KEY')

        self.client = OpenAI(api_key=api_key)

    def chat_completion(
        self,
        system_prompt,
        user_prompt,
        model="gpt-3.5-turbo",
        max_tokens=150,
        temperature=0.5,
        target_reading_level=None,
        as_json=False,
    ):
        """Wrapper for OpenAI's chat completion API (`chat.completions.create`)

        Use this when:
        - Building a chatbot or any application that requires maintaining the context of a conversation over multiple turns.
        - Need to provide a sequence of messages to the model.
        - Using ChatGPT models like `gpt-3.5-turbo` which are optimized for dialogue.
        """
        messages = []
        messages.append({'role': 'system', 'content': system_prompt})

        if target_reading_level:
            messages.append(
                {
                    'role': 'system',
                    'content': f'Target reading level: {target_reading_level}',
                }
            )

        if as_json:
            messages.append(
                {
                    'role': 'system',
                    'content': 'The response MUST be valid JSON, and able to be parsed directly using standard Python `json.loads()`.',
                }
            )

        messages.append({'role': 'user', 'content': user_prompt})

        response = self.client.chat.completions.create(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            model=model,
        )

        response_content = response.choices[0].message.content
        try:
            response_data = json.loads(response_content)
        except json.JSONDecodeError:
            response_data = response_content

        return response_data
