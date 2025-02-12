from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
from models import Recipe, Rating, Comment, User
from schemas import RecipeCreate, RecipeUpdate, RecipeOut, UserCreate, CommentCreate, CommentResponse, RatingRequest
from typing import List, Optional

app = FastAPI(
    title="Recipe API",
    description="An API for managing recipes, users, ratings, and comments.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Recipe Management", "description": "Endpoints for adding, retrieving, and updating recipes."},
        {"name": "Recipe Search", "description": "Search recipes by name, ingredients, or get suggestions."},
        {"name": "User Management", "description": "Endpoints for user registration and authentication."},
        {"name": "Ratings & Comments", "description": "Endpoints for rating and commenting on recipes."}
    ]
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------ #
#       Recipe Search            #
# ------------------------------ #

@app.get("/recipes/search/", response_model=List[RecipeOut], tags=["Recipe Search"])
def search_recipes(
    search_query: Optional[str] = None, db: Session = Depends(get_db)
):
    if not search_query:
        recipes = db.query(Recipe).all()
        return [RecipeOut.from_orm(recipe) for recipe in recipes]

    recipes = db.query(Recipe).filter(
        func.lower(Recipe.name).like(f"%{search_query.lower()}%") |
        func.lower(Recipe.ingredients).like(f"%{search_query.lower()}%")
    ).all()

    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found")

    return [RecipeOut.from_orm(recipe) for recipe in recipes]

# ------------------------------ #
#       User Management          #
# ------------------------------ #

@app.post("/users/", response_model=UserCreate, tags=["User Management"])
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(name=user_data.name, email=user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[UserCreate], tags=["User Management"])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{user_id}", response_model=UserCreate, tags=["User Management"])   
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ------------------------------ #
#       Recipe Management        #
# ------------------------------ #

@app.post("/recipes/", response_model=RecipeOut, tags=["Recipe Management"])
def add_recipe(recipe_data: RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = Recipe(
        name=recipe_data.name,
        ingredients=recipe_data.ingredients,
        steps=recipe_data.steps,
        prep_time=recipe_data.prep_time
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return RecipeOut.from_orm(new_recipe)

@app.get("/recipes/", response_model=List[RecipeOut], tags=["Recipe Management"])
def get_all_recipes(db: Session = Depends(get_db)):
    recipes = db.query(Recipe).order_by(Recipe.created_at.desc()).all()
    return [RecipeOut.from_orm(recipe) for recipe in recipes]

@app.get("/recipes/{recipe_id}", response_model=RecipeOut, tags=["Recipe Management"])
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return RecipeOut.from_orm(recipe)

@app.put("/recipes/{recipe_id}", response_model=RecipeOut, tags=["Recipe Management"])
def update_recipe(recipe_id: int, recipe_data: RecipeUpdate, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe.name = recipe_data.name
    recipe.ingredients = recipe_data.ingredients
    recipe.steps = recipe_data.steps
    recipe.prep_time = recipe_data.prep_time
    db.commit()
    db.refresh(recipe)

    return RecipeOut.from_orm(recipe)

@app.delete("/recipes/{recipe_id}", tags=["Recipe Management"])
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}

# ------------------------------ #
#       Ratings & Comments       #
# ------------------------------ #

@app.post("/recipes/{recipe_id}/ratings/", tags=["Ratings & Comments"])
def rate_recipe(recipe_id: int, rating_data: RatingRequest, db: Session = Depends(get_db)):
    user_id = 1  # Replace with actual user authentication logic

    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    new_rating = Rating(recipe_id=recipe_id, user_id=user_id, rating=rating_data.rating)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    update_recipe_rating(recipe_id, db)

    return {"message": "Rating added successfully"}

def update_recipe_rating(recipe_id: int, db: Session):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe:
        avg_rating = db.query(func.avg(Rating.rating)).filter(Rating.recipe_id == recipe_id).scalar()
        recipe.rating = avg_rating
        db.commit()
        db.refresh(recipe)

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import datetime

@app.post("/recipes/{recipe_id}/comments/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED, tags=["Ratings & Comments"])
async def add_comment(recipe_id: int, comment_data: CommentCreate, db: Session = Depends(get_db)):
    # Check if recipe exists
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Check if user exists
    user = db.query(User).filter(User.id == comment_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create new comment
    new_comment = Comment(
        recipe_id=recipe_id,
        user_id=comment_data.user_id,
        comment=comment_data.comment
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    # Return the new comment as the response
    return CommentResponse.from_orm(new_comment)


@app.get("/recipes/{recipe_id}/comments/", response_model=List[CommentResponse], tags=["Ratings & Comments"])
def get_comments(recipe_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.recipe_id == recipe_id).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found for this recipe")
    return comments

@app.get("/recipes/suggestions/", response_model=List[RecipeOut], tags=["Recipe Search"])
def suggest_recipes(db: Session = Depends(get_db)):
    suggested_recipes = (
        db.query(
            Recipe.id,
            Recipe.name,
            Recipe.ingredients,
            Recipe.steps,
            Recipe.prep_time,
            Recipe.created_at,
            func.avg(Rating.rating).label("average_rating")
        )
        .join(Rating, Recipe.id == Rating.recipe_id)
        .group_by(Recipe.id, Recipe.name, Recipe.ingredients, Recipe.steps, Recipe.prep_time, Recipe.created_at)
        .order_by(func.avg(Rating.rating).desc())
        .limit(5)
        .all()
    )

    if not suggested_recipes:
        raise HTTPException(status_code=404, detail="No recipes found for suggestions")

    return [
        RecipeOut(
            id=recipe.id,
            name=recipe.name,
            ingredients=recipe.ingredients,
            steps=recipe.steps,
            prep_time=recipe.prep_time,
            created_at=int(recipe.created_at.timestamp()) if recipe.created_at else None,
            rating=recipe.average_rating
        ) for recipe in suggested_recipes
    ]
