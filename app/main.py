from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)

from app.database import init_db
from app.session.routes import router as session_router
from app.questions.routes import router as questions_router
from app.core.errors import AppException

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure database models and indexes exist
    init_db()
    yield
    # Shutdown logic (none required for this demo)

app = FastAPI(title="Adaptive Diagnostic Engine", lifespan=lifespan)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )

app.include_router(session_router)
app.include_router(questions_router)

@app.get("/")
def root():
    return {"message": "Adaptive Diagnostic Engine API is running."}

@app.get("/health")
def health():
    """Verify backend status quickly."""
    return {"status": "ok"}
