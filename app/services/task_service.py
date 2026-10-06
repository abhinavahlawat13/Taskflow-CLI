from app.db.session import get_db_connection
from typing import Optional,List
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

    @staticmethod
    def search_tasks(keyword: str) -> List[TaskResponse]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            pattern = f"%{keyword}%"
            cursor.execute(
                """
                SELECT id, title, description, priority, status, created_at, updated_at
                FROM tasks
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY id ASC
                """,
                (pattern, pattern),
            )
            rows = cursor.fetchall()
            return [TaskResponse.model_validate(row) for row in rows]

    @staticmethod
    def update_task(
        task_id: int, task_data: TaskUpdate
    ) -> Optional[TaskResponse]:
        updates = task_data.model_dump(exclude_unset=True)
        if not updates:
            return TaskService.get_task_by_id(task_id)

        clean_updates = {
            k: (v.value if hasattr(v, "value") else v) for k, v in updates.items()
        }
        set_clause = ", ".join([f"{col} = ?" for col in clean_updates.keys()])
        query = (
            f"UPDATE tasks SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        )
        params = list(clean_updates.values()) + [task_id]
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if cursor.rowcount == 0:
                return None

            cursor.execute(
                """
                SELECT id, title, description, priority, status, created_at, updated_at
                FROM tasks
                WHERE id = ?
                """,
                (task_id,),
            )
            row = cursor.fetchone()
            return TaskResponse.model_validate(row)

    @staticmethod
    def delete_task(task_id: int) -> bool:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cursor.rowcount > 0