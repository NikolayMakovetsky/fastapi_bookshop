from fastapi import FastAPI
from routers import *
import uvicorn

app = FastAPI()
app.include_router(task_router)
app.include_router(genre_router)

if __name__ == '__main__':
    uvicorn.run(app)
