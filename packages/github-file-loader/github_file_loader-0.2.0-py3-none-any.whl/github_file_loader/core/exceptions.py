"""Custom exceptions for GitHub File Loader."""


class GitHubError(Exception):
    """Base exception for GitHub-related errors."""

    pass


class GitHubAuthenticationError(GitHubError):
    """Exception for authentication errors."""

    pass


class GitHubRateLimitError(GitHubError):
    """Exception for rate limit errors."""

    pass


class GitHubRepositoryNotFoundError(GitHubError):
    """Exception for repository not found errors."""

    pass
