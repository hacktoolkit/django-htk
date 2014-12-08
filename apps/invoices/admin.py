from django.contrib import admin

from htk.utils import htk_setting
from htk.utils.general import resolve_model_dynamically

InvoiceModel = resolve_model_dynamically(htk_setting('HTK_INVOICE_MODEL'))
InvoiceLineItemModel = resolve_model_dynamically(htk_setting('HTK_INVOICE_LINE_ITEM_MODEL'))

class InvoiceLineItemInline(admin.TabularInline):
    model = InvoiceLineItemModel
    extra = 0
    can_delete = True

class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'notes',
        'total',
        'date',
        'paid',
        'payment_terms',
        'view_invoice_link',
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

#admin.site.register(InvoiceModel, InvoiceAdmin)
