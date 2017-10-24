import inspect
import rollbar

from django.template import TemplateDoesNotExist
from django.template.loader import get_template

from htk.tasks import BaseTask
from htk.mailers import send_email

class BaseBatchRelationshipEmails(BaseTask):
    """
    Relationship emails are related to transactional emails, but usually happen asynchronously or offline, apart from direct web requests

    Examples:
    - Daily or weekly updates
    - Drip reminders
    - Account status reports
    - Shopping cart abandonment reminders

    References:
    - http://blog.mailchimp.com/what-is-transactional-email/
    - https://www.ftc.gov/tips-advice/business-center/guidance/can-spam-act-compliance-guide-business
    """
    def __init__(self, cooldown_class=None, template=None):
        # set cooldown_class
        from htk.cachekeys import BatchRelationshipEmailCooldown
        if inspect.isclass(cooldown_class) and issubclass(cooldown_class, BatchRelationshipEmailCooldown):
            self.cooldown_class = cooldown_class
        else:
            self.cooldown_class = BatchRelationshipEmailCooldown

        # set template
        if template:
            self.template = template
            template_name = 'emails/%s.html' % template
            # try to get the template... otherwise fail now before processing emails
            tpl = get_template(template_name)
            self.tpl = tpl
        else:
            raise TemplateDoesNotExist('Unspecified template')

    def get_email_batch_cooldown_prekey(self, user, **kwargs):
        prekey = ['email_batch', user.id,]
        kw_values = [kwargs[key] for key in sorted(kwargs.keys())]
        prekey += kw_values
        return prekey

    def has_email_batch_cooldown(self, user, **kwargs):
        """Checks whether cooldown timer is still going for the email batch for `user` and `kwargs`
        """
        prekey = self.get_email_batch_cooldown_prekey(user, **kwargs)
        c = self.cooldown_class(prekey)
        _has_cooldown = bool(c.get())
        return _has_cooldown

    def reset_email_batch_cooldown(self, user, **kwargs):
        """Resets cooldown timer for email batch for `user` and `kwargs`

        Returns whether cooldown was reset, False if timer was still running
        """
        prekey = self.get_email_batch_cooldown_prekey(user, **kwargs)
        c = self.cooldown_class(prekey)
        if c.get():
            was_reset = False
        else:
            c.cache_store()
            was_reset = True
        return was_reset

    def get_users(self):
        users = self.get_recipients()
        return users

    def get_recipient_email_batches_data(self, recipient):
        """Gets data about each email for the `recipient`

        Use cases. A recipient can receive multiple emails if:
        - recipient has multiple "sub-accounts"

        Returns a list of dictionaries
        """
        return [{}]

    def get_recipients(self):
        """Returns a list or QuerySet of User objects

        Should be overridden
        """
        users = super(BaseTask, self).get_users()
        return users

    def execute(self, user):
        """Send out emails for `user`

        One `user` may receive one or many emails
        """
        recipient = user
        email_batches_data = self.get_recipient_email_batches_data(recipient)
        for email_batch_data in email_batches_data:
            try:
                if self.has_email_batch_cooldown(recipient, **email_batch_data):
                    pass
                else:
                    self.send_email(recipient, **email_batch_data)
                    self.reset_email_batch_cooldown(recipient, **email_batch_data)
            except:
                extra_data = {
                    'user' : user,
                    'email_batch_data' : email_batch_data,
                }
                rollbar.report_exc_info(extra_data=extra_data)

    def send_email(self, recipient, **kwargs):
        """Workhorse function called by `self.send_emails` for
        sending to one `recipient`

        Can be overridden
        """
        email_params = self._craft_email_params(recipient, **kwargs)
        context = email_params.get('context', {})
        send_email(
            template=email_params.get('template'),
            subject=context.get('subject'),
            to=email_params.get('recipients', []),
            context=context
        )

    def get_subject(self, recipient, **kwargs):
        """Returns the email subject line for `recipient`

        Should be overridden
        """
        subject = ''
        return subject

    def get_email_context(self, recipient, **kwargs):
        """Returns a dictionary for the email context
        """
        context = {}
        return context

    def _craft_email_params(self, recipient, **kwargs):
        """Build the email params for rendering this BatchRelationshipEmail
        """
        recipients = [recipient.email,]
        subject = self.get_subject(recipient, **kwargs)

        context = {
            'user' : recipient,
            'subject' : subject,
        }
        context.update(self.get_email_context(recipient, **kwargs))
        email_params = {
            'template' : self.template,
            'recipients' : recipients,
            'context' : context,
        }
        return email_params
