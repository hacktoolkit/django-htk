from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect

from htk.decorators.classes import restful_obj_seo_redirect
from htk.utils import htk_setting
from htk.utils import resolve_model_dynamically
from htk.utils.templates import get_renderer
from htk.utils.templates import get_template_context_generator
from htk.view_helpers import add_page_title
from htk.view_helpers import render_to_response_custom as _r
from htk.view_helpers import wrap_data as htk_wrap_data

Product = resolve_model_dynamically(htk_setting('HTK_STORE_PRODUCT_MODEL'))
ProductCollection = resolve_model_dynamically(htk_setting('HTK_STORE_PRODUCT_COLLECTION_MODEL'))

def index(request):
    renderer = get_renderer()
    wrap_data = get_template_context_generator()
    data = wrap_data(request)
    data['product_collections'] = ProductCollection.objects.all()
    response = renderer('store/index.html', data)
    return response

def product_collections(request):
    renderer = get_renderer()
    wrap_data = get_template_context_generator()
    data = wrap_data(request)
    data['product_collections'] = ProductCollection.objects.all()
    response = renderer('store/collections.html', data)
    return response

def products(request):
    renderer = get_renderer()
    wrap_data = get_template_context_generator()
    data = wrap_data(request)
    data['products'] = Product.objects.all()
    response = renderer('store/products.html', data)
    return response

@restful_obj_seo_redirect(ProductCollection, 'collection_id')
def product_collection_view(request, collection_id, seo_title, **kwargs):
    renderer = get_renderer()
    wrap_data = get_template_context_generator()
    product_collection = kwargs.pop('productcollection')
    data = wrap_data(request)
    data['product_collection'] = product_collection
    response = renderer('store/collection.html', data)
    return response

@restful_obj_seo_redirect(Product, 'product_id')
def product(request, product_id, seo_title, **kwargs):
    renderer = get_renderer()
    wrap_data = get_template_context_generator()
    product = kwargs.pop('product')
    data = wrap_data(request)
    data['product'] = product
    response = renderer('store/product.html', data)
    return response
