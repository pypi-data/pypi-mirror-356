"""Version utilities for DBAgent."""

from . import __version__


def get_version():
    """Get the current version of DBAgent.
    
    Returns:
        str: The version string.
    """
    return __version__


def print_version():
    """Print the current version of DBAgent."""
    print(f"DBAgent version {get_version()}")


if __name__ == "__main__":
    print_version()