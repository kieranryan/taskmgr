#! /usr/bin/python3

"""
TaskMgr Web Server Entry Point

Starts the Flask web server for the task manager.
Author: Kieran Ryan
2025
"""

from web.app import create_app

if __name__ == '__main__':
    app = create_app()
    print("Starting TaskMgr web interface at http://localhost:5001")
    app.run(debug=True, port=5001, host='0.0.0.0')
