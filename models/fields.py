from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

class StarRatingField(models.PositiveIntegerField):
    def __init__(self, min_value=1, max_value=5, *args, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        super(StarRatingField, self).__init__(
            blank=True,
            null=True,
            validators=[
                MinValueValidator(min_value),
                MaxValueValidator(max_value),
            ],
            *args,
            **kwargs
        )

    def formfield(self, **kwargs):
        import htk.forms.fields
        defaults = {
            'min_value' : self.min_value,
            'max_value' : self.max_value,
            'form_class' : htk.forms.fields.StarRatingField,
        }
        defaults.update(kwargs)
        return super(StarRatingField, self).formfield(**defaults)
