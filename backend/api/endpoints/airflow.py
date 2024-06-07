import asyncio
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from views.views import search
from config.deps import get_db
from schemas.search import SearchSchema, CreateSearchSchema
from views.services import ProviderAService, ProviderBService
from utils.rate import sort_and_edit_json

router = APIRouter()


@router.post("/search/", response_model=CreateSearchSchema)
async def create_position(
        db: Session = Depends(get_db),
        background_tasks: BackgroundTasks = None
) -> Any:
    """
    Отправляет запросы на поиск в сервисы provider-a и provider-b
    и в ответе возвращает уникальный search_id поиска
    """
    search_create = search.create_search(db=db)
    search_id = str(search_create.search_id)
    provider_a_service = ProviderAService(search_id)
    provider_b_service = ProviderBService(search_id)
    background_tasks.add_task(provider_a_service)
    background_tasks.add_task(provider_b_service)
    return search_create


@router.get("/results/{search_id}/")
async def read_replacement(
        db: Session = Depends(get_db),
        search_id: str = None,
) -> Any:
    """
    Возвращает результаты поиска в провайдерах provider-a и provider-b
    по уникальному search_id поиска с указанием валюты currency
    """
    search_get = search.get_search(db, search_id=search_id)
    if not search_get:
        raise HTTPException(status_code=404, detail=f"{search_id} не найден")

    task = asyncio.create_task(sort_and_edit_json(search_id))

    try:
        data = await task
        if search_get[0].status != "COMPLETED":
            search.update_status(db, search_get[0].search_id, search_get[0].status)
        data_json = SearchSchema(
            search_id=search_get[0].search_id,
            status=search_get[0].status,
            items=data
        )
    except IndexError:
        raise HTTPException(status_code=400, detail="Некорректные данные")

    return data_json
