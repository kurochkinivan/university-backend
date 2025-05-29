import uvicorn 
from fastapi import FastAPI
from routers import task as TaskRouter
from database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(
    TaskRouter.router,
    prefix='/api/tasks'
)

if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8080, workers=3, reload=True)