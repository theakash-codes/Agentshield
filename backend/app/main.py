from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.api.agents import router as agents_router
from app.api.transactions import router as transactions_router


app = FastAPI(
    title="AgentShield",
    description="AI Agent Trust, Risk & Security Layer",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(agents_router)
app.include_router(transactions_router)


app.mount(
    "/dashboard",
    StaticFiles(directory="../frontend", html=True),
    name="dashboard"
)


@app.get("/")
def root():
    return RedirectResponse(url="/dashboard/")