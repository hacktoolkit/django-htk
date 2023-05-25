# Python Standard Library Imports
import re


RELEASE_TAG_REGEXES = [
    # never format: 'tag: deploy-202211031730-4acb099a93-master'
    re.compile(
        r'^tag: deploy-(?P<dt>\d{12})-(?P<sha>[a-f0-9]{10})-(?P<branch>[a-z]+)$'
    ),
    # older format: 'tag: deploy-20220710.195443'
    re.compile(r'^tag: deploy-(?P<date>\d{8})\.(?P<hms>\d{6})$'),
]

GITHUB_ISSUE_REGEX = re.compile(r'\(#(?P<issue_num>\d+)\)')

# example: 'git@github.com:[organization]/[repository].git'
ORIGIN_URL_REGEX = re.compile(
    r'^(?P<user>.+)@(?P<host>[a-z\.]+):(?P<org>[A-Za-z0-9_-]+)/(?P<repository>[A-Za-z0-9_-]+)\.git$'
)
