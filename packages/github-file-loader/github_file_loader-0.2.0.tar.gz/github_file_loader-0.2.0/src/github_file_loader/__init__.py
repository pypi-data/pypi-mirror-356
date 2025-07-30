"""GitHub File Loader - A Python package for loading files from GitHub repositories."""

__version__ = "0.2.0"

# Import main classes/functions for easy access
from .client import GitHubClient
from .file_loader import FileLoader
from .parser import build_github_api_url, build_github_web_url, parse_github_url

__all__ = [
    "GitHubClient",
    "FileLoader",
    "parse_github_url",
    "build_github_api_url",
    "build_github_web_url",
]
