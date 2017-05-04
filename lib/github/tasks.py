from htk.constants.time import *
from htk.tasks import BaseTask

class GitHubReminderTask(BaseTask):
    def __init__(self):
        from htk.lib.github.cachekeys import GitHubReminderCooldown
        super(GitHubReminderTask, self).__init__(cooldown_class=GitHubReminderCooldown)

    def has_cooldown(self, user):
        _has_cooldown = super(GitHubReminder, self).has_cooldown(user)
        #_has_cooldown = False
        return _has_cooldown

    def get_users(self):
        import htk.apps.accounts.filters as _filters
        from htk.apps.accounts.utils.lookup import get_users_with_attribute_value
        users = get_users_with_attribute_value('github_reminders', 1)
        users = _filters.users_currently_at_local_time(users, MID_MORNING_HOURS_START, MID_MORNING_HOURS_END, isoweekdays=ISOWEEKDAY_WEEKDAYS)

        return users

    def execute(self, user):
        now = user.profile.get_local_time()
        github_organizations = user.profile.get_attribute('github_organizations').split('\n')
        github_organizations = [organization.strip() for organization in github_organizations]
        for organization in github_organizations:
            self.send_github_reminders(user, organization)

    def send_github_reminders(self, user, organization):
        github_access_token = user.profile.get_attribute('github_access_token')
        slack_webhook_url = user.profile.get_attribute('slack_webhook_url')
        slack_channel = user.profile.get_attribute('github_reminders_slack_channel')

        from htk.lib.github.bots import GitHubReminderSlackBot
        bot = GitHubReminderSlackBot(github_access_token, organization, slack_webhook_url, slack_channel)
        bot.remind_pull_requests()
