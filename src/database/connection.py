from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List
from pydantic import BaseSettings, BaseModel
from dotenv import load_dotenv
import os
from models.users import User
from models.events import Event

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: str = os.getenv('SECRET_KEY')

    async def initialize_database(self, env: str = 'dev'):
        client = AsyncIOMotorClient(os.getenv('DATABASE_URL'))
        database = client.db_name
        if env == 'test':
            database = client.test_db
        await init_beanie(database=database, document_models=[Event, User])

class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        des_body = body.dict(exclude_unset=True)
        update_query = {'$set': {field: value for field, value in des_body.items()}}
        doc = await self.get(id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True
