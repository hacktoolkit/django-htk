# Python Standard Library Imports
import json
import typing as T

# Third Party (PyPI) Imports
from openai import OpenAI

# HTK Imports
from htk.lib.openai.constants.prompts import (
    OPENAI_PROMPT_INSTRUCTION__JSON_RESPONSE,
    OPENAI_PROMPT_INSTRUCTION_FORMAT__TARGET_READING_GRADE_LEVEL,
)
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


# isort: off


if T.TYPE_CHECKING:
    from .models import OpenAIResult


class OpenAIAdapter:
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = htk_setting('HTK_OPENAI_API_KEY')

        self.client = OpenAI(api_key=api_key)

    def chat_completion(
        self,
        system_prompt_lines: list[str],
        user_prompt_lines: list[str],
        system_prompt: T.Optional[
            T.Type[resolve_model_dynamically('HTK_OPENAI_SYSTEM_PROMPT_MODEL')]
        ] = None,
        model: str = "gpt-4o-mini",
        max_tokens: int = 150,
        temperature: float = 0.5,
        target_reading_grade_level: T.Optional[int] = None,
        as_json: bool = False,
        result_storage_model: T.Optional[T.Type['OpenAIResult']] = None,
        result_storage_model_kwargs: T.Optional[dict] = None,
    ) -> T.Union[str, dict, T.Type['OpenAIResult']]:
        """Wrapper for OpenAI's chat completion API (`chat.completions.create`)

        Use this when:
        - Building a chatbot or any application that requires maintaining the context of a conversation over multiple turns.
        - Need to provide a sequence of messages to the model.
        - Using ChatGPT models like `gpt-3.5-turbo`, `gpt-4o-mini` which are optimized for dialogue.
        """
        all_system_prompt_lines = []
        if system_prompt:
            all_system_prompt_lines.append(system_prompt.rendered_content)
        else:
            all_system_prompt_lines.extend(system_prompt_lines)

            if target_reading_grade_level:
                all_system_prompt_lines.append(
                    OPENAI_PROMPT_INSTRUCTION_FORMAT__TARGET_READING_GRADE_LEVEL.format(
                        target_reading_grade_level=target_reading_grade_level
                    )
                )

            if as_json:
                all_system_prompt_lines.append(
                    OPENAI_PROMPT_INSTRUCTION__JSON_RESPONSE
                )

        _system_prompt = "\n".join(all_system_prompt_lines)
        _user_prompt = "\n".join(user_prompt_lines)

        messages = [
            {'role': 'system', 'content': _system_prompt},
            {'role': 'user', 'content': _user_prompt},
        ]

        response = self.client.chat.completions.create(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            model=model,
        )

        response_content = response.choices[0].message.content
        is_json = False

        if as_json or system_prompt and system_prompt.as_json:
            try:
                response_data = json.loads(response_content)
                is_json = True
            except json.JSONDecodeError:
                response_data = response_content
        else:
            response_data = response_content

        if result_storage_model:
            result_storage_model_kwargs = result_storage_model_kwargs or {}
            result_storage_model_kwargs['ai_model'] = model
            if system_prompt:
                # Remove the system prompt from the messages when using a stored system prompt
                messages = messages[1:]
                result_storage_model_kwargs['system_prompt'] = system_prompt
            else:
                # NOOP: When not using a stored system prompt, we don't need to remove the system prompt from the messages
                pass

            result_storage_model_kwargs.update(
                {
                    'ai_model': model,
                    'prompt_content': json.dumps(messages),
                    'response_content': response_content,
                    'is_json': is_json,
                }
            )
            result = result_storage_model.objects.create(
                **result_storage_model_kwargs
            )
        else:
            result = response_data

        return result
