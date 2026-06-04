import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(os.path.dirname(current_dir), "backend")
sys.path.append(backend_dir)

from app.db.session import engine, Base
import app.models
from sqlalchemy import inspect, text


def add_dataset_storage_columns():
    inspector = inspect(engine)
    if "datasets" not in inspector.get_table_names():
        return

    existing = {column["name"] for column in inspector.get_columns("datasets")}
    dialect = engine.dialect.name
    statements = []

    if "file_data" not in existing:
        data_type = "BYTEA" if dialect == "postgresql" else "BLOB"
        statements.append(f"ALTER TABLE datasets ADD COLUMN file_data {data_type}")
    if "file_size" not in existing:
        statements.append("ALTER TABLE datasets ADD COLUMN file_size INTEGER")
    if "content_type" not in existing:
        statements.append("ALTER TABLE datasets ADD COLUMN content_type VARCHAR(100)")

    if statements:
        with engine.begin() as conn:
            for statement in statements:
                conn.execute(text(statement))


def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    add_dataset_storage_columns()
    print("Database tables created successfully.")


if __name__ == "__main__":
    init_db()
