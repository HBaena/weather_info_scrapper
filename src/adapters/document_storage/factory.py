from .interface import DocumentStorageInterface
from .local_storage.adapter import LocalStorageAdapter


def get_adapter(client_name: str = "local") -> DocumentStorageInterface:
    if client_name == "local":
        return LocalStorageAdapter
