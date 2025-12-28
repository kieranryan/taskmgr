"""Command-line interface for TaskMgr."""

import cmd
import readline
from .models import Task, TaskStatus, Priority
from .service import TaskService
from .storage import TaskStorage


def format_task_row(task: Task) -> str:
    """Format a task as a single row for display."""
    date_due = task.date_due if task.date_due else ''
    tag = task.tag if task.tag else '     '
    priority = task.priority.value
    note_indicator = " ..." if task.note else ""

    return (f"{task.id} - {tag:>5} - {date_due} - {priority} - {task.status.value} "
            f"- {task.description}{note_indicator}")


def format_task_detail(task: Task) -> str:
    """Format a task with all details for display."""
    lines = [
        f"Description: {task.description}",
        f"Status: {task.status.value}"
    ]

    if task.date_created:
        lines.append(f"Date Created: {task.date_created}")
    if task.date_due:
        lines.append(f"Date Due: {task.date_due}")
    if task.note:
        lines.append(f"Note: {task.note}")
    if task.tag:
        lines.append(f"Tag: {task.tag}")

    return "\n".join(lines)


class TaskCLI(cmd.Cmd):
    """Command-line processor for task management."""

    prompt = 'taskmgr> '

    def __init__(self):
        """Initialize CLI with task service."""
        super().__init__()
        storage = TaskStorage()
        self.service = TaskService(storage)

    def do_all(self, line):
        """Usage: all (list all tasks)"""
        for task in self.service.get_tasks_sorted():
            print(format_task_row(task))

    def do_add(self, task_desc):
        """Usage: add task-description (Adds a new task to your list)"""
        if not task_desc.strip():
            print("Error: Task description cannot be empty")
            return
        task = self.service.add_task(task_desc)
        print(format_task_row(task))

    def do_del(self, task_id):
        """Usage: del {id} (Delete the task with the specified id)"""
        if self.service.delete_task(task_id):
            print(f"Task {task_id} deleted")
        else:
            print(f"No such task: {task_id}")

    def do_done(self, task_id):
        """Usage: done {id} (Complete the task with the specified id)"""
        task = self.service.update_task_status(task_id, TaskStatus.DONE)
        if task:
            print(format_task_row(task))
        else:
            print("No such task")

    def do_doing(self, task_id):
        """Usage: doing {id} (Start the task with the specified id)"""
        task = self.service.update_task_status(task_id, TaskStatus.DOING)
        if task:
            print(format_task_row(task))
        else:
            print("No such task")

    def do_print(self, task_id):
        """Usage: print {id} (Print to the screen the task with the specified id)"""
        task = self.service.get_task(task_id)
        if task:
            print(format_task_detail(task))
        else:
            print("No such task")

    def do_due(self, args):
        """Usage: due {id} {date} (Set a due date for this task with the specified id)"""
        parts = args.split()
        if len(parts) < 2:
            print("Could not apply due date")
            return

        task_id = parts[0]
        date = parts[1]
        task = self.service.set_due_date(task_id, date)
        if not task:
            print("Could not apply due date")

    def do_priority(self, task_id):
        """Usage: priority {id} (Set the priority of the task with the specified id to HIGH)"""
        task = self.service.set_priority(task_id)
        if not task:
            print("No such task")

    def do_note(self, args):
        """Usage: note {id} {note} (Set a text note for this task with the specified id)"""
        parts = args.split()
        if len(parts) < 2:
            print("Could not apply notes")
            return

        task_id = parts[0]
        note = " ".join(parts[1:])
        task = self.service.add_note(task_id, note)
        if not task:
            print("Could not apply notes")

    def do_tag(self, args):
        """Usage: tag {id} {tag} (Set a tag for this task with the specified id)"""
        parts = args.split()
        if len(parts) < 2:
            print("Could not apply tag")
            return

        task_id = parts[0]
        tag = parts[1]
        task = self.service.add_tag(task_id, tag)
        if not task:
            print("Could not apply tag")

    def do_save(self, line):
        """save your task list"""
        if self.service.save():
            print("Saved")
        else:
            print("Error saving")

    def do_EOF(self, line):
        """Handle Ctrl+D to exit"""
        self.service.save()
        return True

    def do_filter(self, tag):
        """Usage: filter {tag} (filter by a specified tag)"""
        tasks = self.service.filter_by_tag(tag)
        for task in tasks:
            print(format_task_row(task))

    def do_tbd(self, line):
        """Usage: tbd (list incomplete tasks)"""
        tasks = self.service.get_incomplete_tasks()
        for task in tasks:
            print(format_task_row(task))

    def do_search(self, query):
        """Usage: search {search-string} (search tasks for the specified string - ignores case)"""
        tasks = self.service.search_tasks(query)
        for task in tasks:
            print(format_task_row(task))
