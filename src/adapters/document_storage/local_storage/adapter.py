from os import path
from src.adapters.document_storage.interface import DocumentStorageInterface


class LocalStorageAdapter(DocumentStorageInterface):

    def __init__(self, root_location: str, storage_client=open):
        self.root_location = root_location
        self.storage_client = storage_client

    def read_file(filename: str):
        raise NotImplementedError

    def save_file(self, filename: str, content):
        write_mode = "w+" if isinstance(content, str) else "wb+"
        try:
            with self.storage_client(
                path.join(self.root_location, filename),
                mode=write_mode,
            ) as file:
                file.write(content)
        except Exception as error:
            return error
