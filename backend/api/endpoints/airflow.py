import asyncio
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
from views.views import search
from .deps import get_db
from schemas.search import SearchSchema, CreateSearchSchema
from views.services import get_response, sort_and_edit_json


router = APIRouter()


@router.post("/search/", response_model=CreateSearchSchema)
async def create_position(
    *,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks

) -> Any:
    """
    отправляет запросы на поиск в сервисы  provider-a и provider-b
    и в ответе возвращает уникальный search_id поиска
    """
    search_create = search.create_search(db=db)
    id = str(search_create.search_id)
    background_tasks.add_task(get_response, id)
    return search_create


@router.get("/results/{search_id}/{currency}")
async def read_replacement(
    db: Session = Depends(get_db),
    search_id: str = None,
    currency: str = None
) -> Any:
    """
    возвращает результаты поиска в провайдерах provider-a и provider-b
    по уникальному search_id  поиска с указанием валюты currency
    """
    try: 
        search_get = search.get_search(db, search_id=search_id)
    except Exception:      
        raise HTTPException(status_code=404, detail=f"{search_id} not found ")

    task1 = asyncio.create_task(sort_and_edit_json(search_id))
    try:
        data = await task1
        if search_get[0].status != "COMPLITED":
            search.update_status(db, search_get[0].search_id)
        data_json = SearchSchema(
            search_id=search_get[0].search_id,
            status=search_get[0].status, items=data
            )
    except:
        data_json = SearchSchema(
            search_id=search_get[0].search_id,
            status=search_get[0].status, items=[]
            )

    return data_json
