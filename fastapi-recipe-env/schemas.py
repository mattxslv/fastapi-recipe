from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Recipe Out model
class RecipeOut(BaseModel):
    id: int
    name: str
    ingredients: str
    steps: str
    prep_time: Optional[int] = None
    rating: Optional[float] = None
    created_at: Optional[int] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        obj_dict = obj.__dict__
        if isinstance(obj_dict.get('created_at'), datetime):
            obj_dict['created_at'] = int(obj_dict['created_at'].timestamp())
        return super().from_orm(obj)


# Recipe Create model
class RecipeCreate(BaseModel):
    name: str
    ingredients: str
    steps: str
    prep_time: Optional[int] = None


# Recipe Update model
class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    ingredients: Optional[str] = None
    steps: Optional[str] = None
    prep_time: Optional[int] = None


# Comment Create model
class CommentCreate(BaseModel):
    user_id: int
    comment: str


# Comment Response model
class CommentResponse(BaseModel):
    id: int
    user_id: int
    recipe_id: int
    comment: str

    class Config:
        from_attributes = True


# User Create model
class UserCreate(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# Rating Request model
class RatingRequest(BaseModel):
    rating: float
