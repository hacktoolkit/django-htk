from django.contrib import admin

class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'stripe_id',
        'live_mode',
    )

class StripePlanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'stripe_id',
        'live_mode',
        'amount',
        'currency',
        'interval',
        'interval_count',
        'name',
        'trial_period_days',
        'statement_description',
    )
    list_filter = (
        'live_mode',
    )
