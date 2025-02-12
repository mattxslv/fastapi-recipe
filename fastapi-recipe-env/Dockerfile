# Use official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy FastAPI project files to the container
COPY . .

# Install required dependencies
RUN pip install --no-cache-dir fastapi uvicorn pyodbc sqlalchemy pydantic

# Expose FastAPI port
EXPOSE 8000

# Command to start FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

