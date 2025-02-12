
# FastAPI Recipe App Setup Guide

## Step 1: Set Up the Environment

Ensure you have Python and Docker installed on your system:

- **Python**: Install Python by running the following command:
  ```
  sudo apt install python3
  ```
- **Docker**: Follow the [official guide](https://docs.docker.com/get-docker/) to install Docker.

## Step 2: Set Up FastAPI Project

1. Clone the repository (assuming your project is on GitHub):
   ```
   git clone https://github.com/yourusername/fastapi-recipe.git
   cd fastapi-recipe
   ```

2. Create a Python Virtual Environment:
   ```
   python3 -m venv fastapi-recipe-env
   ```

3. Activate the Virtual Environment:
   ```
   source fastapi-recipe-env/bin/activate
   ```

4. Install Dependencies:
   ```
   pip install -r requirements.txt
   ```
   If you don't have a `requirements.txt` file, install the necessary packages manually:
   ```
   pip install fastapi uvicorn sqlalchemy pyodbc
   ```

## Step 3: Set Up the Database

1. Install MSSQL for your database, and install the necessary drivers:
   ```
   pip install sqlalchemy pyodbc
   ```

2. Configure Database Connection: In your `database.py` file, configure the connection to your MSSQL database. Example:
   ```python
   from sqlalchemy import create_engine
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker

   SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://username:password@hostname/dbname?driver=ODBC+Driver+17+for+SQL+Server"
   engine = create_engine(SQLALCHEMY_DATABASE_URL)
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

   Base = declarative_base()
   ```

## Step 4: Run the FastAPI App

Run the application:
```
uvicorn main:app --reload
```
This will start the app at [http://127.0.0.1:8000](http://127.0.0.1:8000). You can access the Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Optional: Using Docker

To run the application with Docker, follow these steps:

1. Build the Docker image (assuming you have a `Dockerfile` in your project):
   ```
   docker build -t fastapi-recipe .
   ```

2. Run the Docker container:
   ```
   docker run -d -p 8000:8000 fastapi-recipe
   ```

## Additional Notes:

- Ensure your database is correctly set up and accessible.
- Adjust the database connection string in `database.py` as needed.
- You can run tests or deploy using Docker if required.
```
