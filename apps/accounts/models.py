import datetime
import pytz
import random
import rollbar
from hashlib import sha1

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from htk.apps.accounts.cachekeys import UserFollowersCache
from htk.apps.accounts.cachekeys import UserFollowingCache
from htk.apps.accounts.constants import *
from htk.apps.accounts.emails import activation_email
from htk.apps.accounts.emails import welcome_email
from htk.apps.accounts.enums import ProfileAvatarType
from htk.apps.accounts.utils import encrypt_uid
from htk.models import AbstractAttribute
from htk.models import AbstractAttributeHolderClassFactory
from htk.utils import extract_request_ip
from htk.utils import htk_setting
from htk.utils import utcnow
from htk.utils.request import get_current_request

class UserAttribute(AbstractAttribute):
    holder = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='attributes')

    class Meta:
        app_label = 'accounts'
        verbose_name = 'User Attribute'
        unique_together = (
            ('holder', 'key',),
        )

    def __unicode__(self):
        value = '%s (%s)' % (self.key, self.holder)
        return value

UserAttributeHolder = AbstractAttributeHolderClassFactory(
    UserAttribute,
    holder_resolver=lambda self: self.user
).get_class()

class BaseAbstractUserProfile(models.Model, UserAttributeHolder):
    """
    django.contrib.auth.models.User does not have a unique email
    """
    # TODO: related_name="%(app_label)s_%(class)s_related"
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    has_username_set = models.BooleanField(default=False)

    timezone = models.CharField(max_length=64, choices=[(tz, tz,) for tz in pytz.common_timezones], blank=True, default='America/Los_Angeles')

    # tracking
    last_login_ip = models.CharField(max_length=15, blank=True)
    # http://en.wikipedia.org/wiki/ISO_3166-2
    detected_country = models.CharField(max_length=2, blank=True)
    detected_timezone = models.CharField(max_length=36, blank=True)

    # meta
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        #s = '%d: %s' % (self.user.id, self.user.email,)
        s = self.user.__unicode__()
        return s

    ##
    # name
    def get_full_name(self):
        name_parts = [
            self.user.first_name.strip(),
            self.user.last_name.strip(),
        ]
        full_name = ' '.join(name_parts).strip()
        return full_name

    def get_first_name_last_initial(self):
        first_name_part = self.user.first_name.strip()
        last_name_part = self.user.last_name.strip()[:1]
        last_name_part += '.' if last_name_part else ''

        name_parts = [
            first_name_part,
            last_name_part,
        ]
        name = ' '.join(name_parts).strip()
        return name

    def get_display_name(self):
        display_name = self.get_display_username()
        return display_name

    def get_display_username(self):
        display_username = self.user.username if self.has_username_set else htk_setting('HTK_ACCOUNTS_DEFAULT_DISPLAY_NAME')
        return display_username

    def get_nav_display_name(self):
        """Gets the name to be displayed to the user in app navigation context
        """
        display_name = self.get_display_name()
        if display_name.strip() == '':
            display_name = self.user.username if self.has_username_set else self.user.email
        return display_name

    def get_org_display_name(self):
        """Gets the name to be displayed to other users in Organization context
        """
        display_name = '%s (%s)' % (self.get_full_name(), self.user.username,)
        return display_name

    def has_completed_account_setup(self, require_name=False):
        """Determines whether this User has completed the minimum account setup:
        - has a primary email address set
        - has username set

        Optional:
        - has first and last name set
        """
        # TODO: cache this, perhaps?
        # the tricky part is figuring out all the places where we should invalidate the cache
        user = self.user
        value = self.has_primary_email() and self.has_username_set
        if require_name:
            value = value and user.first_name and user.last_name
        else:
            pass
        return value

    ##
    # emails

    def has_email(self, email):
        """Determine whether this User owns `email`
        """
        user_email = get_user_email(self.user, email)
        has_email = user_email and user_email.is_confirmed
        return has_email

    def set_primary_email(self, email):
        """Set the primary email address for `self.user`
        This is typically called from UserEmail.set_primary_email

        Assumes that there is no other auth.User with this email, so doesn't check
        """
        user = self.user
        if self.has_email(email):
            user.email = email
            user.save()
        else:
            pass
        return user

    def has_primary_email(self):
        """Determines whether this `User` has a primary email set
        """
        primary_email = self.get_primary_email()
        value = primary_email is not None
        return value

    def get_primary_email(self):
        """Retrieve this `User`'s primary email
        """
        email = self.user.email
        if email and self.has_email(email):
            primary_email = email
        else:
            primary_email = None
        return primary_email

    def get_nonprimary_emails(self):
        """Returns a list of UserEmail objects associated with `self.user`, besides the primary email
        We can just get primary email from self.get_primary_email()
        """
        # TODO: cache this
        primary_email = self.get_primary_email()
        if primary_email:
            user_emails = self.user.emails.exclude(email=primary_email).order_by('-is_confirmed', 'id')
        else:
            user_emails = self.user.emails.order_by('-is_confirmed', 'id')
        return user_emails

    def get_confirmed_emails(self):
        user = self.user
        user_emails = user.emails.filter(is_confirmed=True)
        return user_emails

    def get_gravatar_hash(self):
        primary_email = self.get_primary_email()
        if primary_email:
            from htk.lib.gravatar.utils import get_gravatar_hash
            gravatar_hash = get_gravatar_hash(primary_email)
        else:
            gravatar_hash = ''
        return gravatar_hash

    # send emails

    def send_activation_reminder_email(self, template=None, subject=None, sender=None):
        user_email = get_user_email(self.user, self.user.email)
        user_email.send_activation_reminder_email(template=template, subject=subject, sender=sender)

    def send_welcome_email(self, template=None, subject=None, sender=None):
        """Sends a welcome email to the user
        """
        try:
            welcome_email(self.user, template=template, subject=subject, sender=sender)
        except:
            request = get_current_request()
            rollbar.report_exc_info(request=request)

    ##
    # social auth stuff

    def get_social_auths(self):
        """Gets all associated UserSocialAuth objects
        """
        from social_django.models import UserSocialAuth
        social_auths = UserSocialAuth.objects.filter(user__id=self.user.id)
        return social_auths

    def get_social_user(self, provider, provider_id=None):
        from social_django.models import UserSocialAuth
        try:
            if provider_id:
                social_user = UserSocialAuth.objects.get(
                    user__id=self.user.id,
                    provider=provider,
                    uid=provider_id
                )
            else:
                social_user = UserSocialAuth.objects.get(
                    user__id=self.user.id,
                    provider=provider
                )
        except UserSocialAuth.DoesNotExist:
            social_user = None
        return social_user

    def get_fb_social_user(self):
        """Gets a Facebook UserSocialAuth
        """
        social_user = self.get_social_user(SOCIAL_AUTH_PROVIDER_FACEBOOK)
        return social_user

    def get_fbid(self):
        """Gets a user's Facebook id
        """
        fbid = None
        social_user = self.get_fb_social_user()
        if social_user:
            fbid = social_user.uid
        return fbid

    def get_tw_social_user(self):
        """Gets a Twitter UserSocialAuth
        """
        social_user = self.get_social_user(SOCIAL_AUTH_PROVIDER_TWITTER)
        return social_user

    def get_twid(self):
        """Gets a user's Twitter id
        """
        twid = None
        social_user = self.get_tw_social_user()
        if social_user:
            twid = social_user.uid
        return twid

    def get_social_auth_linkedin(self):
        from social_django.models import UserSocialAuth
        social_auth = UserSocialAuth.objects.get(user__id=self.user.id, provider=SOCIAL_AUTH_PROVIDER_LINKEDIN)
        return social_auth

    def has_social_auth_connected(self, provider):
        social_auths = self.get_social_auths()
        has_connected = social_auths.filter(provider=provider).exists()
        return has_connected

    def has_social_auth_facebook(self):
        # TODO: cache this
        has_facebook = self.has_social_auth_connected(SOCIAL_AUTH_PROVIDER_FACEBOOK)
        return has_facebook

    def has_social_auth_linkedin(self):
        # TODO: cache this
        has_linkedin = self.has_social_auth_connected(SOCIAL_AUTH_PROVIDER_LINKEDIN)
        return has_linkedin

    def has_social_auth_twitter(self):
        # TODO: cache this
        has_twitter = self.has_social_auth_connected(SOCIAL_AUTH_PROVIDER_TWITTER)
        return has_twitter

    def can_disconnect_social_auth(self):
        """Returns whether the user can disconnect at least one social auth
        True if:
        - user has (a usuable password set + confirmed email)
        - user has multiple connected social auths
        """
        can_disconnect = False
        if self.user.has_usable_password() and self.user.emails.filter(is_confirmed=True).exists():
            can_disconnect = True
        else:
            social_auths = self.get_social_auths()
            can_disconnect = social_auths.count() > 1
        return can_disconnect

    ##
    # Organizations
    # These methods only work if using htk.apps.organizations

    def get_organizations(self):
        from htk.utils.general import resolve_model_dynamically
        Organization = resolve_model_dynamically(htk_setting('HTK_ORGANIZATION_MODEL'))
        organizations = Organization.objects.filter(members__user=self.user, members__active=True)
        return organizations

    ##
    # meta stuff

    def activate(self, email_template=None, email_subject=None, email_sender=None):
        """Activate the User if not already activated
        """
        was_activated = False
        user = self.user
        if not user.is_active:
            user.is_active = True
            user.save()
            was_activated = user.is_active
        if was_activated:
            self.send_welcome_email(template=email_template, subject=email_subject, sender=email_sender)
        return was_activated

    def get_timezone(self):
        tz = self.timezone if self.timezone else self.get_detected_timezone()
        return tz

    def get_django_timezone(self):
        tz = self.get_timezone()
        django_timezone = pytz.timezone(tz)
        return django_timezone

    def get_detected_country(self):
        country = self.detected_country or htk_setting('HTK_DEFAULT_COUNTRY')
        return country

    def get_detected_timezone(self):
        tz = self.detected_timezone or htk_setting('HTK_DEFAULT_TIMEZONE')
        return tz

    def get_local_time(self, dt=None):
        """Gets the current local time for User
        If `dt` is specified, format `dt` into User's timezone
        """
        tz = self.get_django_timezone()
        if dt is None:
            local_time = utcnow().astimezone(tz)
        else:
            local_time = dt.astimezone(tz)
        return local_time

    def update_locale_info_by_ip_from_request(self, request):
        """Update user info by IP Address
        
        Store last_login_ip only when logging in
        Store country resolved from IP
        Store timezone resolved from IP
        
        Caller: api.auth.decorators.register_or_login_user
        
        Unknown whether this code throws an exception, but catch it upstream if any
        """
        try:
            ip = extract_request_ip(request)
            if ip and self.last_login_ip != ip:
                self.last_login_ip = ip
                try:
                    from htk.lib.geoip.utils import get_country_code_by_ip
                    from htk.lib.geoip.utils import get_timezone_by_ip
                    detected_country = get_country_code_by_ip(ip) or ''
                    detected_timezone = get_timezone_by_ip(ip) or ''
                    self.detected_country = detected_country
                    self.detected_timezone = detected_timezone
                except:
                    # couldn't find geoip records for ip, just be quiet for now
                    pass
                finally:
                    self.save()
        except:
            # error extracting IP or saving
            rollbar.report_exc_info(request=request)

class AbstractUserProfile(BaseAbstractUserProfile):
    share_name = models.BooleanField(default=False)

    # location info
    address = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.CharField(max_length=5, blank=True)
    share_location = models.BooleanField(default=False)

    # profile, links, and social
    avatar = models.PositiveIntegerField(default=ProfileAvatarType.GRAVATAR.value)
    website = models.CharField(max_length=128, blank=True)
    facebook = models.CharField(max_length=32, blank=True)
    twitter = models.CharField(max_length=32, blank=True)
    biography = models.TextField(max_length=2000, blank=True)

    # community
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True)

    class Meta:
        abstract = True

    def get_display_name(self):
        display_name = super(AbstractUserProfile, self).get_display_name()

        if self.share_name:
            full_name = self.get_full_name()
            if full_name:
                display_name = full_name

        return display_name

    def get_avatar_type(self):
        avatar_type = ProfileAvatarType(self.avatar).name
        return avatar_type

    # followers/following
    def follow_user(self, user):
        self.following.add(user)
        # invalidate caches
        following_cache = UserFollowingCache(prekey=self.user.id)
        following_cache.invalidate_cache()
        followers_cache = UserFollowersCache(prekey=user.id)
        followers_cache.invalidate_cache()

    def unfollow_user(self, user):
        self.following.remove(user)
        # invalidate caches
        following_cache = UserFollowingCache(prekey=self.user.id)
        following_cache.invalidate_cache()
        followers_cache = UserFollowersCache(prekey=user.id)
        followers_cache.invalidate_cache()

    def get_following(self):
        """Gets User following
        Returns a list of User objects
        """
        c = UserFollowingCache(prekey=self.user.id)
        following = c.get()
        if following is None:
            following = self.following.all()
            c.cache_store(following)
        return following

    def get_followers(self):
        """Gets User followers
        Returns a list of User objects
        """
        prekey = [self.user.id,]
        c = UserFollowersCache(prekey=self.user.id)
        followers = c.get()
        if followers is None:
            follower_profiles = self.user.followers.all()
            followers = [profile.user for profile in follower_profiles]
            c.cache_store(followers)
        return followers

    def has_follower(self, user=None):
        """Check if the currently logged-in user is following self.user
        """
        if user is None:
            request = get_current_request()
            user = request.user
        else:
            pass
        if user:
            value = user.profile.get_following().filter(id=self.user.id).exists()
        else:
            value = False
        return value

    def get_follow_uri(self):
        follow_user_url_name = htk_setting('HTK_API_USERS_FOLLOW_URL_NAME')
        follow_uri = reverse(follow_user_url_name, args=(encrypt_uid(self.user),))
        return follow_uri

    def get_unfollow_uri(self):
        unfollow_user_url_name = htk_setting('HTK_API_USERS_UNFOLLOW_URL_NAME')
        unfollow_uri = reverse(unfollow_user_url_name, args=(encrypt_uid(self.user),))
        return unfollow_uri

class UserEmail(models.Model):
    """A User can have multiple email addresses using this table

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emails')
    email = models.EmailField(_('email address'))
    # set in self._reset_activation_key()
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        app_label = 'accounts'
        verbose_name = 'User Email'
        unique_together = (
            ('user', 'email',),
        )

    def __unicode__(self):
        s = '%s, %s' % (self.user, self.email,)
        return s

    def _reset_activation_key(self, resend=False):
        """Resets the activation key

        `resend` whether this key is being reset as the result of a resend confirmation email

        If `resend`, then check the `key_expires` timestamp to see if we should reuse the existing activation key, or generate a new one
        """
        should_reset = True
        if resend and self.activation_key and self.key_expires:
            now = utcnow()
            if now < self.key_expires:
                # do not reset key if remaining time has not fallen below threshold
                remaining_time = self.key_expires - now
                threshold = datetime.timedelta(hours=EMAIL_ACTIVATION_KEY_REUSE_THRESHOLD_HOURS)
                should_reset = remaining_time < threshold

        if should_reset:
            user = self.user
            salt = sha1(str(random.random())).hexdigest()[:5]
            activation_key = sha1(salt + user.username).hexdigest()
            key_expires = utcnow() + datetime.timedelta(hours=EMAIL_ACTIVATION_KEY_EXPIRATION_HOURS)

            self.activation_key = activation_key
            self.key_expires = key_expires
            self.save()
        else:
            # no need to reset activation key, use the same one
            pass

    def is_primary(self):
        """Determines whether this UserEmail is the primary email address of `self.user`
        """
        value = self.is_confirmed and self.user.email == self.email
        return value

    def set_primary_email(self):
        """Sets the primary email address of `self.user` to `self.email`
        """
        user = self.user
        if self.is_confirmed:
            # only able to set primary email address to this one if it has been confirmed
            email = self.email
            user = user.profile.set_primary_email(email)
        else:
            user = None
        return user

    def delete(self, *args, **kwargs):
        """Deletes this associated email address

        Can only be deleted if not the primary email address
        """
        user = self.user
        if user.email != self.email:
            super(UserEmail, self).delete(*args, **kwargs)
            result = True
        else:
            result = False
        return result

    def send_activation_email(self, domain=None, resend=False, template=None, subject=None, sender=None):
        """Sends an activation email
        """
        domain = domain or htk_setting('HTK_DEFAULT_EMAIL_SENDING_DOMAIN')
        self._reset_activation_key(resend=resend)
        activation_email(self, domain=domain, template=template, subject=subject, sender=sender)

    def send_activation_reminder_email(self, template=None, subject=None, sender=None):
        """Sends an account activation reminder email

        Piggybacks off of `self.send_activation_email`
        """
        if template is None:
            template = htk_setting('HTK_ACCOUNT_ACTIVATION_REMINDER_EMAIL_TEMPLATE')
        if subject is None:
            subject = 'Reminder to activate your account on %s' % htk_setting('HTK_SITE_NAME')
        self.send_activation_email(resend=True, template=template, subject=subject, sender=sender)

    def confirm_and_activate_account(self, email_template=None, email_subject=None, email_sender=None):
        """Confirms the email address, and activates the associated account if not already activated

        Side effect: Once an email address is confirmed by an account, no other accounts can have that email address in a pending (unconfirmed state)
        """
        # TODO: what if an account was purposefully deactivated? we should not activate it. but how would we know the difference?
        if not self.is_confirmed:
            self.is_confirmed = True
            self.save()
        was_activated = self.user.profile.activate(email_template=email_template, email_subject=email_subject, email_sender=email_sender)
        # purge all other records with same email addresses that aren't confirmed
        # NOTE: Be careful to not delete the wrong ones!
        UserEmail.objects.filter(email=self.email, is_confirmed=False).delete()
        return was_activated

####################
# Import these last to prevent circular import
from htk.apps.accounts.utils import get_user_email
