# TaskFlow CLI

A command-line task manager written in Python using SQLite for storage and Pydantic for validation.

## Features

- Add, view, search, update, and delete tasks
- Filter tasks by status (pending, in_progress, completed)
- Partial updates (change only the fields you want to edit)
- Input validation using Pydantic schemas

## Project Structure

```text
taskflow-cli/
├── app/
│   ├── cli/
│   │   ├── router.py         # Menu loop and user choices
│   │   └── views.py          # Tables and terminal prompts
│   ├── core/
│   │   └── config.py         # Paths and settings
│   ├── db/
│   │   └── session.py        # Database connection and table setup
│   ├── schemas/
│   │   ├── common.py         # Status and Priority enums
│   │   └── task.py           # Pydantic models
│   └── services/
│       └── task_service.py   # Database queries and business logic
├── requirements.txt
└── README.md