#! /usr/bin/python3

"""
TaskMgr CLI Entry Point

Simple task manager with command-line interface.
Author: Kieran Ryan
Jan 2019/2025
"""

from taskmgr.cli import TaskCLI

if __name__ == '__main__':
    TaskCLI().cmdloop()
