from app.db.session import get_db_connection
from typing import Optional
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
import sqlite3
from app.schemas.common import TaskStatus
from typing import List


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
            cursor.execute(
                """
                SELECT id, title, description, priority, status, created_at, updated_at
                FROM tasks
                WHERE id = ?
                """,
                (new_task_id,),
            )
            row = cursor.fetchone()
            return TaskResponse.model_validate(row)

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[TaskResponse]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, title, description, priority, status, created_at, updated_at
                FROM tasks
                WHERE id = ?
                """,
                (task_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            return TaskResponse.model_validate(row)
    @staticmethod
    def list_tasks(status_filter: Optional[TaskStatus] = None) -> List[TaskResponse]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if status_filter:
                cursor.execute(
                    """
                    SELECT id, title, description, priority, status, created_at, updated_at
                    FROM tasks
                    WHERE status = ?
                    ORDER BY id ASC
                    """,
                    (status_filter.value,)
                )
            else:
                cursor.execute(
                    """
                    SELECT id, title, description, priority, status, created_at, updated_at
                    FROM tasks
                    ORDER BY id ASC
                    """
                )
            rows = cursor.fetchall()
            return [TaskResponse.model_validate(row) for row in rows]
   