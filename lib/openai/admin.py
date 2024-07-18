# Django Imports
from django.contrib import admin


class OpenAIResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ai_model',
        'prompt_content',
        'response_content',
        'is_json',
        'created_at',
        'updated_at',
    )
