from fastapi import FastAPI
from sqlalchemy.orm import Session
import os
import uvicorn
from dotenv import load_dotenv
from endpoint.user_router import user_router

load_dotenv('core/config.env')

# 기본 FastAPI 애플리케이션
app = FastAPI()

app.max_connections = int(os.getenv("REST_MAX_CONNECTIONS"))
app.max_request_size = int(os.getenv("REST_BODY_LIMIT"))
app.debug = os.getenv("REST_DEBUG").lower() == "true"
app.host = os.getenv("REST_HOST")
app.port = int(os.getenv("REST_PORT"))

# FastAPI 애플리케이션 설정
if __name__ == "__main__":
    # FastAPI 애플리케이션 설정
    uvicorn.run("main:app", host=app.host, port=app.port, reload=True)


@app.get("/")
def index():
    return {"message": "Hello World"}


app.include_router(user_router)
