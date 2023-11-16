from fastapi import FastAPI
from sqlalchemy.orm import Session
import os
import uvicorn
from endpoint.user_router import user_router
import core.config_yaml_read as config
import service.schedules

# from dotenv import load_dotenv
# load_dotenv('core/config_old.env')

# 기본 FastAPI 애플리케이션
app = FastAPI()

app.max_connections = str(config.REST_CONFIG["max_connections"])
app.max_request_size = int(config.REST_CONFIG["max_request_size"])
app.debug = str(config.REST_CONFIG["debug"])
app.host = str(config.REST_CONFIG["host"])
app.port = int(config.REST_CONFIG["port"])



# FastAPI 애플리케이션 설정
# if __name__ == "__main__":
#     # FastAPI 애플리케이션 설정
#     uvicorn.run("main:app", host=app.host, port=app.port, reload=True)


@app.get("/")
def index():
    return {"message": "Hello World"}


app.include_router(user_router)
