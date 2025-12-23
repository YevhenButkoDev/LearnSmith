"""Main application entry point."""

from fastapi import FastAPI
from mentor_app.mentor.coordinator import MentorCoordinator

app = FastAPI(title="AI Mentor", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "AI Mentor API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
