from unittest.mock import call, Mock
from mamba import before, context, describe, it

from expects import be_false, be_none, expect, equal, be_true

from src.handler.save_db_resume.app import DBResumeSaver

with describe(DBResumeSaver) as self:
    with before.each:
        self.weather_info_repository = Mock()
        self.document_storage_adapter = Mock()
        self.parquet_file_generator = Mock()

    with context("when something went wrong"):
        with it("should raise an error and return ERROR"):
            self.weather_info_repository.get_resume.side_effect = Exception()
            executor = DBResumeSaver(
                weather_info_repository=self.weather_info_repository,
                document_storage_adapter=self.document_storage_adapter,
                parquet_file_generator=self.parquet_file_generator,
            )

            response = executor.execute()

            expect(self.weather_info_repository.get_resume.called).to(be_true)
            expect(self.document_storage_adapter.save_file.called).to(be_false)
            expect(self.parquet_file_generator.write.called).to(be_false)
            expect(response).to(equal("ERROR"))

    with context("when success"):
        with it("should raise return a SUCCESS"):
            ...
            # TODO: Create a parquet generator adapter to be able to mock an test this flow
