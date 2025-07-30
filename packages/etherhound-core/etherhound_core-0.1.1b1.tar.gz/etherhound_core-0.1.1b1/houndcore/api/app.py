from fastapi import FastAPI
from houndcore import router

app = FastAPI()
app.include_router(router)