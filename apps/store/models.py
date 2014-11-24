from django.db import models

class AbstractProduct(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1000, blank=True)
    editor_notes = models.TextField(max_length=1000, blank=True)
    # 3rd party
    amazon_product_id = models.CharField(max_length=64)

    # meta
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        value = self.name
        return value
