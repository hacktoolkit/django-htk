# Python Standard Library Imports
import json
from functools import cached_property

# Django Imports
from django.db import models


class OpenAIResult(models.Model):
    """Model to store the results of OpenAI API calls"""

    ai_model = models.CharField(max_length=255)
    prompt_content = models.TextField()
    response_content = models.TextField()
    is_json = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @cached_property
    def prompt_messages(self):
        return json.loads(self.prompt_content)

    @cached_property
    def system_prompt(self):
        system_prompt_lines = [
            message['content']
            for message in self.prompt_messages
            if message['role'] == 'system'
        ]
        system_prompt = "\n".join(system_prompt_lines)
        return system_prompt

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
