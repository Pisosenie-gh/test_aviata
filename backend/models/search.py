from sqlalchemy import JSON, Column, String
from sqlalchemy.dialects.postgresql import UUID
from config.db import Base


class Search(Base):
    __tablename__ = "search"

    search_id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    status = Column(String, default='PENDING')
    items = Column(JSON,  nullable=True)
