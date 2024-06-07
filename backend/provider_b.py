import uvicorn
import time
from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/search")
def read_item():
    with open('files/response_b.json') as f:
        templates = json.load(f)
        time.sleep(10)
    return templates


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
