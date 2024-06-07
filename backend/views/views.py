from typing import List
import uuid
from sqlalchemy.orm import Session
from views.base import ViewBase
from models.search import Search
from schemas.search import SearchSchema


class SearchView(ViewBase[Search, SearchSchema]):
    """ Логика поиска (обновление, создание, поиск)"""

    @staticmethod
    def update_status(db: Session, search_id: str, status_data: dict) -> Search:
        db_search = db.get(Search, search_id)
        for key, value in status_data.items():
            setattr(db_search, key, value)
        db.add(db_search)
        db.commit()
        db.refresh(db_search)
        return db_search

    @staticmethod
    def create_search(db: Session, ) -> Search:
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
