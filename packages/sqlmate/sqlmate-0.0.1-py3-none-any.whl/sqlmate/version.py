"""Version utilities for SQLMate."""

from . import __version__


def get_version():
    """Get the current version of SQLMate.
    
    Returns:
        str: The version string.
    """
    return __version__


def print_version():
    """Print the current version of SQLMate."""
    print(f"SQLMate version {get_version()}")


if __name__ == "__main__":
    print_version()