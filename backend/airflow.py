import uvicorn
from fastapi import FastAPI
from fastapi import APIRouter
from multiprocessing import Process
from api.endpoints import airflow
from tasks import task_app

app = FastAPI()
api_router = APIRouter()
api_router.include_router(airflow.router, tags=["airflow"])

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
