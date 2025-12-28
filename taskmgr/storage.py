"""Storage layer for TaskMgr - handles JSON file persistence."""

import json
import os
import fcntl
from typing import Dict
from .models import Task


class TaskStorage:
    """Handles loading and saving tasks to JSON files."""

    def __init__(self, tasks_file: str = 'tasks.json', config_file: str = 'tasks.config'):
        """Initialize storage with file paths."""
        self.tasks_file = tasks_file
        self.config_file = config_file

    def load_tasks(self) -> Dict[str, Task]:
        """Load tasks from JSON file."""
        try:
            with open(self.tasks_file, 'r') as f:
                tasks_dict = json.load(f)

            # Convert dict to Task objects
            tasks = {}
            for task_id, task_data in tasks_dict.items():
                tasks[task_id] = Task.from_dict(task_id, task_data)

            return tasks
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing {self.tasks_file}: {e}")

    def save_tasks(self, tasks: Dict[str, Task]) -> None:
        """Save tasks to JSON file with backup."""
        # Create backup if file exists
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    backup_data = json.load(f)
                with open(f'{self.tasks_file}.bak', 'w') as f:
                    json.dump(backup_data, f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass

        # Convert Task objects to dict
        tasks_dict = {}
        for task_id, task in tasks.items():
            tasks_dict[task_id] = task.to_dict()

        # Write to file with file locking
        with open(self.tasks_file, 'w') as f:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                json.dump(tasks_dict, f, sort_keys=True)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def load_config(self) -> dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'sequence-next': 1}
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing {self.config_file}: {e}")

    def save_config(self, config: dict) -> None:
        """Save configuration to JSON file."""
        with open(self.config_file, 'w') as f:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                json.dump(config, f)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def get_next_sequence(self) -> int:
        """Get and increment the next sequence number."""
        config = self.load_config()
        current = config.get('sequence-next', 1)
        config['sequence-next'] = current + 1
        self.save_config(config)
        return current
