from os import path
from unittest.mock import call, Mock
from mamba import before, context, describe, it

from expects import expect, equal, be_none

from src.adapters.document_storage.local_storage.adapter import LocalStorageAdapter

with describe(LocalStorageAdapter) as self:
    with before.all:
        self.root_location = "/SOME/LOCATION/"
        self.content = "SOME_FILE_CONTENT"
        self.file_name = "SOME_FILE.NAME"

    with before.each:
        self.file = Mock()
        self.context_manager = Mock()
        self.storage_client = Mock()
        self.storage_client.return_value = self.context_manager
        self.context_manager.__enter__ = Mock(return_value=self.file)
        self.context_manager.__exit__ = Mock(return_value=None)

    with context(LocalStorageAdapter.save_file):
        with context("when something went wrong"):
            with it("shoul return an exception"):
                adapter = LocalStorageAdapter(
                    root_location=self.root_location,
                    storage_client=self.storage_client,
                )

                response = adapter.save_file(
                    filename=self.file_name,
                    content=self.content,
                )

                expect(
                    self.storage_client.call_args
                ).to(
                    equal(call(
                        path.join(self.root_location, self.file_name),
                        mode="w+",
                    ))
                )
                expect(self.file.write.call_args).to(equal(call(self.content)))
                expect(response).to(be_none)

        with context("when something went wrong"):
            with it("shoul return an exception"):
                error = Exception("SOME ERROR")
                self.context_manager.__enter__.side_effect = error
                adapter = LocalStorageAdapter(
                    root_location=self.root_location,
                    storage_client=self.storage_client,
                )

                response = adapter.save_file(
                    filename=self.file_name,
                    content=self.content,
                )

                expect(
                    self.storage_client.call_args
                ).to(
                    equal(call(
                        path.join(self.root_location, self.file_name),
                        mode="w+",
                    ))
                )
                expect(response).to(equal(error))
