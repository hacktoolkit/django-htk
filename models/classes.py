import json

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from htk.utils import utcnow

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

    ##
    # URLs

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        url = reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.id,))
        return url

    def get_absolute_url(self):
        raise Exception('Not implemented')

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
                    except TypeError, ValueError:
                        value = False
                return value

            def delete_attribute(self, key):
                attribute = self._get_attribute_object(key)
                if attribute:
                    attribute.delete()

            def get_attribute_keys(self):
                """Returns a list of attribute keys
                """
                return ()

            def get_boolean_attributes_lookup(self):
                """Returns a dictionary of attribute keys that are boolean values
                """
                return {}

        return AbstractAttributeHolderClass
