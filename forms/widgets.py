# Django Imports
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe


# Deprecated in Django 1.11
# forms.widgets.RadioChoiceInput
# https://docs.djangoproject.com/en/2.0/releases/1.11/#changes-due-to-the-introduction-of-template-based-widget-rendering
#class StarRatingRadioChoiceInput(forms.widgets.RadioChoiceInput):
class StarRatingRadioChoiceInput(object):
    def render(self, name=None, value=None, attrs=None, choices=()):
        if self.id_for_label:
            label_for = format_html(' for="{}"', self.id_for_label)
        else:
            label_for = ''
        attrs = dict(self.attrs, **attrs) if attrs else self.attrs
        # TODO: some kind of double encoding is happening, somehow
        #result = format_html(
        #    '<label{}></label>{}', label_for, self.tag(attrs)
        #)
        result = mark_safe('<label%s></label>%s' % (label_for, self.tag(attrs),))
        return result

# Deprecated
#class StarRatingRadioChoiceFieldRenderer(forms.widgets.RadioFieldRenderer):
class StarRatingRadioChoiceFieldRenderer(object):
    choice_input_class = StarRatingRadioChoiceInput
    outer_html = '<span{id_attr} class="star-rating">{content}</span>'
    inner_html = '{choice_value}'

class StarRatingRadioSelect(forms.RadioSelect):
    renderer = StarRatingRadioChoiceFieldRenderer

    def __init__(self, *args, **kwargs):
        #super(StarRatingRadioSelect, self).__init__(choices=self.get_choices(min_value, max_value), *args, **kwargs)
        super(StarRatingRadioSelect, self).__init__(*args, **kwargs)

    def get_choices(self, min_value, max_value):
        choices = [('', '',),]
        for rating in range(min_value, max_value + 1):
            choices.append((rating, rating,))
        return choices
