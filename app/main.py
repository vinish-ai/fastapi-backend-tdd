from fastapi import FastAPI, Depends
from app.config import Settings, get_settings

app = FastAPI()

@app.get("/ping")
def hello(settings: Settings = Depends(get_settings)):
    return {
        "msg": "Hello World!",
        "environment": settings.environment,
        "testing": settings.testing
        }