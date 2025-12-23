# LearnSmith - AI Mentor

AI-powered adaptive learning mentor that creates personalized courses and guides users through interactive learning experiences.

## Project Structure

```
LearnSmith/
├── pyproject.toml             # Project dependencies and configuration
├── .env.example              # Environment variables template
├── src/
│   └── mentor_app/
│       ├── main.py           # FastAPI application entry point
│       ├── architect/        # Course planning and curriculum design
│       ├── builder/          # Content generation and quiz creation
│       ├── mentor/           # Main orchestrator and session management
│       ├── auditor/          # Analytics and progress tracking
│       └── infrastructure/   # Database, LLM client, and external services
├── tests/                    # Unit and integration tests
├── ui/                       # Frontend (placeholder)
└── docs/                     # Documentation
```

## Getting Started

1. Copy `.env.example` to `.env` and configure your environment variables
2. Install dependencies: `pip install -e .`
3. Run the application: `uvicorn src.mentor_app.main:app --reload`

## Architecture

The application follows Clean Architecture principles with four main modules:

- **Architect**: Strategic course planning and curriculum design
- **Builder**: Tactical content creation and quiz generation  
- **Mentor**: Orchestrates the learning process and manages user sessions
- **Auditor**: Tracks progress and provides analytics
- **Infrastructure**: Handles external dependencies (database, LLM, etc.)
