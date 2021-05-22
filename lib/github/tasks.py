# HTK Imports
from htk.constants.time import (
    BUSINESS_HOURS_START,
    ISOWEEKDAY_WEEKDAYS,
    MORNING_HOURS_END,
)
from htk.tasks import BaseTask
from htk.utils.text.transformers import get_symbols


# isort: off


class GitHubReminderTask(BaseTask):
    def __init__(self):
        from htk.lib.github.cachekeys import GitHubReminderCooldown
        super(GitHubReminderTask, self).__init__(cooldown_class=GitHubReminderCooldown)

    def has_cooldown(self, user):
        _has_cooldown = super(GitHubReminderTask, self).has_cooldown(user)
        #_has_cooldown = False
        return _has_cooldown

    def get_users(self):
        import htk.apps.accounts.filters as _filters
        from htk.apps.accounts.utils.lookup import get_users_with_attribute_value
        users = get_users_with_attribute_value('github_reminders', True, as_bool=True)
        users = _filters.users_currently_at_local_time(users, BUSINESS_HOURS_START, MORNING_HOURS_END, isoweekdays=ISOWEEKDAY_WEEKDAYS)

        return users

    def execute(self, user):
        now = user.profile.get_local_time()

        valid_chars = 'A-Za-z0-9_\-/'
        github_organizations = get_symbols(
            user.profile.get_attribute('github_organizations') or '',
            valid_chars=valid_chars
        )
        github_repositories = get_symbols(
            user.profile.get_attribute('github_repositories') or '',
            valid_chars=valid_chars
        )

        self.send_github_reminders(
            user,
            organizations=github_organizations,
            repositories=github_repositories
        )

    def send_github_reminders(self, user, organizations=None, repositories=None):
        github_access_token = user.profile.get_attribute('github_access_token')
        slack_webhook_url = user.profile.get_attribute('slack_webhook_url')
        slack_channel = user.profile.get_attribute('github_reminders_slack_channel')

        from htk.lib.github.bots import GitHubReminderSlackBot
        bot = GitHubReminderSlackBot(
            slack_webhook_url,
            slack_channel,
            github_access_token,
            organizations=organizations,
            repositories=repositories
        )
        bot.remind_pull_requests()
