import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
    event_json = json.loads(request.body)

    event_id = event_json.get('id', None)
    live_mode = event_json.get('livemode', False)

    from htk.lib.stripe_lib.utils import retrieve_event
    event = retrieve_event(event_id, live_mode=live_mode)

    if event:
        from htk.lib.stripe_lib.utils import handle_event
        handle_event(event, request=request)
    elif event_id and not live_mode:
        # handle the Stripe dashboard webhook test case
        from htk.lib.stripe_lib.utils import log_event
        log_event(event_json, request=request)
    else:
        pass

    response = HttpResponse(status=200)
    return response
