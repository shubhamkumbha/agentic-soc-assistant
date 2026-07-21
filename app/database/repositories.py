from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.log_models import (
    FTPLog,
    HTTPSLog,
    OctopusLog,
    RDPLog,
    SQLILog,
    SSHLog,
    BinariesAnalytics,
)

TABLE_MODELS = {
    "ftp_logs": FTPLog,
    "https_logs": HTTPSLog,
    "octopus_logs": OctopusLog,
    "rdp_logs": RDPLog,
    "sqli_logs": SQLILog,
    "ssh_logs": SSHLog,
    "binaries_analytics": BinariesAnalytics,
}


class LogRepository:
    def __init__(self, db: Session):
        self.db = db

    def bulk_insert(self, table_name: str, records: list[dict]) -> tuple[int, int]:
        """
        Fast batch insert.

        If the batch fails, automatically fall back to
        inserting records one by one.

        Returns:
            (imported_count, failed_count)
        """

        model = TABLE_MODELS[table_name]

        objects = [
            model(document=record)
            for record in records
        ]

        try:
            self.db.bulk_save_objects(objects)
            self.db.commit()

            print(f"   ✓ Batch insert successful ({len(objects)} records)")
            return len(objects), 0

        except SQLAlchemyError as e:

            print("\n⚠ Batch insert failed.")
            print("Falling back to row-by-row insertion...")
            print(f"Reason: {e}")

            self.db.rollback()

        imported = 0
        failed = 0

        total = len(records)

        for index, record in enumerate(records, start=1):

            try:
                self.db.add(model(document=record))
                self.db.commit()

                imported += 1

                if index % 100 == 0 or index == total:
                    print(f"   Progress: {index}/{total}")

            except Exception as e:

                self.db.rollback()

                failed += 1

                print(f"\n✗ Failed record #{index}")
                print(type(e).__name__)
                print(e)

        return imported, failed