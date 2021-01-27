from datetime import datetime

from fastapi import FastAPI
from pydantic.main import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class GetResultRequest(BaseModel):
    ctn: str
    iin: str
    smartphoneID: int
    income: int
    creationDate: datetime


@app.post("/get_result")
async def get_result(request: GetResultRequest):
    return {
        "result": "Одобрение",
    }
