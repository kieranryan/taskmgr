"""Data models for TaskMgr."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime


class TaskStatus(str, Enum):
    """Task status values."""
    INCOMPLETE = "Incomplete"
    DOING = "Doing"
    DONE = "Done"


class Priority(str, Enum):
    """Task priority values."""
    NORMAL = "Normal"
    HIGH = "HIGH"


@dataclass
class Task:
    """Represents a task with all its properties."""

    id: str
    description: str
    status: TaskStatus = TaskStatus.INCOMPLETE
    date_created: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))
    date_due: Optional[str] = None
    priority: Priority = Priority.NORMAL
    note: Optional[str] = None
    tag: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert Task to dictionary format matching JSON storage."""
        result = {
            'description': self.description,
            'status': self.status.value,
            'date-created': self.date_created,
        }

        if self.date_due:
            result['date-due'] = self.date_due
        if self.priority != Priority.NORMAL:
            result['priority'] = self.priority.value
        if self.note:
            result['note'] = self.note
        if self.tag:
            result['tag'] = self.tag

        return result

    @classmethod
    def from_dict(cls, task_id: str, data: dict) -> 'Task':
        """Create Task from dictionary (JSON format)."""
        return cls(
            id=task_id,
            description=data['description'],
            status=TaskStatus(data.get('status', 'Incomplete')),
            date_created=data.get('date-created', ''),
            date_due=data.get('date-due'),
            priority=Priority(data.get('priority', 'Normal')),
            note=data.get('note'),
            tag=data.get('tag')
        )

    def validate(self) -> bool:
        """Validate task data."""
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty")
        if not self.id:
            raise ValueError("Task ID cannot be empty")
        return True
