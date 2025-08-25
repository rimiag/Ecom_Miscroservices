from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(
    title="User Service",
    description="E-Commerce User Management API",
    version="1.0.0"
)

# Mock Database
users_db: Dict[int, Dict[str, Any]] = {
    1: {"id": 1, "name": "John Doe", "email": "john@example.com"},
    2: {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
}

class User(BaseModel):
    name: str
    email: str

class UserResponse(User):
    id: int

@app.get("/", tags=["Root"])
def root():
    """Service health check"""
    return {
        "service": "User Service",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Liveness probe"""
    return {"status": "healthy"}

@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    responses={
        404: {"description": "User not found"},
        200: {"description": "User retrieved successfully"}
    }
)
def get_user(user_id: int):
    """
    Retrieve a specific user by ID
    """
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return users_db[user_id]

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    responses={
        201: {"description": "User created successfully"}
    }
)
def create_user(user: User):
    """
    Create a new user
    - **name**: User's full name
    - **email**: User's email (must be unique)
    """
    new_id = max(users_db.keys()) + 1
    users_db[new_id] = {"id": new_id, **user.dict()}
    return users_db[new_id]

@app.get("/users", response_model=Dict[int, UserResponse], tags=["Users"])
def list_users():
    """List all users"""
    return users_db