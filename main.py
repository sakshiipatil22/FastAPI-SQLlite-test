from fastapi import FastAPI
from uvicorn import run
from src.routes.all_routes import router
from src.db.models import init_db
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="Student library management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.on_event("startup")
async def init_process():
    init_db()

app.include_router(router)

if __name__=="__main__":
    run("main:app",host="0.0.0.0",port=12000, reload=True)