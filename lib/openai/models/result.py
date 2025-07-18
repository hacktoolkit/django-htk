# Python Standard Library Imports
import json
from functools import cached_property

# Django Imports
from django.db import models

# Local Imports
from .fk_fields import fk_openai_system_prompt


class OpenAIResult(models.Model):
    """Model to store the results of OpenAI API calls"""

    ai_model = models.CharField(max_length=255)
    system_prompt = fk_openai_system_prompt(
        related_name='+',  # disable reverse relation
        required=False,
    )
    prompt_content = models.TextField()
    response_content = models.TextField()
    is_json = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        verbose_name = 'OpenAI Result'

    @cached_property
    def prompt_messages(self):
        return json.loads(self.prompt_content)

    @cached_property
    def system_prompt_content(self):
        if self.system_prompt:
            content = self.system_prompt.content
        else:
            system_prompt_lines = [
                message['content']
                for message in self.prompt_messages
                if message['role'] == 'system'
            ]
            content = "\n".join(system_prompt_lines)
        return content

    @cached_property
    def user_prompt(self):
        user_prompt_lines = [
            message['content']
            for message in self.prompt_messages
            if message['role'] == 'user'
        ]
        user_prompt = "\n".join(user_prompt_lines)
        return user_prompt

    @cached_property
    def response_json(self):
        return json.loads(self.response_content)
