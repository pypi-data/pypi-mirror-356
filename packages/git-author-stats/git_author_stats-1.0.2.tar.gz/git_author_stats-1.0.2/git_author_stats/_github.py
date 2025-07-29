from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import ParseResult, urlparse

from github import Github
from github.Auth import Auth, Login, Token

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import date

    from github.Organization import Organization
    from github.Repository import Repository


def iter_organization_repository_clone_urls(
    url: str, user: str = "", password: str = "", since: date | None = None
) -> Iterable[str]:
    """
    Yield URLs for all repositories in a Github organization to which
    the specified user (or an unauthenticated user if none is specified)
    has access.

    Parameters:

    - url (str): The URL of the organization. For example:
      https://github.com/enorganic.
    - user (str) = "": A username with which to authenticate.
      Note: If neither user name nor password are provided, the default system
      configuration will be used.
    - password (str) = "": A password/token with which to authenticate.
    """
    auth: Auth | None = (
        Login(user, password)
        if user and password
        else Token(password)
        if password
        else None
    )
    github: Github = Github(auth=auth)
    if "://" not in url:
        url = f"https://{url}"
    parse_result: ParseResult = urlparse(url)
    organization_name: str = parse_result.path.strip("/")
    if not organization_name:
        raise ValueError(url)
    organization: Organization = github.get_organization(organization_name)
    repos: Iterable[Repository] = organization.get_repos()
    if since is not None:
        # Only include repositories which have been pushed to after `since`,
        # if `since` is not `None`
        repos = filter(lambda repo: repo.pushed_at.date() >= since, repos)
    repo: Repository
    yield from (
        repo.clone_url
        for repo in filter(
            # Only include repositories to which the user has pull access
            lambda repo: repo.permissions.pull,
            repos,
        )
    )
