from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import origins
from . import seed

app = FastAPI(title="BeanAtlas API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://beanatlas.net",
        "https://www.beanatlas.net",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
seed.run()

app.include_router(origins.router)


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
