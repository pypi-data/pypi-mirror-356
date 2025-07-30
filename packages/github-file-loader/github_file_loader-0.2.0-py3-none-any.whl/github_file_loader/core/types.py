"""Type definitions for GitHub File Loader."""

from dataclasses import dataclass


@dataclass
class GitHubFileInfo:
    """Information about a GitHub file."""

    path: str
    name: str
    sha: str
    size: int
    url: str
    download_url: str
    type: str
    encoding: str
    content: str

    def dict(self):
        """Convert to dictionary for compatibility."""
        return {
            "path": self.path,
            "name": self.name,
            "sha": self.sha,
            "size": self.size,
            "url": self.url,
            "download_url": self.download_url,
            "type": self.type,
            "encoding": self.encoding,
            "content": self.content,
        }
