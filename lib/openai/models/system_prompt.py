# Django Imports
from django.db import models

# HTK Imports
from htk.lib.openai.constants.prompts import (
    OPENAI_PROMPT_JSON_RESPONSE_INSTRUCTION,
    OPENAI_PROMPT_TARGET_READING_GRADE_LEVEL_INSTRUCTION_FORMAT,
)
from htk.models.fk_fields import fk_user


DEFAULT_RELATED_NAME = 'openai_system_prompts'


class BaseOpenAISystemPrompt(models.Model):
    """Model to store OpenAI system prompts for reuse"""

    name = models.CharField(max_length=255)
    key = models.CharField(
        max_length=255,
        unique=True,
        help_text='Snake case identifier for the system prompt (e.g. "chat_assistant_v1")',
    )
    description = models.TextField(blank=True)
    content = models.TextField()
    target_reading_grade_level = models.PositiveIntegerField(default=0)
    as_json = models.BooleanField(default=False)
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
    def rendered_content(self):
        content_lines = [self.content]
        if self.target_reading_grade_level > 0:
            content_lines.append(
                OPENAI_PROMPT_TARGET_READING_GRADE_LEVEL_INSTRUCTION_FORMAT.format(  # noqa: E501
                    target_reading_grade_level=self.target_reading_grade_level
                )
            )
        if self.as_json:
            content_lines.append(OPENAI_PROMPT_JSON_RESPONSE_INSTRUCTION)

        content = "\n".join(content_lines)
        return content
