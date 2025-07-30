"""Configuration for GitHub File Loader."""


class Settings:
    """Basic settings for GitHub File Loader."""

    def __init__(self):
        self.github_timeout = 30
        self.github_concurrent_requests = 10
        self.github_retries = 3


# Global settings instance
settings = Settings()
