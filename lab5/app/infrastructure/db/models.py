from sqlalchemy import Column, String, Integer, DateTime, JSON, Text, Float
from datetime import datetime
from .database import Base
import uuid


class RecipeModel(Base):
    __tablename__ = "recipes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False)
    ingredients = Column(JSON, nullable=False)  # List[Ingredient] -> JSON
    steps = Column(JSON, nullable=False)  # List[CookingStep] -> JSON
    status = Column(String(50), nullable=False, default="draft")
    source = Column(String(50), nullable=False, default="ai")
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")
    created_at = Column(DateTime, default=datetime.now)


class CookingSessionModel(Base):
    __tablename__ = "cooking_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False)
    recipe_id = Column(String(36), nullable=False)
    completed_steps = Column(JSON, default=list)
    start_time = Column(DateTime, nullable=True)
    estimated_minutes = Column(Integer, nullable=True)
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.now)
