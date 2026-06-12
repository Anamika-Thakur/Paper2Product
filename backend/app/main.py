from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import create_tables
from app.routers import auth, projects

settings = get_settings()

app = FastAPI(
    title="Research-to-Product Advisor",
    version="2.0.0",
    description="AI Venture Studio — 15-agent pipeline with debate, scoring, and full traceability",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://paper2product.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)


@app.on_event("startup")
def startup():
    create_tables()  # auto-creates all tables on first run (no Alembic needed)


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}
