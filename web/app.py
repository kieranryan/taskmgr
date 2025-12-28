"""Flask application factory for TaskMgr web interface."""

from flask import Flask, jsonify
from taskmgr.storage import TaskStorage
from taskmgr.service import TaskService


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)

    # Initialize task service as a singleton
    storage = TaskStorage()
    app.task_service = TaskService(storage)

    # Register blueprints
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Serve the main page
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app
