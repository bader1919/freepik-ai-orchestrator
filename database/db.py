"""Database connection and management"""

import asyncio
import asyncpg
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os

class DatabaseManager:
    """Async database manager for Freepik Orchestrator"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///freepik_orchestrator.db")
        self.pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self):
        """Initialize database connection pool"""
        try:
            # Only initialize if using PostgreSQL
            if self.database_url.startswith("postgresql"):
                self.pool = await asyncpg.create_pool(
                    self.database_url,
                    min_size=5,
                    max_size=20,
                    command_timeout=60
                )
                
                # Run migrations
                await self.run_migrations()
            else:
                print("Using SQLite - database operations will be mocked")
                
        except Exception as e:
            print(f"Database initialization failed: {str(e)}")
    
    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
    
    async def run_migrations(self):
        """Run database migrations"""
        if not self.pool:
            return
            
        async with self.pool.acquire() as conn:
            # Check if migrations table exists
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id SERIAL PRIMARY KEY,
                    version VARCHAR(50) NOT NULL,
                    applied_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Run initial migration
            migration_exists = await conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM migrations WHERE version = '001_initial')"
            )
            
            if not migration_exists:
                # Read and execute migration file
                migration_path = os.path.join(
                    os.path.dirname(__file__), 
                    "migrations", 
                    "001_initial.sql"
                )
                
                if os.path.exists(migration_path):
                    with open(migration_path, 'r') as f:
                        migration_sql = f.read()
                    
                    await conn.execute(migration_sql)
                    await conn.execute(
                        "INSERT INTO migrations (version) VALUES ('001_initial')"
                    )
                    print("Database migration 001_initial completed")
    
    # Task management methods
    async def create_task(self, task_data: Dict[str, Any]) -> str:
        """Create a new task record"""
        if not self.pool:
            # Mock implementation for development
            return f"mock_task_{hash(str(task_data)) % 100000}"
            
        async with self.pool.acquire() as conn:
            task_id = await conn.fetchval("""
                INSERT INTO freepik_tasks (
                    task_id, user_input, enhanced_prompt, model_used, 
                    source, task_type, environment, optimization_data, 
                    workflow_id, user_id
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                RETURNING id
            """, 
                task_data["task_id"],
                task_data["user_input"],
                task_data.get("enhanced_prompt"),
                task_data["model_used"],
                task_data["source"],
                task_data.get("task_type", "generation"),
                task_data.get("environment", "development"),
                json.dumps(task_data.get("optimization_data", {})),
                task_data.get("workflow_id"),
                task_data.get("user_id")
            )
            return str(task_id)
    
    async def update_task_status(self, task_id: str, status: str, 
                               result_data: Optional[Dict[str, Any]] = None) -> bool:
        """Update task status and result data"""
        if not self.pool:
            print(f"Mock: Updated task {task_id} status to {status}")
            return True
            
        async with self.pool.acquire() as conn:
            if status == "completed" and result_data:
                await conn.execute("""
                    UPDATE freepik_tasks 
                    SET status = $1, result_url = $2, thumbnail_url = $3, 
                        completed_at = NOW(),
                        processing_time_seconds = EXTRACT(EPOCH FROM (NOW() - created_at))
                    WHERE task_id = $4
                """, 
                    status,
                    result_data.get("image_url"),
                    result_data.get("thumbnail_url"),
                    task_id
                )
            elif status == "failed":
                await conn.execute("""
                    UPDATE freepik_tasks 
                    SET status = $1, error_message = $2, completed_at = NOW()
                    WHERE task_id = $3
                """, 
                    status,
                    result_data.get("error") if result_data else "Unknown error",
                    task_id
                )
            else:
                await conn.execute("""
                    UPDATE freepik_tasks SET status = $1 WHERE task_id = $2
                """, status, task_id)
            
            return True
    
    async def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task by task_id"""
        if not self.pool:
            # Mock data for development
            return {
                "task_id": task_id,
                "status": "completed",
                "model_used": "mystic",
                "created_at": datetime.now()
            }
            
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM freepik_tasks WHERE task_id = $1
            """, task_id)
            
            if row:
                return dict(row)
            return None

# Global database instance
db_manager = DatabaseManager()
