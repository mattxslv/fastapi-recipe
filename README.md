# Guide
 
Step 1: Set Up the Environment
Make sure you have Python and Docker installed on your system:

- Python: Install Python by running:
bash command:
sudo apt install python3

Docker: Follow the official guide to install Docker on your system.

Step 2: Set Up FastAPI Project
1.Clone the repository (assuming your project is on GitHub):
bash command:
git clone https://github.com/yourusername/fastapi-recipe.git
cd fastapi-recipe

2.Create a Python Virtual Environment:
bash command:
python3 -m venv fastapi-recipe-env

3.Activate the Virtual Environment:
bash command:
source fastapi-recipe-env/bin/activate

4.Install Dependencies: Install the required Python packages using pip:
bash command:
pip install -r requirements.txt

Note: If you don't have a requirements.txt, run this:
bash command:
pip install fastapi uvicorn sqlalchemy pyodbc

Step 3: Set Up the Database
1.Install MSSQL for your database, make sure to install the necessary drivers:
bash command:
pip install sqlalchemy pyodbc

2.Configure Database Connection: In your database.py file, configure the connection to your MSSQL database. Example:

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://username:password@hostname/dbname?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Step 4: Run the FastAPI App
Run the Application: After setting up the virtual environment and installing the dependencies, you can start the FastAPI app.
bash command:
uvicorn main:app --reload

This will start the app on http://127.0.0.1:8000. You can now access the Swagger UI at http://127.0.0.1:8000/docs.

-------------------------------------------------------------------------------------------------

Optional: Using Docker
If you'd like to use Docker to run the application:

1.Build the Docker Image - Assuming you have a Dockerfile in your project.
bash command:
docker build -t fastapi-recipe .

2.Run the Docker Container
bash command:
docker run -d -p 8000:8000 fastapi-recipe

-------------------------------------------------------------------------------------------------

Additional Notes:
Ensure that your database is correctly set up and accessible. Adjust the database connection string in database.py if needed.
You can run tests or use Docker for deployment if required.
