""" revna.py
    @brief a personal assistant to improve your daily shredding.
    @author gunnarpope
    @date   6/14/22

"""
from datetime import datetime as dt
import pandas as pd
import argparse
import json
import os

# load the todo list
REVNA_ROOT = os.getenv('REVNA_ROOT')
filename = REVNA_ROOT + 'todo/list.json'
df_filename = REVNA_ROOT + 'todo/todo.json'
df = pd.read_json(df_filename)

class Todo():
    def __init__(self, task, project=None, status='todo',  due=None, level='low', category=None):
        self.category = category 
        self.task     = task
        self.level    = level 
        self.status   = status
        self.origin   = dt.now().strftime('%Y-%m-%d')
        self.due      = due

def GetPending():
    tasks = df[ df['status'] != 'done']
    if tasks.size == 0:
        print('Congratulations - You have no pending tasks!')
    else:
        print(tasks)

def RemoveTask(id):
    id = int(id)
    df.loc[int(id), 'rm_date'] = dt.now().strftime('%Y-%m-%d')
    df.loc[int(id), 'status'] = 'removed'
    print('Task Removed: ')
    print(df.loc[id])

def MarkTaskAsDone(id):
    id = int(id)
    df.loc[int(id), 'done_date'] = dt.now().strftime('%Y-%m-%d')
    df.loc[int(id), 'status'] = 'done'
    print('Task Done: ')
    print(df.loc[id])

def MarkTaskAsUndone(id):
    id = int(id)
    df.loc[int(id), 'done_date'] = 'NaN' 
    df.loc[int(id), 'status'] = 'todo'
    print('Task Done: ')
    print(df.loc[id])


parser = argparse.ArgumentParser(description="I'm Revna - your personal, get-shit-done assistant.")
parser.add_argument("--add",     type=str, help="Add an item to the todo list")
parser.add_argument("--all",      help="List all tasks", action='store_true')
parser.add_argument("--due",           type=str, help="Add a due date to an item")
parser.add_argument("-d", "--done",    type=str, help="Mark task as done")
parser.add_argument("-u", "--undone",    type=str, help="Mark task as undone")
parser.add_argument("-s", "--status",  type=str, help="The status of the task ( todo | doing | done )")
parser.add_argument("-i", "--importance", type=str, help="The importance level of the task ( low | med | high )")
parser.add_argument("-c", "--category", type=str, help="The category of the task.")
parser.add_argument("-l", "--list",     action='store_true', help="List all pending tasks.")
parser.add_argument("-g", "--go",       action='store_true', help="Revna, let's go!")
parser.add_argument("-r", "--remove",   type=str, help="Remove a task")
args = parser.parse_args()

# parse the arguments
if args.add:
    print('Todo: ', args.add)

    task = Todo(task=args.add, level=args.importance, status=args.status, due=args.due)

    df_new = pd.DataFrame(task.__dict__, index=[1])
    df = pd.concat([df, df_new], ignore_index=True)

elif args.list:
    print(df[ df['status'] != 'done'])

elif args.all:
    print(df)

elif args.go:
    print("Hello, Gunnar.")
    print("Here are your tasks for today:")
    GetPending()

elif args.remove:
    print('Removing Task: ', args.remove)
    RemoveTask(args.remove)
    df.to_json(df_filename)

elif args.done:
    MarkTaskAsDone(args.done)
    df.to_json(df_filename)

elif args.done:
    MarkTaskAsUndone(args.undone)
    df.to_json(df_filename)

else:
    print("Here's what you have to do today...\n")
    GetPending()


# write the final result to file.
df.to_json(df_filename )
