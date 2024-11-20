#! /usr/bin/python3

# Simple task manager 
# Author: Kieran Ryan
# Jan 2019

import json
import cmd
import datetime
import readline

# Read the Task data from the JSON file
with open('tasks.json', 'r') as f:
    tasks_dict = json.load(f)

# make a backup of the tasks file
with open('tasks.json.bak', 'w') as fp:
   json.dump(tasks_dict, fp)

# read the config data
with open('tasks.config', 'r') as fp2:
    conf_dict = json.load(fp2)

# get the next sequence number for the task list
task_counter = int(conf_dict['sequence-next'])

def save():
   global tasks_dict
   global config_dict
   with open('tasks.json', 'w') as fp:
      json.dump(tasks_dict, fp, sort_keys=True)
   with open('tasks.config', 'w') as fp2:
	   json.dump(conf_dict, fp2)
   print ("Saved")

# an individual item in row format
def print_item(key):
       date_due = 'YYYY-MM-DD'
       if 'date-due' in tasks_dict[key]:
              date_due = tasks_dict[key]['date-due'] 
       priority = 'Normal'
       if 'priority' in tasks_dict[key]:
              priority = tasks_dict[key]['priority'] 
       if 'note' in tasks_dict[key]:
          note = " ..."
       else:
          note = ""
	
       print(str(key) + " - " + date_due + " - " + priority + " - " + tasks_dict[key]['status'] 
			  + " - " + tasks_dict[key]['description'] + note)

def list_items():
   for key,value in sorted(tasks_dict.items(),  key=lambda x: int(x[0])):
       print_item(key)

def filter_items(filter):
   for key,value in sorted(tasks_dict.items(),  key=lambda x: int(x[0])):
       # print anything with the filter if applicable - if there's no filter also skip it
       if ('tag' in tasks_dict[key] and filter == tasks_dict[key]['tag']):
           print_item(key)

def search_items(search_string):
   for key,value in sorted(tasks_dict.items(),  key=lambda x: int(x[0])):
       # print anything with the filter if applicable - if there's no filter also skip it
       if (search_string.lower() in tasks_dict[key]['description'].lower()):
           print_item(key)
    
# Task processing
class TaskList:

	#def __init__(self):

	def all_items(self):
	   list_items()

	def filter_tasks(self, tag):
	   filter_items(filter=tag)

	def search_tasks(self, srch):
	   search_items(search_string=srch)

	def add_task(self, task):
		global task_counter
		now = datetime.datetime.now()
		current_date = now.strftime("%Y-%m-%d %H:%M")
		tasks_dict[str(task_counter)] = {'description':task, 'status' : 'Incomplete', 'date-created': current_date}
		print_item(str(task_counter))
		task_counter += 1
		# update the sequence number we will store to the config file
		conf_dict['sequence-next'] = task_counter

	def del_task(self, task):
		global tasks_dict
		del(tasks_dict[task])

        def done_task(self, task):
		global tasks_dict
		tasks_dict[task]['status'] = "Done"
		print_item(task)

	def prioritise_task(self, task):
		global tasks_dict
		tasks_dict[task]['priority'] = "HIGH"

        def due_task(self, task):
		global tasks_dict
		commands = task.split()
		try:
	           tasks_dict[commands[0]]['date-due'] = commands[1]
		except:
		   print "Could not apply due date"

	def note_task(self, task):
		global tasks_dict
		commands = task.split()
		try:
		   # rejoin the rest of the note string
		   sep = " "
		   note_temp = sep.join(commands[1:])
	           tasks_dict[commands[0]]['note'] = note_temp
		except:
		   print "Could not apply notes"

	def tag_task(self, task):
		global tasks_dict
		commands = task.split()
		try:
	           tasks_dict[commands[0]]['tag'] = commands[1]
		except:
		   print "Could not apply tag"

	# long form of the print showing all details
        def print_task(self, task):
			if task in tasks_dict:
				print("Description: " + tasks_dict[task]['description'])
				print("Status: " + tasks_dict[task]['status'])
				if 'date-created' in tasks_dict[task]:
					print("Date Created: " + tasks_dict[task]['date-created'])
				if 'date-due' in tasks_dict[task]:
					print("Date Due: " + tasks_dict[task]['date-due'])
				if 'note' in tasks_dict[task]:
					print("Note: " + tasks_dict[task]['note'])
				if 'tag' in tasks_dict[task]:
					print("Tag: " + tasks_dict[task]['tag'])

	def show_incomplete_tasks(self):
	   for key,value in sorted(tasks_dict.items(),  key=lambda x: int(x[0])):
	       # print anything with the filter if applicable - if there's no filter also skip it
	       if (tasks_dict[key]['status'] != "Done"):
		   print_item(key)
 
# Command line processor
class CommandProc(cmd.Cmd):
    """Simple command processor example."""

    prompt = 'taskmgr> '
    
    def do_all(self, line):
	'Usage: all (list all tasks)'		
	t = TaskList()
	t.all_items()
    
    def do_add(self, task):
        'Usage: add task-description (Adds a new task to your list)'
	t = TaskList()
	t.add_task(task)

    def do_del(self, task):
        'Usage: del {id} (Delete the task with the specified id)'
	t = TaskList()
	t.del_task(task)

    def do_done(self, task):
        'Usage: done {id} (Complete the task with the specified id)'
	t = TaskList()
	t.done_task(task)

    def do_print(self, task):
        'Usage: print {id} (Print to the screen the task with the specified id)'
	t = TaskList()
	t.print_task(task)

    def do_due(self, task):
        'Usage: due {id} {date} (Set a due date for this task with the specified id)'
	t = TaskList()
	t.due_task(task)

    def do_priority(self, task):
        'Usage: priority {id} (Set the priority of the task with the specified id to HIGH)'
	t = TaskList()
	t.prioritise_task(task)

    def do_note(self, task):
        'Usage: note {id} {note} (Set a text note for this task with the specified id)'
	t = TaskList()
	t.note_task(task)

    def do_tag(self, task):
        'Usage: tag {id} {tag} (Set a tag for this task with the specified id)'
	t = TaskList()
	t.tag_task(task)

    def do_save(self, task):
	'save your task list'
	save()

    def do_EOF(self, line):
	save()
        return True

    def do_filter(self, tag):
	'Usage: filter {tag} (filter by a specified tag)'
	t = TaskList()
	t.filter_tasks(tag)	

    def do_tbd(self, cmd):
	'Usage: tbd (list incomplete tasks)'
	t = TaskList()
	t.show_incomplete_tasks()

    def do_search(self, srch):
	'Usage: search {search-string} (search tasks for the specified string - ignores case)'
	t = TaskList()
	t.search_tasks(srch)

if __name__ == '__main__':
    CommandProc().cmdloop()
