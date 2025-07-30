"""Command line interface for github-file-loader."""

import asyncio
import sys

from .file_loader import FileLoader


async def main():
    """Main CLI function."""
    if len(sys.argv) < 2:
        print("Usage: github-file-loader <repo_url> [file_paths...]")
        print("       github-file-loader <repo_url> --sync [file_paths...]")
        print("")
        print("Examples:")
        print("  github-file-loader owner/repo")
        print("  github-file-loader owner/repo README.md src/main.py")
        print("  github-file-loader owner/repo --sync README.md src/main.py")
        return

    repo_url = sys.argv[1]

    # Check if --sync flag is used
    use_sync = "--sync" in sys.argv
    if use_sync:
        # Remove --sync from arguments
        args = [arg for arg in sys.argv[2:] if arg != "--sync"]
        file_paths = args if args else None
    else:
        file_paths = sys.argv[2:] if len(sys.argv) > 2 else None

    loader = FileLoader()

    if file_paths:
        # Load specific files
        if use_sync:
            print("Using synchronous loading...")
            files, failed = loader.load_files_sync(repo_url, file_paths)
        else:
            print("Using asynchronous loading...")
            files, failed = await loader.load_files(repo_url, file_paths)

        print(f"Successfully loaded {len(files)} files:")
        for file_info in files:
            print(f"  - {file_info.path} ({file_info.size} bytes)")

        if failed:
            print(f"Failed to load {len(failed)} files: {failed}")
    else:
        # Discover files
        files, message = loader.discover_files(repo_url)
        print(message)
        print(f"Found files: {files[:10]}")  # Show first 10 files
        if len(files) > 10:
            print(f"... and {len(files) - 10} more files")


def cli_main():
    """Synchronous entry point for CLI."""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()
