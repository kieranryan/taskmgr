"""Business logic layer for TaskMgr."""

from typing import Dict, List, Optional
from datetime import datetime
from .models import Task, TaskStatus, Priority
from .storage import TaskStorage


class TaskService:
    """Core business logic for task management."""

    def __init__(self, storage: TaskStorage):
        """Initialize service with storage backend."""
        self.storage = storage
        self.tasks: Dict[str, Task] = {}
        self.config: dict = {}
        self.load()

    def load(self) -> None:
        """Load tasks and config from storage."""
        self.tasks = self.storage.load_tasks()
        self.config = self.storage.load_config()

    def reload(self) -> None:
        """Reload tasks from storage (for web to pick up CLI changes)."""
        self.load()

    def save(self) -> bool:
        """Save tasks and config to storage."""
        try:
            self.storage.save_tasks(self.tasks)
            self.storage.save_config(self.config)
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False

    def add_task(self, description: str) -> Task:
        """Add a new task and return it."""
        task_id = str(self.config.get('sequence-next', 1))
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d %H:%M")

        task = Task(
            id=task_id,
            description=description,
            status=TaskStatus.INCOMPLETE,
            date_created=current_date
        )

        self.tasks[task_id] = task
        self.config['sequence-next'] = int(task_id) + 1

        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a single task by ID."""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> Dict[str, Task]:
        """Get all tasks."""
        return self.tasks

    def get_tasks_sorted(self) -> List[Task]:
        """Get all tasks sorted by ID in descending order (newest first)."""
        return [self.tasks[key] for key in sorted(self.tasks.keys(), key=lambda x: int(x), reverse=True)]

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def update_task_status(self, task_id: str, status: TaskStatus) -> Optional[Task]:
        """Update task status."""
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            return self.tasks[task_id]
        return None

    def set_priority(self, task_id: str, priority: Priority = Priority.HIGH) -> Optional[Task]:
        """Set task priority."""
        if task_id in self.tasks:
            self.tasks[task_id].priority = priority
            return self.tasks[task_id]
        return None

    def set_due_date(self, task_id: str, date: str) -> Optional[Task]:
        """Set task due date."""
        if task_id in self.tasks:
            self.tasks[task_id].date_due = date
            return self.tasks[task_id]
        return None

    def add_note(self, task_id: str, note: str) -> Optional[Task]:
        """Add a note to a task."""
        if task_id in self.tasks:
            self.tasks[task_id].note = note
            return self.tasks[task_id]
        return None

    def add_tag(self, task_id: str, tag: str) -> Optional[Task]:
        """Add a tag to a task."""
        if task_id in self.tasks:
            self.tasks[task_id].tag = tag
            return self.tasks[task_id]
        return None

    def filter_by_tag(self, tag: str) -> List[Task]:
        """Filter tasks by tag."""
        result = []
        for task in self.get_tasks_sorted():
            if task.tag == tag:
                result.append(task)
        return result

    def filter_by_status(self, status: TaskStatus) -> List[Task]:
        """Filter tasks by status."""
        result = []
        for task in self.get_tasks_sorted():
            if task.status == status:
                result.append(task)
        return result

    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by description (case-insensitive)."""
        result = []
        query_lower = query.lower()
        for task in self.get_tasks_sorted():
            if query_lower in task.description.lower():
                result.append(task)
        return result

    def get_incomplete_tasks(self) -> List[Task]:
        """Get all incomplete tasks (not Done)."""
        result = []
        for task in self.get_tasks_sorted():
            if task.status != TaskStatus.DONE:
                result.append(task)
        return result
