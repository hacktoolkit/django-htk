#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
GitHub reminder bot

Usage:
    python bots.py [-t] TOKEN -o ORGANIZATION
Examples:
    $ python bots.py -t YOURTOKEN -o hacktoolkit
"""

import getopt
import json
import random
import re
import requests
import sys
import urllib

from github import Github

class GitHubReminderBot(object):
    """GitHub Reminder bot

    Uses PyGithub as a base API client - http://pygithub.readthedocs.io/en/latest/index.html
    """

    def __init__(self, github_access_token, organization):
        """Initializes the GitHub API client and prefetches the `organization` and repositories
        """
        self.github_access_token = github_access_token
        self.organization = organization

        self.cli = Github(self.github_access_token)
        self.org = self.cli.get_organization(organization)
        # http://pygithub.readthedocs.io/en/latest/github_objects/Organization.html#github.Organization.Organization.get_repos
        self.repos = self.org.get_repos(type='all')

    def pull_request_reminder(self):
        """Returns a Markdown-formatted message for this organization's pull requests
        """
        greeting = random.choice([u'Hola', u'Como estas', u'Greetings', u'你好', u'Hello', u'Aloha', u'Ciao', u'Salut', u'안녕하세요', u'こんにちは', u'שלום', u'chào bạn',])

        def pluralize(s, num):
            plural_suffix = '' if num == 1 else 's'
            value = '%s %s' % (num, s + plural_suffix,)
            return value

        def should_exclude_pull_request(pull_request):
            title = pull_request.title.strip()
            m = re.match(r'^\[WIP\].*', title)
            should_exclude = m is not None
            return should_exclude

        def format_pull_request(num, repo, pull_request):
            # http://pygithub.readthedocs.io/en/latest/github_objects/PullRequest.html#github.PullRequest.PullRequest
            # https://api.slack.com/docs/message-formatting
            num_comments = pull_request.comments
            context = {
                'num' : num,
                'repo_name' : repo.name,
                'pr_author' : pull_request.user.login,
                'pr_author_url' : pull_request.user.html_url,
                'pr_title' : pull_request.title,
                'pr_url' : pull_request.html_url,
                'num_comments' : pluralize('comment', num_comments),
            }

            msg = """%(num)s) **%(repo_name)s** | <%(pr_author_url)s|%(pr_author)s>
<%(pr_url)s|%(pr_title)s> - %(num_comments)s""" % context

            return msg

        num = 1
        pull_request_messages = []
        for repo in self.repos:
            open_pull_requests = repo.get_pulls(state='open', sort='created')
            for pull_request in open_pull_requests:
                if should_exclude_pull_request(pull_request):
                    pass
                else:
                    message = format_pull_request(num,repo, pull_request)
                    pull_request_messages.append(message)
                    num += 1

        context = {
            'greeting' : greeting,
            'pull_requests' : '\n'.join(pull_request_messages),
        }
        markdown_content = u"""%(greeting)s Team!

Here are the pull requests that need to be reviewed today:

%(pull_requests)s

Happy reviewing!
""" % context
        return markdown_content

class GitHubReminderSlackBot(GitHubReminderBot):
    def __init__(self, github_access_token, organization, slack_webhook_url, slack_channel):
        super(GitHubReminderSlackBot, self).__init__(github_access_token, organization)
        self.slack_webhook_url = slack_webhook_url
        self.slack_channel = slack_channel

    def remind_pull_requests(self):
        markdown_content = self.pull_request_reminder()
        from htk.utils.text.converters import markdown2slack
        slack_text = markdown2slack(markdown_content)
        from htk.lib.slack.utils import webhook_call
        webhook_call(
            webhook_url=self.slack_webhook_url,
            channel=self.slack_channel,
            text=slack_text,
            username='GitHub Reminder Bot',
            icon_emoji=':dark_sunglasses:',
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
        except getopt.error, msg:
             raise Usage(msg)
        # process options
        for o, a in opts:
            if o in ('-h', '--help'):
                print __doc__
                sys.exit(0)
            elif o in ('-t', '--token'):
                token = a
            elif o in ('-o', '--org'):
                org = a
        if token and org:
            bot = GitHubReminderBot(token, org)
            print bot.pull_request_reminder()
        else:
            raise Usage('Incorrect arguments')

    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 3.14159

if __name__ == '__main__':
    main()
