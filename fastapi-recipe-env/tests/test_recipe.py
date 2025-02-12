import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, SessionLocal
import os

# Set the TESTING environment variable
os.environ["TESTING"] = "1"

# Set up a testing database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # SQLite for testing purposes
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables
Base.metadata.create_all(bind=engine)

# Override the DB session for testing
@pytest.fixture(scope="function")
def override_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Clean up after tests

app.dependency_overrides[SessionLocal] = override_db  # Use test DB instead of real DB

client = TestClient(app)  # Test client


# Test: Create a new recipe
def test_add_recipe():
    response = client.post("/recipes/", json={
        "name": "Test Recipe",
        "ingredients": "Flour, Water, Salt",
        "steps": "Mix, Bake, Serve",
        "prep_time": 30
    })
    
    assert response.status_code == 200  # Change to 200 instead of 201
    response_json = response.json()
    
    assert "id" in response_json
    assert response_json["name"] == "Test Recipe"
    assert response_json["ingredients"] == "Flour, Water, Salt"
    assert response_json["steps"] == "Mix, Bake, Serve"
    assert response_json["prep_time"] == 30
    return response_json["id"]  # Return ID from the response


# Test: Retrieve all recipes
def test_get_recipes():
    response = client.get("/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test: Retrieve a specific recipe (assuming ID 1 exists)
def test_get_recipe_by_id():
    recipe_id = test_add_recipe()  # Use the correct function to create a recipe
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    assert "name" in response.json()


# Test: Update a recipe (assuming ID 1 exists)
def test_update_recipe():
    recipe_id = test_add_recipe()  # Use the correct function to create a recipe
    response = client.put(f"/recipes/{recipe_id}", json={
        "name": "Updated Recipe",
        "ingredients": "Updated ingredients",
        "steps": "Updated steps",
        "prep_time": 25
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Recipe"


# Test: Delete a recipe (assuming ID 1 exists)
def test_delete_recipe():
    recipe_id = test_add_recipe()  # Use the correct function to create a recipe
    response = client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Recipe deleted successfully"


# Test: Add a rating (assuming recipe ID 1 exists)
def test_rate_recipe():
    recipe_id = test_add_recipe()  # Use the correct function to create a recipe
    response = client.post(f"/recipes/{recipe_id}/ratings/", json={"rating": 5})
    assert response.status_code == 200  # Change to 200 for successful response
    assert response.json()["message"] == "Rating added successfully"


# Test: Add a comment to a recipe
def test_add_comment():
    recipe_id = test_add_recipe()  # Use the correct function to create a recipe
    response = client.post(f"/recipes/{recipe_id}/comments/", json={
        "comment": "This is a test comment",
        "user_id": 1  # Assuming user with ID 1 exists
    })
    assert response.status_code == 201  # Change to 201 as API returns 201 Created
    assert response.json()["comment"] == "This is a test comment"


# Test: Get comments for a specific recipe
def test_get_comments():
    # Step 1: Add a recipe
    recipe_id = test_add_recipe()  # Ensure this returns a valid recipe ID
    assert recipe_id is not None, "Recipe ID is None"

    # Step 2: Check if the recipe exists
    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200, "Recipe not found"

    # Step 3: Add a comment to the recipe
    comment_data = {"user_id": 1, "comment": "Delicious recipe!"}
    response = client.post(f"/recipes/{recipe_id}/comments/", json=comment_data)
    assert response.status_code == 201, "Failed to add comment"  # Change to 201 for successful creation

    # Step 4: Get comments for the recipe
    response = client.get(f"/recipes/{recipe_id}/comments/")
    assert response.status_code == 200, "Failed to fetch comments"
    assert len(response.json()) > 0, "No comments found"



# Test: Retrieve recipe suggestions based on ratings
def test_get_suggestions():
    # Create a recipe and add ratings to test suggestions
    recipe_id = test_add_recipe()
    client.post(f"/recipes/{recipe_id}/ratings/", json={"rating": 5})
    
    response = client.get("/recipes/suggestions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
