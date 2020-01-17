# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django import forms

# HTK Imports
from htk.apps.feedback.emails import feedback_email
from htk.apps.feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea, required=False, label="Your thoughts?")
    email = forms.EmailField(required=False, label="Your email address (only if you want a reply)")

    class Meta:
        model = Feedback
        fields = (
            'user',
            'name',
            'comment',
            'email',
        )
        widgets = {
            'user' : forms.HiddenInput,
        }

    def save(self, site, request, commit=True):
        domain = request.get_host()
        uri = request.META.get('HTTP_REFERER', '')

        feedback = super(FeedbackForm, self).save(commit=False)
        feedback.site = site
        feedback.uri = uri
        feedback.save()

        try:
            feedback_email(feedback, domain=domain)
        except:
            rollbar.report_exc_info(request=request)
        return feedback
