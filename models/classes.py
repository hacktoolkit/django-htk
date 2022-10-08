# Python Standard Library Imports
import json

# Third Party (PyPI) Imports
import six.moves.urllib as urllib

# Django Imports
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http import Http404
from django.urls import reverse
from django.utils.http import (
    base36_to_int,
    int_to_base36,
)

# HTK Imports
from htk.utils import (
    htk_setting,
    utcnow,
)
from htk.utils.cache_descriptors import CachedAttribute
from htk.utils.general import resolve_model_dynamically


# isort: off


"""
While we *could* import models here for convenience,
we must also remember to be careful to not assume that the external dependencies will be met for every platform, so it's better to import only what's needed explicitly

For example, the following module requires AWS Credentials.
  from htk.lib.aws.s3.models import S3MediaAsset

Others, like imaging libraries, require PIL, etc
"""


class HtkBaseModel(models.Model):
    """An abstract class extending Django models.Model for performing common operations
    """
    class Meta:
        abstract = True

    def json_encode(self):
        """Returns a dictionary that can be `json.dumps()`-ed as a JSON representation of this object
        """
        value = {
            'id' : self.id,
        }
        return value

    def json_decode(self, payload):
        """Iterates over a flat dictionary `payload` and updates the attributes on `self`
        """
        was_updated = False
        for key, value in payload.items():
            if hasattr(self, key):
                was_updated = True
                setattr(self, key, value)

        if was_updated:
            self.save()

        return was_updated

    ##
    # Crypto

    @classmethod
    def _luhn_xor_key(cls):
        xor_key = htk_setting('HTK_LUHN_XOR_KEYS').get(cls.__name__, 0)
        return xor_key

    @CachedAttribute
    def id_with_luhn_base36(self):
        from htk.utils.luhn import calculate_luhn
        xor_key = self.__class__._luhn_xor_key()
        xored = self.id ^ xor_key
        check_digit = calculate_luhn(xored)
        id_with_luhn = xored * 10 + check_digit
        encoded_id = int_to_base36(id_with_luhn)
        return encoded_id

    @classmethod
    def from_encoded_id_luhn_base36(cls, encoded_id):
        from htk.utils.luhn import is_luhn_valid
        id_with_luhn = base36_to_int(encoded_id)
        if is_luhn_valid(id_with_luhn):
            xored = id_with_luhn // 10
            xor_key = cls._luhn_xor_key()
            obj_id =  xored ^ xor_key
            obj = cls.objects.get(id=obj_id)
        else:
            obj = None
        return obj

    @classmethod
    def from_encoded_id_luhn_base36_or_404(cls, encoded_id):
        try:
            obj = cls.from_encoded_id_luhn_base36(encoded_id)
        except cls.DoesNotExist:
            obj = None

        if obj is None:
            raise Http404('No %s matches the given query.' % cls.__name__)
        return obj

    ##
    # URLs

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        url = reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
        return url

    def get_absolute_url(self):
        raise Exception('Not implemented')

    ##
    # SEO and Unicode

    @CachedAttribute
    def seo_title(self):
        raise Exception('Not implemented')

    def has_seo_title_match(self, seo_title):
        has_match = seo_title is not None and (
            self.seo_title == seo_title
            or self.seo_title == urllib.parse.unquote(seo_title)
            or urllib.parse.quote(self.seo_title) == seo_title
        )

        return has_match


class AbstractAttribute(models.Model):
    """An abstract class for storing an arbitrary attribute on a Django model

    The concrete implementing class should have a ForeignKey to the holder object
    and a related_name of "attributes", e.g.

      holder = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='attributes')

    """
    key = models.CharField(max_length=128, blank=True)
    value = models.TextField(max_length=4096, blank=True)

    # meta
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def set_value(self, value):
        self.value = value
        self.save()

    def value_as_json(self):
        try:
            value = json.loads(self.value)
        except ValueError:
            value = None
        return value


class AbstractAttributeHolderClassFactory(object):
    """Creates an attribute holder class for multi-inheritance
    """
    def __init__(self, attribute_class, holder_resolver=None, defaults=None):
        self.attribute_class = attribute_class
        if holder_resolver is None:
            self.holder_resolver = lambda self: self
        else:
            self.holder_resolver = holder_resolver
        self.defaults = defaults or {}

    def get_class(self):
        factory = self
        class AbstractAttributeHolderClass(object):
            def set_attribute(self, key, value, as_bool=False):
                if as_bool:
                    value = int(bool(value))
                attribute = self._get_attribute_object(key)
                if attribute is None:
                    holder = factory.holder_resolver(self)
                    attribute = factory.attribute_class.objects.create(
                        holder=holder,
                        key=key,
                        value=value
                    )
                else:
                    attribute.set_value(value)
                return attribute

            def _get_attribute_object(self, key):
                try:
                    holder = factory.holder_resolver(self)
                    attribute = holder.attributes.get(
                        holder=holder,
                        key=key
                    )
                except factory.attribute_class.DoesNotExist:
                    attribute = None
                return attribute

            def get_attribute(self, key, as_bool=False):
                attribute = self._get_attribute_object(key)
                value = attribute.value if attribute else factory.defaults.get(key, None)

                if as_bool:
                    try:
                        value = bool(int(value))
                    except TypeError:
                        value = False
                    except ValueError:
                        value = False
                return value

            def delete_attribute(self, key):
                attribute = self._get_attribute_object(key)
                if attribute:
                    attribute.delete()

            @CachedAttribute
            def attribute_fields(self):
                """Returns a list of attribute keys
                """
                return ()

            @CachedAttribute
            def boolean_attributes_lookup(self):
                """Returns a dictionary of attribute keys that are boolean values
                """
                return {}

        return AbstractAttributeHolderClass
