import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from htk.lib.stripe_lib.utils import retrieve_event

@require_POST
@csrf_exempt
def stripe_webhook_view(request):
    """https://stripe.com/docs/webhooks

    Common Uses

    - Payment receipt emails: Subscribe to charge.succeeded events and send your users an email
    - Metered billing: Subscribe to invoice.created events and add new invoice items to the invoice by specifying the invoice's ID in the invoiceitem creation API call.

    customer.created
    customer.subscription.created
    invoice.created
    charge.succeeded (immediate attempt for the first invoice)
    invoice.payment_succeeded
    invoice.created (after the subscription period is up)
    charge.succeeded (approximately one hour later)
    invoice.payment_succeeded
    """
    # Retrieve the request's body and parse it as JSON
    event_json = json.load(request.body)

    event_id = event_json['id']

    event = retrieve_event(event_id)

    if event:
        # Do something with event or event_json
        pass
    else:
        pass

    response = HttpResponse(status=200)
    return response
