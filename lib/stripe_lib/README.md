# Stripe_Lib

## Classes
- **`CreditCardForm`** (stripe_lib/forms.py) - A basic form for entering credit card numbers
- **`BaseStripeCustomer`** (stripe_lib/models.py) - Django model for Stripe Customer
- **`BaseStripeSubscription`** (stripe_lib/models.py) - Django model for Stripe Subscription
- **`BaseStripeProduct`** (stripe_lib/models.py) - Django model for Stripe Product
- **`BaseStripePrice`** (stripe_lib/models.py) - Django model for Stripe Price
- **`BaseStripePlan`** (stripe_lib/models.py) - Django model for Stripe Plan

## Functions
- **`get_stripe_card_dict_from_post_data`** (stripe_lib/form_utils.py) - Gets a Stripe card dict from `post_data` if possible
- **`extract_credit_card_params`** (stripe_lib/form_utils.py) - Extract credit card form params from `post_data`
- **`get_stripe_card_dict`** (stripe_lib/forms.py) - Get a dictionary representing this card compatible with Stripe's format
- **`retrieve`** (stripe_lib/models.py) - Retrieves a Stripe object via API
- **`modify`** (stripe_lib/models.py) - Updates the customer
- **`update_email`** (stripe_lib/models.py) - Updates the email for this Customer
- **`charge`** (stripe_lib/models.py) - Charges a Customer
- **`get_charges`** (stripe_lib/models.py) - List charges for a customer
- **`add_invoice_item`** (stripe_lib/models.py) - Create an `InvoiceItem` for the `Customer`
- **`create_invoice`** (stripe_lib/models.py) - Create an Invoice for this Customer to pay any outstanding invoice items such as when upgrading plans
- **`list_invoice_items`** (stripe_lib/models.py) - Lists the invoice items
- **`delete_pending_invoice_items`** (stripe_lib/models.py) - Delete invoices with status `pending`
- **`list_pending_invoice_items`** (stripe_lib/models.py) - Lists pending invoice items
- **`list_invoices`** (stripe_lib/models.py) - Lists all invoices
- **`create_invoice_and_pay`** (stripe_lib/models.py) - After creating the Invoice, have the Customer immediately pay it
- **`add_card`** (stripe_lib/models.py) - Add an additional credit card to the customer
- **`retrieve_card`** (stripe_lib/models.py) - Retrieves a card
- **`replace_card`** (stripe_lib/models.py) - Adds a new credit card and sets it as this Customer's default source
- **`get_card`** (stripe_lib/models.py) - Gets the customer's default card
- **`has_card`** (stripe_lib/models.py) - Determines whether this StripeCustomer has a card
- **`make_subscription_obj`** (stripe_lib/models.py) - Creates a subscription object to make it easier to handle this
- **`create_subscription`** (stripe_lib/models.py) - Creates a new Subscription for this Customer
- **`retrieve_subscription`** (stripe_lib/models.py) - Retrieves a Subscription for this Customer
- **`change_subscription_plan`** (stripe_lib/models.py) - Changes the plan on a Subscription for this Customer
- **`free_upgrade_or_downgrade`** (stripe_lib/models.py) - Updates the plan on a Subscription for this Customer
- **`cancel_subscription`** (stripe_lib/models.py) - Cancels a Subscription for this Customer
- **`delete`** (stripe_lib/models.py) - Deletes a customer
- **`create`** (stripe_lib/models.py) - Creates a new Subscription
- **`modify`** (stripe_lib/models.py) - Modifies a Subscription plan
- **`cancel`** (stripe_lib/models.py) - Cancels a Subscription for this Customer
- **`create`** (stripe_lib/models.py) - Tries to create a product
- **`create`** (stripe_lib/models.py) - Tries to create a price
- **`create`** (stripe_lib/models.py) - Tries to create a plan
- **`create_stripe_customer`** (stripe_lib/models.py) - Creates a new StripeCustomer object for this User if one does not exist
- **`add_or_replace_credit_card`** (stripe_lib/models.py) - Add or replace the credit card on file for this User
- **`test_charge_card`** (stripe_lib/tests.py) - Actually, charge a customer
- **`get_stripe_customer_model_instance`** (stripe_lib/utils.py) - Gets the StripeCustomerModel object for `customer_id` if available
- **`safe_stripe_call`** (stripe_lib/utils.py) - Wrapper function for calling Stripe API
- **`charge_card`** (stripe_lib/utils.py) - Charges a card, one time
- **`create_customer`** (stripe_lib/utils.py) - Create a Customer
- **`retrieve_event`** (stripe_lib/utils.py) - Retrieve the Stripe event by `event_id`
- **`get_event_type`** (stripe_lib/utils.py) - Gets the event type
- **`get_event_handler`** (stripe_lib/utils.py) - Gets the event handler for a Stripe webhook event, if available
- **`handle_event`** (stripe_lib/utils.py) - Handles a Stripe webhook event
- **`log_event`** (stripe_lib/utils.py) - Log the Stripe event `event`
- **`stripe_webhook_view`** (stripe_lib/views.py) - https://stripe.com/docs/webhooks

## Components
**Models** (`models.py`), **Views** (`views.py`), **Forms** (`forms.py`)
