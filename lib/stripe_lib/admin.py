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
