from django.contrib import admin

class S3MediaAssetAdmin(admin.ModelAdmin):
    list_display = (
        'id',
    )
