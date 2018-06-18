from django.contrib import admin

class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'stripe_id',
        'live_mode',
    )
    readonly_fields = (
        'id',
        'cards',
        'charges',
    )
    fields = (
        'id',
        'stripe_id',
        'live_mode',
        'cards',
        'charges'
    )

    def cards(self, obj):
        cards = obj.get_cards()
        value = '%s' % cards
        return value

    def charges(self, obj):
        charges = obj.get_charges()
        value = '%s' % charges
        return value

class StripeProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'stripe_id',
        'live_mode',
        'name',
        'product_type',
        'active',
        'statement_descriptor',
    )
    list_filter = (
        'live_mode',
        'active',
        'product_type',
    )

class StripePlanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'stripe_id',
        'product_id',
        'live_mode',
        'amount',
        'currency',
        'interval',
        'interval_count',
        'nickname',
        'trial_period_days',
    )
    list_filter = (
        'live_mode',
        'product_id',
    )
