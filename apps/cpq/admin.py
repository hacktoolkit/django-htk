from django.contrib import admin

from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically

GroupQuoteModel = resolve_model_dynamically(htk_setting('HTK_CPQ_GROUP_QUOTE_MODEL'))
GroupQuoteLineItemModel = resolve_model_dynamically(htk_setting('HTK_CPQ_GROUP_QUOTE_LINE_ITEM_MODEL'))
InvoiceModel = resolve_model_dynamically(htk_setting('HTK_CPQ_INVOICE_MODEL'))
InvoiceLineItemModel = resolve_model_dynamically(htk_setting('HTK_CPQ_INVOICE_LINE_ITEM_MODEL'))
QuoteModel = resolve_model_dynamically(htk_setting('HTK_CPQ_QUOTE_MODEL'))
QuoteLineItemModel = resolve_model_dynamically(htk_setting('HTK_CPQ_QUOTE_LINE_ITEM_MODEL'))

class InvoiceLineItemInline(admin.TabularInline):
    model = InvoiceLineItemModel
    extra = 0
    can_delete = True

class InvoiceAdmin(admin.ModelAdmin):
    model = InvoiceModel

    list_display = (
        'id',
        'customer',
        'notes',
        'total',
        'date',
        'paid',
        'invoice_type',
        'payment_terms',
        'view_invoice_link',
    )

    list_filter = (
        'paid',
        'invoice_type',
        'payment_terms',
    )

    inlines = (
        InvoiceLineItemInline,
    )

    def total(self, obj):
        value = '$%s' % obj.get_total()
        return value

    def view_invoice_link(self, obj):
        value = u'<a href="%s" target="_blank">View Invoice</a>' % obj.get_url()
        return value

    view_invoice_link.allow_tags = True
    view_invoice_link.short_description = 'View Invoice'

class GroupQuoteLineItemInline(admin.TabularInline):
    model = GroupQuoteLineItemModel
    extra = 0
    can_delete = True

class GroupQuoteAdmin(admin.ModelAdmin):
    model = GroupQuoteModel

    list_display = (
        'id',
        'organization',
        'notes',
        'total',
        'date',
        'view_quote_link',
    )

    inlines = (
        GroupQuoteLineItemInline,
    )

    def total(self, obj):
        value = '$%s' % obj.get_total()
        return value

    def view_quote_link(self, obj):
        value = u'<a href="%s" target="_blank">View Quote</a>' % obj.get_url()
        return value

    view_quote_link.allow_tags = True
    view_quote_link.short_description = 'View Quote'

class QuoteLineItemInline(admin.TabularInline):
    model = QuoteLineItemModel
    extra = 0
    can_delete = True

class QuoteAdmin(admin.ModelAdmin):
    model = QuoteModel

    list_display = (
        'id',
        'customer',
        'notes',
        'total',
        'date',
        'view_quote_link',
    )

    inlines = (
        QuoteLineItemInline,
    )

    def total(self, obj):
        value = '$%s' % obj.get_total()
        return value

    def view_quote_link(self, obj):
        value = u'<a href="%s" target="_blank">View Quote</a>' % obj.get_url()
        return value

    view_quote_link.allow_tags = True
    view_quote_link.short_description = 'View Quote'

#admin.site.register(InvoiceModel, InvoiceAdmin)
#admin.site.register(QuoteModel, QuoteAdmin)
