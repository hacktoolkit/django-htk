from django import forms

from htk.forms.widgets import StarRatingRadioSelect

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
