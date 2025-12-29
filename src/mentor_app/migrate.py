#!/usr/bin/env python3
"""SQL migration runner."""

import sys
from pathlib import Path
from sqlalchemy import text
from infrastructure.database import DatabaseService


def ensure_migrations_table(db_service):
    """Create migrations table if it doesn't exist."""
    with db_service.engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS migrations (
                filename VARCHAR(255) PRIMARY KEY,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        conn.commit()


def get_executed_migrations(db_service):
    """Get list of already executed migrations."""
    with db_service.engine.connect() as conn:
        result = conn.execute(text("SELECT filename FROM migrations"))
        return {row[0] for row in result}


def execute_migration(db_service, filepath):
    """Execute a single migration file."""
    with open(filepath, 'r') as f:
        sql = f.read()
    
    with db_service.engine.connect() as conn:
        conn.execute(text(sql))
        conn.execute(
            text("INSERT INTO migrations (filename) VALUES (:filename)"),
            {"filename": filepath.name}
        )
        conn.commit()
    print(f"✅ Executed {filepath.name}")


def migrate():
    """Execute SQL migrations in alphabetical order."""
    db_service = DatabaseService()
    ensure_migrations_table(db_service)
    
    migrations_dir = Path(__file__).parent / "migrations"
    if not migrations_dir.exists():
        print("No migrations directory found")
        return
    
    executed = get_executed_migrations(db_service)
    sql_files = sorted(migrations_dir.glob("*.sql"))
    
    for sql_file in sql_files:
        if sql_file.name not in executed:
            execute_migration(db_service, sql_file)
    
    print("✅ All migrations completed")


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    migrate()
