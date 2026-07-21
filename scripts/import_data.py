import argparse

from app.database.client import SessionLocal, engine
from app.database.importer import DataImporter

# Disable SQLAlchemy SQL logging only for the importer
engine.echo = False


def main():
    parser = argparse.ArgumentParser(
        description="Import cybersecurity JSON datasets into PostgreSQL."
    )

    parser.add_argument(
        "--data-dir",
        required=True,
        help="Directory containing JSON files",
    )

    args = parser.parse_args()

    db = SessionLocal()

    try:
        importer = DataImporter(db)
        importer.import_directory(args.data_dir)
    finally:
        db.close()


if __name__ == "__main__":
    main()