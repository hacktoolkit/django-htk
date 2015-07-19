from django.contrib import admin

class BaseKVStorageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'key',
        'value',
        'created_on',
        'timestamp',
    )
