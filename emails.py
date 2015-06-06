import inspect

from django.template import TemplateDoesNotExist
from django.template.loader import get_template

from htk.mailers import send_email

class BaseBatchRelationshipEmails(object):
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

    def has_cooldown(self, user):
        """Checks whether cooldown timer is still going for `user`
        """
        prekey = user.id
        c = self.cooldown_class(prekey)
        _has_cooldown = bool(c.get())
        return _has_cooldown

    def reset_cooldown(self, user):
        """Resets cooldown timer for this `user`

        Returns whether cooldown was reset, False if timer was still running
        """
        prekey = user.id
        c = self.cooldown_class(prekey)
        if c.get():
            was_reset = False
        else:
            c.cache_store()
            was_reset = True
        return was_reset

    def get_recipients(self):
        """Returns a list or QuerySet of User objects

        Should be overridden
        """
        users = []
        return users

    def get_subject(self, recipient):
        """Returns the email subject line for `recipient`

        Should be overridden
        """
        subject = ''
        return subject

    def get_email_context(self, recipient):
        """Returns a dictionary for the email context
        """
        context = {}
        return context

    def _craft_email_params(self, recipient):
        """Build the email params for rendering this BatchRelationshipEmail
        """
        recipients = [recipient.email,]
        subject = self.get_subject(recipient)

        context = {
            'user' : recipient,
            'subject' : subject,
        }
        context.update(self.get_email_context(recipient))
        email_params = {
            'template' : self.template,
            'recipients' : recipients,
            'context' : context,
        }
        return email_params

    def send_email(self, recipient):
        """Workhorse function called by `self.send_emails for`
        sending to one `recipient`

        Can be overridden
        """
        email_params = self._craft_email_params(recipient)
        context = email_params.get('context', {})
        send_email(
            template=email_params.get('template'),
            subject=context.get('subject'),
            to=email_params.get('recipients', []),
            context=context
        )

    def send_emails(self):
        """Send the batch of emails
        """
        recipients = self.get_recipients()
        for recipient in recipients:
            if self.has_cooldown(recipient):
                # cooldown has not elapsed yet, don't send mail too frequently
                pass
            else:
                # cache right before we send, since each send operation costs a non-zero overhead
                self.reset_cooldown(recipient)
                self.send_email(recipient)
