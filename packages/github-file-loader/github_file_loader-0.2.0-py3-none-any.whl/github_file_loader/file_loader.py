"""File loading logic for GitHub repositories."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

from .client import github_client
from .core.types import GitHubFileInfo

logger = logging.getLogger(__name__)


class FileLoader:
    """Main file loader class."""

    def __init__(self, token: str = None):
        """Initialize with optional GitHub token."""
        if token:
            from .client import GitHubClient

            self.client = GitHubClient(token)
        else:
            self.client = github_client

    async def load_files(
        self, repo_url: str, file_paths: List[str], branch: str = "main"
    ) -> Tuple[List[GitHubFileInfo], List[str]]:
        """Load multiple files from GitHub repository asynchronously."""
        return await self.client.get_multiple_files(repo_url, file_paths, branch)

    def load_files_sync(
        self,
        repo_url: str,
        file_paths: List[str],
        branch: str = "main",
        max_concurrent: int = 10,
    ) -> Tuple[List[GitHubFileInfo], List[str]]:
        """
        Load multiple files from GitHub repository synchronously with concurrent processing.

        This method processes files in batches using ThreadPoolExecutor for concurrent
        requests while maintaining the simplicity of synchronous code.

        Args:
            repo_url: GitHub repository URL
            file_paths: List of file paths to load
            branch: Branch name (default: "main")
            max_concurrent: Maximum number of concurrent requests (default: 10)

        Returns:
            Tuple of (successful_files, failed_file_paths)
        """
        successful_files = []
        failed_files = []

        def fetch_single_file(file_path: str) -> Tuple[GitHubFileInfo, str, bool]:
            """
            Fetch a single file synchronously.

            Returns:
                Tuple of (file_info or None, file_path, success_flag)
            """
            try:
                # Run the async method in a new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    file_info = loop.run_until_complete(
                        self.client.get_file_content(repo_url, file_path, branch)
                    )
                    return file_info, file_path, True
                finally:
                    loop.close()
            except Exception as e:
                logger.error(f"Failed to fetch {file_path}: {e}")
                return None, file_path, False

        # Process files in batches with concurrent execution
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            # Submit all tasks
            future_to_path = {
                executor.submit(fetch_single_file, path): path for path in file_paths
            }

            # Collect results as they complete
            for future in as_completed(future_to_path):
                file_info, file_path, success = future.result()

                if success and file_info:
                    successful_files.append(file_info)
                else:
                    failed_files.append(file_path)

        logger.info(
            f"Fetched {len(successful_files)} files successfully, {len(failed_files)} failed"
        )
        return successful_files, failed_files

    # Keep the old method name for backward compatibility
    async def load_files_async(
        self, repo_url: str, file_paths: List[str], branch: str = "main"
    ) -> Tuple[List[GitHubFileInfo], List[str]]:
        """Load multiple files from GitHub repository (deprecated: use load_files)."""
        return await self.load_files(repo_url, file_paths, branch)

    def discover_files(
        self,
        repo_url: str,
        branch: str = "main",
        file_extensions: List[str] = None,
    ) -> Tuple[List[str], str]:
        """Discover files in a GitHub repository."""
        if file_extensions is None:
            file_extensions = [".md", ".mdx", ".py", ".txt"]

        return self.client.get_repository_tree(
            repo_url, branch, file_extensions, include_sha=False
        )
