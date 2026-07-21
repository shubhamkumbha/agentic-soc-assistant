from app.database.client import Base, engine

# Import models so SQLAlchemy registers them
from app.models import log_models


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")