"""
GitHub reminder bot

Usage:
    python bots.py [-t TOKEN] [-o ORGANIZATION]
Examples:
    $ python bots.py -t YOURTOKEN -o hacktoolkit
"""

# Python Standard Library Imports
import getopt
import json
import random
import re
import sys

# Third Party (PyPI) Imports
import requests
from github import Github


# isort: off


class GitHubReminderBot(object):
    """GitHub Reminder bot

    Uses PyGithub as a base API client - http://pygithub.readthedocs.io/en/latest/index.html
    """

    def __init__(
        self,
        github_access_token,
        organizations=None,
        repositories=None,
        mention_here=False
    ):
        """Initializes the GitHub API client and prefetches the `organization` and repositories
        """
        self.github_access_token = github_access_token
        self.organizations = organizations
        self.repositories = repositories
        self.mention_here = mention_here

        self.cli = Github(self.github_access_token)

        self.repos = []

        if organizations:
            for organization in organizations:
                # http://pygithub.readthedocs.io/en/latest/github_objects/Organization.html#github.Organization.Organization.get_repos
                org = self.cli.get_organization(organization)
                self.repos.extend(org.get_repos(type='all'))

        if repositories:
            # https://pygithub.readthedocs.io/en/latest/github.html#github.MainClass.Github.get_repo
            for repository in repositories:
                try:
                    repo = self.cli.get_repo(repository)
                    self.repos.append(repo)
                except Exception as e:
                    print(e)

    def pull_request_reminder(self):
        """Returns a Markdown-formatted message for this organization's pull requests
        """
        from htk.utils.i18n import get_random_greeting
        greeting = get_random_greeting()

        def pluralize(s, num):
            plural_suffix = '' if num == 1 else 's'
            value = '%s %s' % (num, s + plural_suffix,)
            return value

        def should_exclude_pull_request(pull_request):
            title = pull_request.title.strip()
            m = re.match(r'^\[WIP\].*', title)
            should_exclude = m is not None
            return should_exclude

        def add_pull_request(repo, pull_request, reviews, has_approval, has_change, pr_list):
            # http://pygithub.readthedocs.io/en/latest/github_objects/PullRequest.html#github.PullRequest.PullRequest
            # https://api.slack.com/docs/message-formatting
            num_comments = pull_request.comments
            context = {
                'num' : len(pr_list) + 1,
                'repo_name' : repo.name,
                'pr_author' : pull_request.user.login,
                'pr_author_url' : pull_request.user.html_url,
                'pr_title' : pull_request.title,
                'pr_url' : pull_request.html_url,
                'num_comments' : pluralize('comment', num_comments),
            }

            msg = """%(num)s) [%(repo_name)s] <%(pr_author_url)s|%(pr_author)s> | <%(pr_url)s|%(pr_title)s> (%(num_comments)s)""" % context
            pr_list.append(msg)

        pull_requests_review = []
        pull_requests_change = []
        pull_requests_approve = []
        pull_requests_merge = []

        for repo in self.repos:
            # http://pygithub.readthedocs.io/en/latest/github_objects/Repository.html#github.Repository.Repository.get_pulls
            open_pull_requests = repo.get_pulls(state='open', sort='created', direction='desc')
            for pull_request in open_pull_requests:
                if should_exclude_pull_request(pull_request):
                    pass
                else:
                    # https://developer.github.com/v3/pulls/reviews/
                    reviews = pull_request.get_reviews()
                    has_approval = False
                    has_multiple_approvals = False
                    has_change = False
                    for review in reviews:
                        if review.state == 'APPROVED':
                            if has_approval:
                                has_multiple_approvals = True
                            else:
                                has_approval = True
                        elif review.state == 'CHANGES_REQUESTED':
                            has_change = True
                        elif review.state == 'COMMENTED':
                            pass
                        else:
                            print(review.state)

                    pr_list = pull_requests_change if has_change else pull_requests_merge if has_multiple_approvals else pull_requests_approve if has_approval else pull_requests_review
                    add_pull_request(repo, pull_request, reviews, has_approval, has_change, pr_list)

        attachments = []

        if len(pull_requests_review) > 0:
            attachments.append({
                'title' : '%s Pull Requests need to be reviewed:' % len(pull_requests_review),
                'text' : '\n'.join(pull_requests_review),
                'color' : 'warning',
            })

        if len(pull_requests_change) > 0:
            attachments.append({
                'title' : '%s Pull Requests require changes:' % len(pull_requests_change),
                'text' : '\n'.join(pull_requests_change),
                'color' : 'danger',
            })

        if len(pull_requests_approve) > 0:
            attachments.append({
                'title' : '%s Pull Requests need additional approvals:' % len(pull_requests_approve),
                'text' : '\n'.join(pull_requests_approve),
                'color' : '#439fe0',
            })

        if len(pull_requests_merge) > 0:
            attachments.append({
                'title' : '%s Pull Requests are ready to merge!' % len(pull_requests_merge),
                'text' : '\n'.join(pull_requests_merge),
                'color' : 'good',
            })

        PR_PRESENT_MESSAGES = [
            "Let's review some pull requests!",
            "It's code review time!",
        ]

        PR_ABSENT_MESSAGES = [
            "It's code review time... but what a shame, there are no pull requests to review :disappointed:. Let us write more code!",
            'No code reviews today. Enjoy the extra time! :sunglasses:',
        ]

        context = {
            'here' : '<!here> ' if self.mention_here and len(attachments) > 0 else '',
            'greeting' : greeting,
            'message' : random.choice(PR_PRESENT_MESSAGES) if len(attachments) > 0 else random.choice(PR_ABSENT_MESSAGES),
        }

        markdown_content = '%(here)s%(greeting)s Team!\n\n%(message)s' % context

        return (markdown_content, attachments,)


class GitHubReminderSlackBot(GitHubReminderBot):
    def __init__(
        self,
        slack_webhook_url,
        slack_channel,
        github_access_token,
        organizations=None,
        repositories=None,
        mention_here=False
    ):
        super(GitHubReminderSlackBot, self).__init__(
            github_access_token,
            organizations=organizations,
            repositories=repositories
        )
        self.slack_webhook_url = slack_webhook_url
        self.slack_channel = slack_channel

    def remind_pull_requests(self):
        markdown_content, attachments = self.pull_request_reminder()
        from htk.utils.text.converters import markdown2slack
        slack_text = markdown2slack(markdown_content)
        from htk.lib.slack.utils import webhook_call
        webhook_call(
            webhook_url=self.slack_webhook_url,
            channel=self.slack_channel,
            text=slack_text,
            attachments=attachments,
            username='GitHub Reminder Bot',
            icon_emoji=':octocat:',
            unfurl_links=False
        )


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv = None):
    OPT_STR = 'ht:o:'
    OPT_LIST = [
        'help',
        'token=',
        'org=',
    ]
    token = None
    org = None
    if argv is None:
        argv = sys.argv
    try:
        try:
            progname = argv[0]
            opts, args = getopt.getopt(argv[1:],
                                       OPT_STR,
                                       OPT_LIST)
        except getopt.error as msg:
             raise Usage(msg)
        # process options
        for o, a in opts:
            if o in ('-h', '--help'):
                print(__doc__)
                sys.exit(0)
            elif o in ('-t', '--token'):
                token = a
            elif o in ('-o', '--org'):
                org = a
        if token and org:
            bot = GitHubReminderBot(token, org)
            print(bot.pull_request_reminder())
        else:
            raise Usage('Incorrect arguments')

    except Usage as err:
        print(err.msg, file=sys.stderr)
        print('for help use --help', file=sys.stderr)
        return 3.14159

if __name__ == '__main__':
    main()
