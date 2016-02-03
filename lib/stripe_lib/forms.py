from django import forms

from htk.forms.utils import set_input_attrs
from htk.forms.utils import set_input_placeholder_labels

class CreditCardForm(forms.Form):
    """A basic form for entering credit card numbers
    """
    name = forms.CharField(max_length=128, label='Name on Card')
    number = forms.CharField(max_length=16, label='Credit Card Number', widget=forms.TextInput(attrs={ 'type': 'tel', }))
    exp_month = forms.CharField(max_length=2, label='Exp Month', widget=forms.TextInput(attrs={ 'type': 'tel', 'placeholder': 'MM', }))
    exp_year = forms.CharField(max_length=4, label='Exp Year', widget=forms.TextInput(attrs={ 'type': 'tel', 'placeholder': 'YYYY', }))
    cvc = forms.CharField(max_length=4, label='CVC', widget=forms.TextInput(attrs={ 'type': 'tel', 'placeholder': 'CVC', }))

    def __init__(self, *args, **kwargs):
        super(CreditCardForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        set_input_placeholder_labels(self)
        set_input_attrs(self)

    def get_stripe_card_dict(self):
        """Get a dictionary representing this card compatible with Stripe's format
        """
        card_dict = {
            'object' : 'card',
            'number' : self.cleaned_data['number'],
            'exp_month' : self.cleaned_data['exp_month'],
            'exp_year' : self.cleaned_data['exp_year'],
            'cvc' : self.cleaned_data['cvc'],
            'name' : self.cleaned_data['name'],
        }
        return card_dict
