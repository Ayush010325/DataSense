import os
import sys

# Add backend directory to sys.path so 'app' can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(os.path.dirname(current_dir), "backend")
sys.path.append(backend_dir)

from app.db.session import engine, Base
import app.models  # Imports __init__ which registers Dataset, ColumnMetadata, Experiment

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()
