"""Main application entry point."""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from mentor_app.api.courses import router as courses_router
from mentor_app.api.modules import router as modules_router

app = FastAPI(title="AI Mentor", version="0.1.0")

# Include API routers
app.include_router(courses_router)
app.include_router(modules_router)

@app.get("/")
async def root():
    return {"message": "AI Mentor API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
