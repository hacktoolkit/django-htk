# Python Standard Library Imports
import typing as T

# Third Party (PyPI) Imports
from github import Github
from github.GitRelease import GitRelease
from github.Repository import Repository

# Django Imports
from django.conf import settings

# HTK Imports
from htk.utils import (
    htk_setting,
    resolve_model_dynamically,
)


Release = resolve_model_dynamically(htk_setting('HTK_GITHUB_RELEASE_MODEL'))


# isort: off


def get_github_client() -> Github:
    """Get an authenticated GitHub client.

    Returns:
        Github: An authenticated GitHub client instance.
    """
    access_token = htk_setting('HTK_GITHUB_READONLY_ACCESS_TOKEN')
    client = Github(access_token)
    return client


def get_repository(repo_name: str) -> Repository:
    """Get a GitHub repository by its full name.

    Args:
        repo_name (str): Full repository name (e.g., "BawsHuman/bawshuman-expo")

    Returns:
        Repository: GitHub repository instance
    """
    client = get_github_client()
    return client.get_repo(repo_name)


def sync_release(
    repo_name: str,
    release: GitRelease,
    existing_release: T.Optional['Release'] = None,
) -> 'Release':
    """Sync a single GitHub release to our database.

    Args:
        repo_name (str): Full repository name (e.g., "hacktoolkit/django-htk")
        release (GitRelease): GitHub release object
        existing_release (T.Optional[Release]): Existing release object if updating

    Returns:
        Release: The created or updated Release instance
    """
    release_data = {
        "repository": repo_name,
        "tag_name": release.tag_name,
        "name": release.title or "",
        "body": release.body or "",
        "draft": release.draft,
        "prerelease": release.prerelease,
        "published_at": release.published_at,
    }

    if existing_release:
        for key, value in release_data.items():
            setattr(existing_release, key, value)
        existing_release.save()
        return existing_release

    return Release.objects.create(**release_data)


def sync_repository_releases(
    repo_name: str,
    max_releases: T.Optional[int] = None,
) -> list['Release']:
    """Sync all releases from a GitHub repository.

    Args:
        repo_name (str): Full repository name (e.g., "hacktoolkit/django-htk")
        max_releases (T.Optional[int]): Maximum number of releases to sync

    Returns:
        list[Release]: List of synced Release instances
    """
    repo = get_repository(repo_name)
    releases = repo.get_releases()

    if max_releases:
        releases = list(releases[:max_releases])

    synced_releases = []
    existing_releases = {
        r.tag_name: r
        for r in Release.objects.filter(
            repository=repo_name,
        )
    }
    from htk.utils.debug import slack_debug

    # slack_debug(f'Syncing {len(releases)} releases from {repo_name}')

    for github_release in releases:
        existing_release = existing_releases.get(github_release.tag_name)
        release = sync_release(
            repo_name=repo_name,
            release=github_release,
            existing_release=existing_release,
        )
        synced_releases.append(release)

    return synced_releases
