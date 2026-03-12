import os
import uvicorn
from fastapi import FastAPI
from api.app import create_app 

app: FastAPI = create_app()

def start():
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api.server:app", host="0.0.0.0", port=port)