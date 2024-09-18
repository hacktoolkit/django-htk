# Python Standard Library Imports
import os

# Third Party (PyPI) Imports
import rollbar

from .file_io import (
    is_pathlib_path,
    read_file_oneline,
)


def get_current_git_hash(repo_path):
    # Path to the .git/HEAD file
    if is_pathlib_path(repo_path):
        head_file = repo_path / '.git' / 'HEAD'
    else:
        head_file = os.path.join(repo_path, '.git', 'HEAD')

    commit_hash = None

    try:
        # Read the HEAD file to get the current reference
        ref = read_file_oneline(head_file)

        # If HEAD points to a branch, resolve the reference
        if ref.startswith('ref:'):
            # Extract the reference path (e.g., refs/heads/main)
            ref_path = ref.split(' ')[1]
            # Path to the ref file containing the commit hash
            ref_file = os.path.join(repo_path, '.git', ref_path)

            # Read the commit hash from the ref file
            commit_hash = read_file_oneline(ref_file)
        else:
            # HEAD contains the commit hash directly (detached HEAD)
            commit_hash = ref

    except Exception as e:
        rollbar.report_exc_info(extra_data={'repo_path': repo_path})

    return commit_hash


def build_tags_path(repo_path):
    if is_pathlib_path(repo_path):
        tags_path = repo_path / '.git' / 'refs' / 'tags'
    else:
        tags_path = os.path.join(repo_path, '.git', 'refs', 'tags')

    return tags_path


def list_tags(repo_path):
    tags_path = build_tags_path(repo_path)

    tags = [tag for tag in os.listdir(tags_path)]

    return tags


def build_tag_file_path(repo_path, tag):
    tags_path = build_tags_path(repo_path)

    if is_pathlib_path(tags_path):
        tag_file = tags_path / tag
    else:
        tag_file = os.path.join(tags_path, tag)

    return tag_file


def get_tags_for_commit(repo_path, commit_hash):
    tags = []

    try:
        # Check each tag in the refs/tags directory
        for tag in list_tags(repo_path):
            tag_file = build_tag_file_path(repo_path, tag)

            # Read the commit hash associated with the tag
            tag_commit_hash = read_file_oneline(tag_file)

            # If the commit hash matches, add the tag to the list
            if tag_commit_hash == commit_hash:
                tags.append(tag)

    except Exception as e:
        rollbar.report_exc_info(
            extra_data={
                'repo_path': repo_path,
                'commit_hash': commit_hash,
            }
        )

    return tags


##
# GitHub


def build_github_commit_url(repo_url, commit_hash):
    github_commit_url = f'{repo_url}/commit/{commit_hash}'

    return github_commit_url


def build_github_tag_url(repo_url, tag):
    github_tag_url = f'{repo_url}/releases/tag/{tag}'

    return github_tag_url
