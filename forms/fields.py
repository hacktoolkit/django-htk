from django import forms

from htk.forms.widgets import StarRatingRadioSelect

BOOL_CHOICES_TRUE_FALSE = ((False, 'False',), (True, 'True',),)
BOOL_CHOICES_ON_OFF = ((False, 'Off',), (True, 'On',),)
BOOL_CHOICES_YES_NO = ((False, 'No',), (True, 'Yes',),)

class BooleanChoiceField(forms.TypedChoiceField):
    def __init__(self, choices=BOOL_CHOICES_TRUE_FALSE, *args, **kwargs):
        super(BooleanChoiceField, self).__init__(
            choices=choices,
            coerce=lambda x: x =='True',
            empty_value=False
        )

class BooleanOnOffField(BooleanChoiceField):
    def __init__(self, *args, **kwargs):
        super(BooleanOnOffField, self).__init__(choices=BOOL_CHOICES_ON_OFF, *args, **kwargs)

class BooleanYesNoField(BooleanChoiceField):
    def __init__(self, *args, **kwargs):
        super(BooleanYesNoField, self).__init__(choices=BOOL_CHOICES_YES_NO, *args, **kwargs)

class StarRatingField(forms.IntegerField):
    widget = StarRatingRadioSelect

    def __init__(self, *args, **kwargs):
        super(StarRatingField, self).__init__(*args, **kwargs)
        self.widget.choices = self.get_choices()

    def get_choices(self):
        choices = [('', '',),]
        for rating in xrange(self.min_value, self.max_value + 1):
            choices.append((rating, rating,))
        return choices
