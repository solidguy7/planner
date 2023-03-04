from pydantic import BaseModel, EmailStr
from typing import Optional, List
from beanie import Document, Link
from models.events import Event

class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Link[Event]]]

    class Config:
        schema_extra = {
            'example': {
                'email': 'fastapi@gmail.com',
                'password': 'strong',
                'events': [],
            }
        }

    class Settings:
        name = 'users'

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            'example': {
                'email': 'fastapi@gmail.com',
                'password': 'strong'
            }
        }
