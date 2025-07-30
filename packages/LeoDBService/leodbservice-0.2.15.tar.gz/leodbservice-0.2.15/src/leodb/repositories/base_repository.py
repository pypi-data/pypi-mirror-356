from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from leodb.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReadSchemaType]):
    def __init__(self, db: AsyncSession, model: Type[ModelType], read_schema: Type[ReadSchemaType]):
        """
        Base class for data repositories.

        :param db: The SQLAlchemy async session
        :param model: A SQLAlchemy model class
        :param read_schema: A Pydantic schema for reading/returning data
        """
        self.db = db
        self.model = model
        self.read_schema = read_schema

    async def get(self, id: Any) -> Optional[ReadSchemaType]:
        from sqlalchemy.inspection import inspect
        primary_key_name = inspect(self.model).primary_key[0].name
        statement = select(self.model).where(getattr(self.model, primary_key_name) == id)
        result = await self.db.execute(statement)
        db_obj = result.scalar_one_or_none()
        return self.read_schema.from_orm(db_obj) if db_obj else None

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[ReadSchemaType]:
        statement = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(statement)
        db_objs = result.scalars().all()
        return [self.read_schema.from_orm(db_obj) for db_obj in db_objs]

    async def create(self, *, obj_in: CreateSchemaType) -> ReadSchemaType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return self.read_schema.from_orm(db_obj)

    async def update(
        self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ReadSchemaType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return self.read_schema.from_orm(db_obj)

    async def remove(self, *, id: UUID) -> Optional[ReadSchemaType]:
        # First, get the object to be returned later
        statement = select(self.model).where(getattr(self.model, "id", None) == id)
        result = await self.db.execute(statement)
        db_obj = result.scalar_one_or_none()

        if db_obj:
            # Convert to schema before deletion
            read_obj = self.read_schema.from_orm(db_obj)
            await self.db.delete(db_obj)
            await self.db.flush()
            return read_obj
        return None