from typing import List
import uuid
from sqlalchemy.orm import Session
from .base import ViewBase
from models.search import Search
from schemas.search import SearchSchema


# Логика поиска.
class SearchView(ViewBase[Search, SearchSchema]):

    # Обновление статуса.
    def update_status(self, db: Session, search_id: str):
        db_search = db.get(Search, search_id)
        search_data = {"status": "COMPLETED"}
        for key, value in search_data.items():
            setattr(db_search, key, value)
        db.add(db_search)
        db.commit()
        db.refresh(db_search)
        return db_search

    # Создание поиска.
    def create_search(self, db: Session,) -> Search:
        db_obj = Search(
            search_id=str(uuid.uuid4()),
            status="PENDING",
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Получение поиска.
    def get_search(
        self, db: Session, *, search_id: str
    ) -> List[SearchSchema]:
        return db.query(self.model).filter(Search.search_id == search_id).all()


search = SearchView(Search)
