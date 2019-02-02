# Python Standard Library Imports

# Third Party / PIP Imports

# Django Imports
from django.contrib import admin

# HTK Imports


class HtkInvitationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'invited_by',
        'campaign',
        'notes',
        'user',
        'status',
        'created_at',
        'timestamp',
    )
    list_filter = (
        'campaign',
        'invited_by',
        'status',
    )
