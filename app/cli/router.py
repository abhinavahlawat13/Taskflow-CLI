import sys
from app.db.session import init_db
from app.cli.views import (
    view_list_tasks,
    view_create_task,
    view_search_tasks,
    view_update_task,
    view_delete_task
)


def start_cli() -> None:
    """Initializes the database schema and runs the interactive menu loop."""
    init_db()

    menu = (
        "\n=============================="
        "\n       TASKFLOW CLI MENU      "
        "\n=============================="
        "\n1. List All Tasks"
        "\n2. Create New Task"
        "\n3. Search Tasks"
        "\n4. Update Task"
        "\n5. Delete Task"
        "\n6. Exit"
        "\n=============================="
    )

    routes = {
        "1": view_list_tasks,
        "2": view_create_task,
        "3": view_search_tasks,
        "4": view_update_task,
        "5": view_delete_task
    }

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "6":
            print("\nExiting TaskFlow. Goodbye!")
            sys.exit(0)

        action = routes.get(choice)
        if action:
            action()
        else:
            print("\n[!] Invalid selection. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    start_cli()