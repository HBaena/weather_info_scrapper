from abc import ABC, abstractmethod


class DocumentStorageInterface(ABC):

    def __init__(self, root_location: str, storage_client):
        self.storage_client = storage_client
        self.root_location = root_location

    @abstractmethod
    def read_file(self, filename: str):
        raise NotImplementedError

    @abstractmethod
    def save_file(self, filename: str, content):
        raise NotImplementedError
