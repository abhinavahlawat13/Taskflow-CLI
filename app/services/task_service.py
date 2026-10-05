from app.db.session import get_db_connection
from typing import Optional
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
import sqlite3
from app.schemas.common import TaskStatus


class TaskService:
    @staticmethod
    def create_task(task_data: TaskCreate) -> TaskResponse:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (title, description, priority, status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    task_data.title,
                    task_data.description,
                    task_data.priority.value,
                    task_data.status.value,
                ),
            )

            new_task_id = cursor.lastrowid
            cursor.execute("""
                SELECT id,title,description,priority,status,created_at,updated_at FROM tasks WHERE Id=?
                """,(new_task_id,)
                )
            row = cursor.fetchone()
            return TaskResponse.model_validate(row)