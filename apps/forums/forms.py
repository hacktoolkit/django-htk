from django import forms

from htk.apps.forums.models import Forum
from htk.apps.forums.models import ForumMessage
from htk.apps.forums.models import ForumThread

class ThreadCreationForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = ForumThread

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        self.subject = subject
        return subject

    def clean_message(self):
        message = self.cleaned_data['message']
        self.message = message
        return message

    def save(self, author=None, forum=None):
        subject = self.subject
        text = self.message
        thread = ForumThread.objects.create(
            forum=forum,
            author=author,
            subject=subject,
        )
        thread.save()
        message = ForumMessage.objects.create(
            thread=thread,
            author=author,
            text=text
        )
        message.save()
        return thread

class MessageCreationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data['message']
        self.message = message
        return message

    def save(self, author=None, thread=None):
        text = self.message
        message = ForumMessage.objects.create(
            thread=thread,
            author=author,
            text=text
        )
        message.save()
        return message
