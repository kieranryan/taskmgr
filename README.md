# TaskMgr

A simple task management application with both command-line and web interfaces.

## Features

- Create, update, and delete tasks
- Set task status (Incomplete, Doing, Done)
- Set priorities, due dates, tags, and notes
- Filter tasks by status or tag
- Search tasks by description
- Two interfaces: CLI and Web

## Installation

### Requirements

- Python 3.9+
- Flask 3.0.0 (for web interface)

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

Run the CLI version:

```bash
python3 taskmgr_cli.py
```

#### CLI Commands

- `all` - List all tasks
- `add <description>` - Add a new task
- `del <id>` - Delete a task
- `done <id>` - Mark task as complete
- `doing <id>` - Mark task as in-progress
- `print <id>` - Show detailed task information
- `due <id> <date>` - Set due date (format: YYYY-MM-DD)
- `priority <id>` - Set task priority to HIGH
- `note <id> <text>` - Add a note to task
- `tag <id> <tag>` - Add a tag to task
- `filter <tag>` - Filter tasks by tag
- `search <query>` - Search tasks by description
- `tbd` - List incomplete tasks (To Be Done)
- `save` - Manually save tasks
- `Ctrl+D` - Save and exit

### Web Interface

Run the web server:

```bash
python3 run_web.py
```

Then open your browser to: `http://localhost:5001`

#### Web Features

- Modern, responsive UI
- Add tasks with a single click
- Filter by status (All, To Do, Doing, Done)
- Real-time search
- Click on tasks to view details
- Edit tasks (status, priority, due date, tags, notes)
- Quick action buttons (Start, Complete, Delete)
- Visual indicators for:
  - Task status (color-coded borders)
  - High priority tasks (red badge)
  - Tags (blue badge)
  - Overdue tasks (red due date)
  - Tasks with notes (📝 indicator)

## Data Storage

Tasks are stored in JSON files:
- `tasks.json` - Task data
- `tasks.config` - Configuration (sequence counter)
- `tasks.json.bak` - Automatic backup

Both CLI and web interfaces share the same data files, so you can switch between them seamlessly.

## Architecture

The application is structured in layers:

```
taskmgr/
├── taskmgr/          # Core package
│   ├── models.py     # Task data models
│   ├── storage.py    # JSON file operations
│   ├── service.py    # Business logic
│   └── cli.py        # CLI interface
├── web/              # Web application
│   ├── app.py        # Flask application
│   ├── api.py        # REST API endpoints
│   ├── templates/    # HTML templates
│   └── static/       # CSS and JavaScript
├── taskmgr_cli.py    # CLI entry point
└── run_web.py        # Web server entry point
```

## REST API

The web interface uses a REST API that can also be accessed directly:

- `GET /api/tasks` - Get all tasks
- `GET /api/tasks/<id>` - Get single task
- `POST /api/tasks` - Create task (JSON: `{"description": "..."}`)
- `PUT /api/tasks/<id>` - Update task (JSON: `{"status": "...", "priority": "...", ...}`)
- `DELETE /api/tasks/<id>` - Delete task
- `GET /api/tasks/filter/tag/<tag>` - Filter by tag
- `GET /api/tasks/filter/status/<status>` - Filter by status
- `GET /api/tasks/search?q=<query>` - Search tasks

## Development

### Project History

- **2019**: Original CLI version created
- **2025**: Refactored with clean architecture and added web interface

### Author

Kieran Ryan
