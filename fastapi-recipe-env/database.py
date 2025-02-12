from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use a test database when running tests
IS_TEST = os.getenv("TESTING", "0") == "1"

DATABASE_URL = "mssql+pyodbc://sa:YourPassword123@localhost:1433/recipe_db?driver=ODBC+Driver+17+for+SQL+Server"
TEST_DATABASE_URL = "mssql+pyodbc://sa:YourPassword123@localhost:1433/recipe_test_db?driver=ODBC+Driver+17+for+SQL+Server"

# Choose the correct database
DATABASE_URL = TEST_DATABASE_URL if IS_TEST else DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency override for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
