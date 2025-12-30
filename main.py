from fastapi import FastAPI
from starter import start_job
from query import query_job
import asyncio
from common import InputJson

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/jobs/{job_id}")
def read_job(job_id: str):
    return asyncio.run(query_job(job_id))

@app.post("/jobs")
def create_job(input_data: InputJson):
    # input_data = {"msg": "Temporal", "fail_first_attempt": True}
    return asyncio.run(start_job(input_data))