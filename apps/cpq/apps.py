from django.apps import AppConfig
from django.db.models import signals

from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically

################################################################################
# signals and signal handlers

def sync_group_sub_quotes(sender, instance, created, **kwargs):
    """signal handler for GroupQuote post-save
    """
    if created:
        QuoteModel = resolve_model_dynamically(htk_setting('HTK_CPQ_QUOTE_MODEL'))
        group_quote = instance
        members = group_quote.organization.members.all()
        quotes = [
            QuoteModel(
                customer=member,
                group_quote=group_quote,
                date=group_quote.date
            )
            for member in members
        ]
        QuoteModel.objects.bulk_create(quotes)

class HtkCPQAppConfig(AppConfig):
    name = 'htk.apps.cpq'
    verbose_name = 'CPQ'

    def ready(self):
        GroupQuoteModel = resolve_model_dynamically(htk_setting('HTK_CPQ_GROUP_QUOTE_MODEL'))

        ##
        # signals
        signals.post_save.connect(sync_group_sub_quotes, sender=GroupQuoteModel)
