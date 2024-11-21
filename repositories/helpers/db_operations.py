from typing import TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


def copy_attributes(target, source):
    for key, value in source.__dict__.items():
        if not key.startswith('_sa_instance_state'):
            setattr(target, key, value)


class RepositoryDBException(Exception):
    """Custom exception for errors occurring during database save operations."""

    def __init__(self, message: str = 'An error occurred on database', original_exception: Exception = None):
        super().__init__(message)
        self.message = message
        self.original_exception = original_exception

    def __str__(self):
        if self.original_exception:
            return f"{self.message}: {str(self.original_exception)}"
        return self.message
