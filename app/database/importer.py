import json
import time
from pathlib import Path

from sqlalchemy.orm import Session

from app.database.repositories import LogRepository
from app.utils.json_sanitizer import sanitize_json


FILE_TABLE_MAPPING = {
    "logs.ftp_logs.json": "ftp_logs",
    "logs.https_logs.json": "https_logs",
    "logs.octopus_logs.json": "octopus_logs",
    "logs.rdp_logs.json": "rdp_logs",
    "logs.sqli_logs.json": "sqli_logs",
    "logs.ssh_logs.json": "ssh_logs",
    "system.binaries_analytics.json": "binaries_analytics",
}


class DataImporter:
    def __init__(self, db: Session):
        self.db = db
        self.repository = LogRepository(db)

    def import_directory(self, data_dir: str):
        data_path = Path(data_dir)

        total_imported = 0
        total_failed = 0

        overall_start = time.perf_counter()

        summary = {}

        for filename, table_name in FILE_TABLE_MAPPING.items():

            file_path = data_path / filename

            if not file_path.exists():
                print(f"\n⚠ Missing file: {filename}")
                continue

            imported, failed = self.import_file(
                file_path=file_path,
                table_name=table_name,
            )

            summary[table_name] = imported

            total_imported += imported
            total_failed += failed

        total_time = time.perf_counter() - overall_start

        print("\n========== IMPORT SUMMARY ==========\n")

        for table_name, count in summary.items():
            print(f"{table_name:<24} {count:,}")

        print("-" * 38)
        print(f"Imported Records : {total_imported:,}")
        print(f"Failed Records   : {total_failed:,}")
        print(f"Total Time       : {total_time:.2f} seconds")
        print("\n====================================")

    def import_file(self, file_path: Path, table_name: str):

        print("\n" + "=" * 60)
        print(f"Importing: {file_path.name}")
        print(f"Destination Table: {table_name}")
        print("=" * 60)

        start = time.perf_counter()

        imported = 0
        failed = 0

        with open(file_path, "r", encoding="utf-8") as f:
            records = json.load(f)

        print(f"Loaded {len(records):,} records")

        valid_records = []

        for index, record in enumerate(records, start=1):

            if not isinstance(record, dict):
                failed += 1
                print(f"✗ Record {index}: Not a JSON object")
                continue

            try:
                cleaned = sanitize_json(record)
                valid_records.append(cleaned)

            except Exception as e:
                failed += 1
                print(f"✗ Record {index}: Sanitization failed")
                print(f"  {e}")

        print(f"Valid Records : {len(valid_records):,}")
        print(f"Skipped       : {failed:,}")

        if valid_records:

            inserted, insert_failed = self.repository.bulk_insert(
                table_name=table_name,
                records=valid_records,
            )

            imported += inserted
            failed += insert_failed

        elapsed = time.perf_counter() - start

        print("\nFinished")
        print(f"Imported : {imported:,}")
        print(f"Failed   : {failed:,}")
        print(f"Time     : {elapsed:.2f} seconds")

        return imported, failed