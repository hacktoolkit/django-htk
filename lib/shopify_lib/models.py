# Python Standard Library Imports
from decimal import Decimal

# Third Party (PyPI) Imports
import jsonfield

# Django Imports
from django.db import models

# HTK Imports
from htk.apps.geolocations.models import AbstractGeolocation
from htk.models import HtkBaseModel
from htk.utils.datetime_utils import parse_datetime


class ShopifyResource(HtkBaseModel):
    class Meta:
        abstract = True

    @classmethod
    def from_document(cls, document):
        instance = cls()
        pk  = document['_id']
        document['id'] = pk
        del document['_id']

        for key, value in document.items():
            if hasattr(instance, key):
                value = instance.deserialize_value(key, value)
                setattr(instance, key, value)
        return instance

    def upsert(self):
        cls = self.__class__
        # We can directly save without looking up an existing object first
        # since we already have an id and never need to generate an one.
        # Directly saving will in effect do an upsert.
        instance = self.save()
        return instance

    def deserialize_value(self, key, value):
        return value

    def calculate_timestamps(self):
        from htk.utils.datetime_utils import datetime_to_unix_time
        dt_fields = (
            'created_at',
            'updated_at',
            'published_at',
            'processed_at',
            'closed_at',
            'canceled_at',
        )
        update_fields = []
        for field in dt_fields:
            if hasattr(self, field):
                dt = getattr(self, field)
                if dt is not None:
                    timestamp_field = '%s_%s' % (field[:-3], 'timestamp',)
                    timestamp = datetime_to_unix_time(dt)
                    update_fields.append(timestamp_field)
                    setattr(self, timestamp_field, timestamp)
        self.save(update_fields=update_fields)

################################################################################
# Products

class ShopifyProduct(ShopifyResource):
    """https://help.shopify.com/api/reference/product
    """
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    published_at = models.DateTimeField(blank=True, null=True)
    created_timestamp = models.PositiveIntegerField(default=0)
    updated_timestamp = models.PositiveIntegerField(default=0)
    published_timestamp = models.PositiveIntegerField(default=0, blank=True, null=True)

    handle = models.CharField(max_length=63)
    title = models.CharField(max_length=127)
    sku = models.CharField(max_length=63, blank=True, null=True)
    product_type = models.CharField(max_length=63, blank=True)

    body_html = models.TextField(blank=True)
    template_suffix = models.CharField(max_length=63, blank=True)
    image = models.ForeignKey('ShopifyProductImage', blank=True, null=True)

    vendor = models.CharField(max_length=63)
    tags = jsonfield.JSONField()
    options = jsonfield.JSONField()
    published_scope = models.CharField(max_length=63, blank=True)

    def deserialize_value(self, key, value):
        if key in ['created_at', 'updated_at', 'published_at',]:
            value = parse_datetime(value) if value else None
        else:
            value = value
        return value

    class Meta:
        app_label = 'shopify'
        verbose_name = 'Shopify Product'

class ShopifyProductTag(ShopifyResource):
    id = models.CharField(primary_key=True, max_length=127)

    class Meta:
        app_label = 'shopify'
        verbose_name = 'Shopify Product Tag'

class ShopifyProductImage(ShopifyResource):
    """https://help.shopify.com/api/reference/product_image
    """
    id = models.BigIntegerField(primary_key=True)
    product = models.ForeignKey('ShopifyProduct')
    position = models.PositiveIntegerField()
    variant_ids = jsonfield.JSONField()

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_timestamp = models.PositiveIntegerField(default=0)
    updated_timestamp = models.PositiveIntegerField(default=0)

    src = models.URLField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    class Meta:
        app_label = 'shopify'
        verbose_name = 'Shopify Product Image'

    def deserialize_value(self, key, value):
        if key in ['created_at', 'updated_at',]:
            value = parse_datetime(value) if value else None
        else:
            value = value
        return value

class ShopifyProductVariant(ShopifyResource):
    """https://help.shopify.com/api/reference/product_variant
    """
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_timestamp = models.PositiveIntegerField(default=0)
    updated_timestamp = models.PositiveIntegerField(default=0)
    product = models.ForeignKey('ShopifyProduct', related_name='variants')
    position = models.PositiveIntegerField()

    sku = models.CharField(max_length=63, blank=True, null=True)
    title = models.CharField(max_length=127, blank=True, null=True)
    barcode = models.CharField(max_length=63, blank=True, null=True, default=None)
    option1 = models.CharField(max_length=255, blank=True, null=True)
    option2 = jsonfield.JSONField()
    option3 = jsonfield.JSONField()

    inventory_item_id = models.BigIntegerField()
    inventory_quantity = models.PositiveIntegerField(default=0)
    old_inventory_quantity = models.PositiveIntegerField(default=0)
    inventory_policy = models.CharField(max_length=63, blank=True, null=True)
    inventory_management = models.CharField(max_length=63, blank=True, null=True)

    fulfillment_service = models.CharField(max_length=63, blank=True, null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    taxable = models.BooleanField(default=True)

    requires_shipping = models.BooleanField(default=False)
    weight = models.PositiveIntegerField(default=0)
    weight_unit = models.CharField(max_length=15, blank=True, null=True)
    grams = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'shopify'
        verbose_name = 'Shopify Product Variant'

    def deserialize_value(self, key, value):
        if key in ['created_at', 'updated_at',]:
            value = parse_datetime(value) if value else None
        elif key in ['price', 'compare_at_price',]:
            value = Decimal(value) if value else None
        else:
            value = value
        return value

################################################################################
# Customers

class ShopifyCustomer(ShopifyResource):
    """https://help.shopify.com/api/reference/customer
    """
    id = models.BigIntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    created_timestamp = models.PositiveIntegerField(default=0)
    updated_timestamp = models.PositiveIntegerField(default=0)

    accepts_marketing = models.BooleanField(default=True)
    default_address = models.ForeignKey('ShopifyCustomerAddress', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    verified_email = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=63, blank=True, null=True)
    last_name = models.CharField(max_length=63, blank=True, null=True)
    metafield = jsonfield.JSONField()
    multipass_identifier = jsonfield.JSONField()

    last_order = models.ForeignKey('ShopifyOrder', blank=True, null=True)
    last_order_name = models.CharField(max_length=127, blank=True, null=True)
    orders_count = models.PositiveIntegerField()
    total_spent = models.DecimalField(max_digits=11, decimal_places=2)

    note = models.TextField(max_length=4000, blank=True, null=True)
    state = models.CharField(max_length=63, blank=True, null=True)
    tags = jsonfield.JSONField()
    tax_exempt = models.BooleanField()

    class Meta:
        app_label = 'shopify'
        verbose_name = 'Shopify Customer'

    def deserialize_value(self, key, value):
        if key in ['created_at', 'updated_at',]:
            value = parse_datetime(value) if value else None
        elif key in ['total_spent',]:
            value = Decimal(value) if value else None
        else:
            value = value
        return value

class ShopifyCustomerAddress(ShopifyResource, AbstractGeolocation):
    """https://help.shopify.com/api/reference/customeraddress
    """
    id = models.BigIntegerField(primary_key=True)
    customer = models.ForeignKey('ShopifyCustomer', related_name='addresses')
    name = models.CharField(max_length=127, blank=True, null=True)
    first_name = models.CharField(max_length=63, blank=True, null=True)
    last_name = models.CharField(max_length=63, blank=True, null=True)

    address1 = models.CharField(max_length=127, blank=True, null=True)
    address2 = models.CharField(max_length=127, blank=True, null=True)
    city = models.CharField(max_length=63, blank=True, null=True)
    company = models.CharField(max_length=63, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    province = models.CharField(max_length=31, blank=True, null=True)
    country = models.CharField(max_length=63, blank=True, null=True)
    zip = models.CharField(max_length=15, blank=True, null=True)
    province_code = models.CharField(max_length=15, blank=True, null=True)
    country_code = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        app_label = 'shopify'
        verbose_name = 'Shopify Customer Address'
        verbose_name_plural = 'Shopify Customer Addresses'

    def get_address_string(self):
        values = {
            'address1' : self.address1 if self.address1 else '',
            'address_space' : ', ' if self.address2 else '',
            'address2' : self.address2 if self.address2 else '',
            'city' : self.city if self.city else '',
            'state' : self.province_code if self.province_code else '',
            'zipcode' : self.zip if self.zip else '',
            'country' : self.country_code if self.country_code else '',
        }
        location = '%(address1)s%(address_space)s%(address2)s, %(city)s, %(state)s %(zipcode)s, %(country)s' % values
        return location

################################################################################
# Orders, Refunds, Transactions, Fulfillments

class ShopifyOrder(ShopifyResource):
    """https://help.shopify.com/api/reference/order
    """
    id = models.BigIntegerField(primary_key=True)
    token = models.CharField(max_length=255, blank=True, null=True, unique=True)
    customer = models.ForeignKey('ShopifyCustomer', blank=True, null=True)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    closed_at = models.DateTimeField(blank=True, null=True)
    created_timestamp = models.PositiveIntegerField(default=0)
    updated_timestamp = models.PositiveIntegerField(default=0)
    closed_timestamp = models.PositiveIntegerField(default=0, blank=True, null=True)

    cancel_reason = jsonfield.JSONField()
    canceled_at = models.DateTimeField(blank=True, null=True)
    canceled_timestamp = models.PositiveIntegerField(default=0, blank=True, null=True)

    processed_at = models.DateTimeField(blank=True, null=True)
    processed_timestamp = models.PositiveIntegerField(default=0, blank=True, null=True)
    processing_method = models.CharField(max_length=31, blank=True, null=True)

    buyer_accepts_marketing = models.BooleanField(default=True)
    browser_ip = models.CharField(max_length=31, blank=True, null=True)
    client_details = jsonfield.JSONField()
    source_name = models.CharField(max_length=63)
    landing_site = models.CharField(max_length=4000, blank=True, null=True)
    landing_site_ref = jsonfield.JSONField()
    referring_site = models.CharField(max_length=1000, blank=True, null=True)

    cart_token = models.CharField(max_length=255, blank=True, null=True)
    customer_locale = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    contact_email = models.EmailField()
    phone = models.CharField(max_length=16, blank=True, null=True)
    billing_address = jsonfield.JSONField()
    shipping_address = jsonfield.JSONField()
    shipping_lines = jsonfield.JSONField()

    total_line_items_price = models.DecimalField(max_digits=11, decimal_places=2)
    discount_codes = jsonfield.JSONField()
    total_discounts = models.DecimalField(max_digits=11, decimal_places=2)
    subtotal_price = models.DecimalField(max_digits=11, decimal_places=2)
    total_tax = models.DecimalField(max_digits=11, decimal_places=2)
    tax_lines = jsonfield.JSONField()
    taxes_included = models.BooleanField(default=False)
    currency = models.CharField(max_length=31)
    total_price = models.DecimalField(max_digits=11, decimal_places=2)
    total_price_usd = models.DecimalField(max_digits=11, decimal_places=2)

    reference = jsonfield.JSONField()
    taxes_included = models.BooleanField()
    financial_status = models.CharField(max_length=63, blank=True, null=True)

    gateway = models.CharField(max_length=63, blank=True, null=True)
    payment_gateway_names = jsonfield.JSONField()

    location_id = models.BigIntegerField(blank=True, null=True)
    confirmed = models.BooleanField()
    user_id = jsonfield.JSONField()
    fulfillment_status = models.CharField(max_length=63, blank=True, null=True)
    source_identifier = jsonfield.JSONField()

    name = models.CharField(max_length=127, blank=True, null=True)
    order_number = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    note = models.TextField(max_length=4000, blank=True, null=True)
    note_attributes = jsonfield.JSONField()

    test = models.BooleanField(default=False)
    app_id = models.BigIntegerField()

    tags = jsonfield.JSONField()
    source_url = models.CharField(max_length=255, blank=True, null=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    checkout_token = models.CharField(max_length=255, blank=True, null=True)
    checkout_id = models.BigIntegerField()
    node_attributes = jsonfield.JSONField()
    order_status_url = models.URLField(blank=True)
    total_weight = models.PositiveIntegerField()

    class Meta:
        app_label = 'shopify'
        verbose_name = 'Shopify Order'

    def deserialize_value(self, key, value):
        if key in ['created_at', 'updated_at', 'processed_at', 'closed_at', 'canceled_at',]:
            value = parse_datetime(value) if value else None
        elif key in ['subtotal_price', 'total_line_items_price', 'total_discounts', 'total_price', 'total_price_usd',]:
            value = Decimal(value) if value else None
        else:
            value = value
        return value

class ShopifyOrderLineItem(ShopifyResource):
    id = models.BigIntegerField(primary_key=True)
    order = models.ForeignKey('ShopifyOrder', related_name='line_items')
    product = models.ForeignKey('ShopifyProduct', blank=True, null=True)
    variant = models.ForeignKey('ShopifyProductVariant', blank=True, null=True)

    sku = models.CharField(max_length=63, blank=True, null=True)
    title = models.CharField(max_length=127)
    variant_title = models.CharField(max_length=127, blank=True, null=True)
    name = models.CharField(max_length=127)

    fulfillable_quantity = models.PositiveIntegerField(default=0)
    fulfillment_service = models.CharField(max_length=63, blank=True, null=True)
    fulfillment_status = models.CharField(max_length=63, blank=True, null=True)
    grams = models.PositiveIntegerField(default=0)

    price = models.DecimalField(max_digits=11, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    total_discount = models.DecimalField(max_digits=11, decimal_places=2)
    gift_card = models.BooleanField(default=False)
    taxable = models.BooleanField(default=True)
    tax_lines = jsonfield.JSONField()

    requires_shipping = models.BooleanField(default=False)
    variant_inventory_management = models.CharField(max_length=63, blank=True, null=True)
    origin_location = jsonfield.JSONField()
    destination_location = jsonfield.JSONField()
    product_exists = models.BooleanField(default=False)
    vendor = models.CharField(max_length=63, blank=True, null=True)
    properties = jsonfield.JSONField()

    class Meta:
        app_label = 'shopify'
        verbose_name = 'Shopify Order Line Item'

    def deserialize_value(self, key, value):
        if key in ['total_discount', 'price',]:
            value = Decimal(value) if value else None
        else:
            value = value
        return value

class ShopifyFulFillment(ShopifyResource):
    """https://help.shopify.com/api/reference/fulfillment
    """
    id = models.BigIntegerField(primary_key=True)
    order = models.ForeignKey('ShopifyOrder', related_name='fulfillments')

    created_at = models.DateTimeField()
    created_timestamp = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_timestamp = models.PositiveIntegerField(default=0, blank=True, null=True)

    line_items = jsonfield.JSONField()
    notify_customer = models.BooleanField(default=True)
    receipt = jsonfield.JSONField()
    status = models.CharField(max_length=15, blank=True, null=True)
    tracking_company = models.CharField(max_length=63, blank=True, null=True)
    tracking_numbers = jsonfield.JSONField()
    tracking_urls = jsonfield.JSONField()
    variant_inventory_management = models.CharField(max_length=63, blank=True, null=True)

    class Meta:
        app_label = 'shopify'
        verbose_name = 'Shopify Fulfillment'

    def deserialize_value(self, key, value):
        if key in ['created_at', 'updated_at',]:
            value = parse_datetime(value) if value else None
        else:
            value = value
        return value

class ShopifyRefund(ShopifyResource):
    """https://help.shopify.com/api/reference/refund
    """
    id = models.BigIntegerField(primary_key=True)
    order = models.ForeignKey('ShopifyOrder', related_name='refunds')

    created_at = models.DateTimeField()
    created_timestamp = models.PositiveIntegerField(default=0)
    processed_at = models.DateTimeField(blank=True, null=True)
    processed_timestamp = models.PositiveIntegerField(default=0, blank=True, null=True)

    refund_line_items = jsonfield.JSONField()
    restock = models.BooleanField(default=False)
    note = models.TextField(max_length=4000, blank=True, null=True)
    user_id = models.BigIntegerField()

    class Meta:
        app_label = 'shopify'
        verbose_name = 'Shopify Transaction'

    def deserialize_value(self, key, value):
        if key in ['created_at', 'processed_at',]:
            value = parse_datetime(value) if value else None
        else:
            value = value
        return value

class ShopifyTransaction(ShopifyResource):
    """https://help.shopify.com/api/reference/transaction
    """
    id = models.BigIntegerField(primary_key=True)
    order = models.ForeignKey('ShopifyOrder', related_name='transactions')
    refund = models.ForeignKey('ShopifyRefund', related_name='transactions', blank=True, null=True)
    kind = models.CharField(max_length=31, blank=True, null=True)

    created_at = models.DateTimeField()
    created_timestamp = models.PositiveIntegerField(default=0)

    amount = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=3, blank=True, null=True)
    authorization = models.CharField(max_length=63, blank=True, null=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    source_name = models.CharField(max_length=63)

    gateway = models.CharField(max_length=63, blank=True, null=True)
    payment_details = jsonfield.JSONField()
    receipt = jsonfield.JSONField()
    status = models.CharField(max_length=15, blank=True, null=True)
    error_code = models.CharField(max_length=31, blank=True, null=True)

    test = models.BooleanField(default=False)
    user_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        app_label = 'shopify'
        verbose_name = 'Shopify Transaction'

    def deserialize_value(self, key, value):
        if key in ['created_at',]:
            value = parse_datetime(value) if value else None
        elif key in ['amount',]:
            value = Decimal(value) if value else None
        else:
            value = value
        return value
