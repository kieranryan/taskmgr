"""REST API endpoints for TaskMgr."""

from flask import Blueprint, jsonify, request, current_app
from taskmgr.models import TaskStatus, Priority

api_bp = Blueprint('api', __name__)


def get_service():
    """Get the task service from the current app."""
    service = current_app.task_service
    # Reload from disk to pick up CLI changes
    service.reload()
    return service


def task_to_dict(task):
    """Convert a Task object to a dictionary for JSON response."""
    result = {
        'id': task.id,
        'description': task.description,
        'status': task.status.value,
        'date_created': task.date_created,
        'priority': task.priority.value
    }
    if task.date_due:
        result['date_due'] = task.date_due
    if task.note:
        result['note'] = task.note
    if task.tag:
        result['tag'] = task.tag
    return result


@api_bp.route('/tasks', methods=['GET'])
def get_all_tasks():
    """Get all tasks."""
    service = get_service()
    tasks = service.get_tasks_sorted()
    return jsonify({
        'tasks': [task_to_dict(task) for task in tasks]
    })


@api_bp.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task by ID."""
    service = get_service()
    task = service.get_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task_to_dict(task))


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.get_json()
    if not data or 'description' not in data:
        return jsonify({'error': 'Description is required'}), 400

    description = data['description'].strip()
    if not description:
        return jsonify({'error': 'Description cannot be empty'}), 400

    service = get_service()
    task = service.add_task(description)
    service.save()

    return jsonify(task_to_dict(task)), 201


@api_bp.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task."""
    service = get_service()
    task = service.get_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Update status
    if 'status' in data:
        try:
            status = TaskStatus(data['status'])
            service.update_task_status(task_id, status)
        except ValueError:
            return jsonify({'error': 'Invalid status'}), 400

    # Update priority
    if 'priority' in data:
        try:
            priority = Priority(data['priority'])
            service.set_priority(task_id, priority)
        except ValueError:
            return jsonify({'error': 'Invalid priority'}), 400

    # Update due date
    if 'date_due' in data:
        service.set_due_date(task_id, data['date_due'])

    # Update note
    if 'note' in data:
        service.add_note(task_id, data['note'])

    # Update tag
    if 'tag' in data:
        service.add_tag(task_id, data['tag'])

    service.save()
    updated_task = service.get_task(task_id)
    return jsonify(task_to_dict(updated_task))


@api_bp.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    service = get_service()
    if not service.delete_task(task_id):
        return jsonify({'error': 'Task not found'}), 404

    service.save()
    return jsonify({'success': True})


@api_bp.route('/tasks/filter/tag/<tag>', methods=['GET'])
def filter_by_tag(tag):
    """Filter tasks by tag."""
    service = get_service()
    tasks = service.filter_by_tag(tag)
    return jsonify({
        'tasks': [task_to_dict(task) for task in tasks]
    })


@api_bp.route('/tasks/filter/status/<status>', methods=['GET'])
def filter_by_status(status):
    """Filter tasks by status."""
    try:
        task_status = TaskStatus(status)
    except ValueError:
        return jsonify({'error': 'Invalid status'}), 400

    service = get_service()
    tasks = service.filter_by_status(task_status)
    return jsonify({
        'tasks': [task_to_dict(task) for task in tasks]
    })


@api_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    """Search tasks by description."""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400

    service = get_service()
    tasks = service.search_tasks(query)
    return jsonify({
        'tasks': [task_to_dict(task) for task in tasks]
    })


@api_bp.route('/save', methods=['POST'])
def save_data():
    """Manually trigger save."""
    service = get_service()
    if service.save():
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Save failed'}), 500
