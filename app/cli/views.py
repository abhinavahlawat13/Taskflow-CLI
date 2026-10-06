from typing import List,Optional
from pydantic import ValidationError
from app.schemas.common import TaskPriority, TaskStatus
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

def display_tasks_table(tasks: List[TaskResponse]) -> None:
    if not tasks:
        print("No tasks found. ")
        return
    header = f"{'ID':<4} | {'Title':<25} | {'Priority':<8} | {'Status':<12} | {'Created At':<19}"
    separator = "-" * len(header)
    print("\n" + separator)
    print(header)
    print(separator)

    for t in tasks:
        title_display = (t.title[:22] + "...") if len(t.title) > 25 else t.title
        created = t.created_at.strftime("%Y-%m-%d %H:%M")
        print(f"{t.id:<4} | {title_display:<25} | {t.priority.value:<8} | {t.status.value:<12} | {created:<19}")
    print(separator + "\n")


def view_list_tasks() -> None:
    """Prompts for optional status filter and displays tasks."""
    print("\n--- View Tasks ---")
    filter_choice = input("Filter by status? (pending, in_progress, completed, or press Enter for all): ").strip().lower()
    status_filter = None
    if filter_choice:
        try:
            status_filter = TaskStatus(filter_choice)
        except ValueError:
            print("[!] Invalid status filter provided. Displaying all tasks.")

    tasks = TaskService.list_tasks(status_filter=status_filter)
    display_tasks_table(tasks)


def view_create_task() -> None:
    """Collects user input, validates via Pydantic, and creates a new task."""
    print("\n--- Create New Task ---")
    title = input("Title: ").strip()
    description = input("Description (Optional, press Enter to skip): ").strip()
    priority_input = input("Priority (low, medium, high) [default: medium]: ").strip().lower() or "medium"
    status_input = input("Status (pending, in_progress, completed) [default: pending]: ").strip().lower() or "pending"

    try:
        task_in = TaskCreate(
            title=title,
            description=description if description else None,
            priority=TaskPriority(priority_input),
            status=TaskStatus(status_input)
        )
        created = TaskService.create_task(task_in)
        print(f"\n[+] Success: Task #{created.id} '{created.title}' created.")
    except (ValidationError, ValueError) as e:
        print(f"\n[X] Validation Error: {e}")


def view_search_tasks() -> None:
    """Queries tasks matching a keyword in title or description."""
    keyword = input("\nEnter search keyword: ").strip()
    if not keyword:
        print("[!] Search keyword cannot be blank.")
        return
    tasks = TaskService.search_tasks(keyword)
    display_tasks_table(tasks)


def view_update_task() -> None:
    """Prompts for task ID and partial field changes, then submits updates."""
    print("\n--- Update Task ---")
    task_id_str = input("Enter Task ID: ").strip()
    if not task_id_str.isdigit():
        print("[!] Task ID must be a valid integer.")
        return
    task_id = int(task_id_str)

    existing = TaskService.get_task_by_id(task_id)
    if not existing:
        print(f"[X] Task #{task_id} does not exist.")
        return

    print(f"Updating Task #{task_id}: '{existing.title}' (Leave blank to keep current value)")
    new_title = input(f"New Title [{existing.title}]: ").strip()
    new_desc = input("New Description: ").strip()
    new_priority = input(f"New Priority [{existing.priority.value}]: ").strip()
    new_status = input(f"New Status [{existing.status.value}]: ").strip()

    update_payload = {}
    if new_title:
        update_payload["title"] = new_title
    if new_desc:
        update_payload["description"] = new_desc
    if new_priority:
        try:
            update_payload["priority"] = TaskPriority(new_priority.lower())
        except ValueError:
            print("[!] Invalid priority provided. Keeping existing value.")
    if new_status:
        try:
            update_payload["status"] = TaskStatus(new_status.lower())
        except ValueError:
            print("[!] Invalid status provided. Keeping existing value.")

    try:
        task_update_obj = TaskUpdate(**update_payload)
        updated = TaskService.update_task(task_id, task_update_obj)
        if updated:
            print(f"\n[+] Success: Task #{updated.id} updated.")
        else:
            print("\n[!] No changes applied.")
    except ValidationError as e:
        print(f"\n[X] Validation Error: {e}")


def view_delete_task() -> None:
    """Prompts for task ID and confirmation before deletion."""
    print("\n--- Delete Task ---")
    task_id_str = input("Enter Task ID to delete: ").strip()
    if not task_id_str.isdigit():
        print("[!] Task ID must be a valid integer.")
        return
    task_id = int(task_id_str)

    confirm = input(f"Are you sure you want to delete Task #{task_id}? (y/N): ").strip().lower()
    if confirm == "y":
        deleted = TaskService.delete_task(task_id)
        if deleted:
            print(f"[+] Task #{task_id} successfully deleted.")
        else:
            print(f"[X] Task #{task_id} not found.")
    else:
        print("[-] Deletion canceled.")