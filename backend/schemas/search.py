from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class SearchInDBBase(BaseModel):
    search_id: Optional[UUID]

    class Config:
        orm_mode = True


class SearchPath(BaseModel):
    items: Optional[list]

    class Config:
        orm_mode = True


# Properties to return to client
class CreateSearchSchema(SearchInDBBase):
    search_id: Optional[UUID]

    class Config:
        orm_mode = True


class SearchSchema(SearchInDBBase):
    search_id: UUID
    status: str
    items: Optional[list]

    class Config:
        orm_mode = True


# Properties properties stored in DB
class SearchInDB(SearchInDBBase):
    pass
