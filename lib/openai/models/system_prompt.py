# Django Imports
from django.db import models

# HTK Imports
from htk.lib.openai.constants.prompts import (
    OPENAI_PROMPT_INSTRUCTION__EXPECTED_RESPONSE_FORMAT,
    OPENAI_PROMPT_INSTRUCTION__JSON_RESPONSE,
    OPENAI_PROMPT_INSTRUCTION_FORMAT__TARGET_READING_GRADE_LEVEL,
)
from htk.models.fk_fields import fk_user


DEFAULT_RELATED_NAME = 'openai_system_prompts'


class BaseOpenAISystemPrompt(models.Model):
    """Model to store OpenAI system prompts for reuse"""

    name = models.CharField(
        max_length=255,
        help_text='Name of the system prompt (internal use)',
    )
    key = models.CharField(
        max_length=255,
        unique=True,
        help_text='Snake case identifier for the system prompt (e.g. "chat_assistant_v1")',
    )
    description = models.TextField(
        blank=True,
        help_text='Description of the system prompt (internal use)',
    )
    content = models.TextField(
        help_text='Content of the system prompt (sent to ChatGPT)'
    )
    # response parameters
    target_reading_grade_level = models.PositiveIntegerField(
        default=0,
        help_text='Instruction to set the ChatGPT model to target a specific reading grade level when generating a response.',  # noqa: E501
    )
    as_json = models.BooleanField(
        default=False,
        help_text='Instruction to set the ChatGPT model to return a response in JSON format.',  # noqa: E501
    )
    expected_response_format = models.TextField(
        blank=True,
        help_text='Expected response format from ChatGPT (e.g. JSON schema, Markdown, etc.).',
    )
    created_by = fk_user(
        related_name=f'{DEFAULT_RELATED_NAME}_created',
        required=False,
    )
    updated_by = fk_user(
        related_name=f'{DEFAULT_RELATED_NAME}_updated',
        required=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name = 'OpenAI System Prompt'
        unique_together = ('key',)

    def __str__(self):
        return f'System Prompt: {self.key}'

    @property
    def has_response_parameters(self):
        result = (
            self.target_reading_grade_level > 0
            or self.as_json
            or self.expected_response_format
        )
        return result

    @property
    def response_parameters_instructions(self) -> list[str]:
        """Instructions to set the ChatGPT model to return a response in a specific format.

        Returns:
            list[str]: List of instructions to set the ChatGPT model to return a response in a specific format.
        """
        content_lines = ['Response Parameters:']

        if self.target_reading_grade_level > 0:
            content_lines.append(
                '- '
                + OPENAI_PROMPT_INSTRUCTION_FORMAT__TARGET_READING_GRADE_LEVEL.format(  # noqa: E501
                    target_reading_grade_level=self.target_reading_grade_level
                )
            )

        if self.expected_response_format:
            content_lines.append(
                '- '
                + OPENAI_PROMPT_INSTRUCTION__EXPECTED_RESPONSE_FORMAT
                + '\n'
                + '```'
                + self.expected_response_format
                + '```'
            )

        if self.as_json:
            content_lines.append(OPENAI_PROMPT_INSTRUCTION__JSON_RESPONSE)

        return content_lines

    @property
    def rendered_content(self) -> str:
        """Rendered content of the system prompt."""
        content_lines = [self.content]

        if self.has_response_parameters:
            content_lines.extend(self.response_parameters_instructions)

        content = "\n".join(content_lines)
        return content
