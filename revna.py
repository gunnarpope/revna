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

def CreateTodo(task):
    print('Todo: ', task)
    global df
    task = Todo(task=task, level=args.importance, status=args.status, due=args.due)

    df_new = pd.DataFrame(task.__dict__, index=[1])
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_json(df_filename)

class Todo():
    def __init__(self, task, project=None, status='todo',  due=None, level='low', category=None):
        self.category = category 
        self.task     = task
        self.level    = level 
        self.status   = status
        self.origin   = dt.now().strftime('%Y-%m-%d')
        self.due      = due

def SaveDf():
    global df
    df.to_json(df_filename)

def GetPending():
    print("Hello, Gunnar.")
    print("Here are your tasks for today:")
    global df
    tasks = df[ (df['status'] != 'done') ]
    if tasks.size == 0:
        print('Congratulations - You have no pending tasks!')
    else:
        print(tasks)

def RemoveTask(id):
    id = int(id)
    global df
    df.loc[int(id), 'end'] = dt.now().strftime('%Y-%m-%d')
    df.loc[int(id), 'status'] = 'removed'
    df.to_json(df_filename)
    print('Task Removed: ')
    print(df.loc[id])

def MarkTaskAsDone(id):
    id = int(id)
    global df
    df.loc[int(id), 'end'] = dt.now().strftime('%Y-%m-%d')
    df.loc[int(id), 'status'] = 'done'
    df.to_json(df_filename)
    print('Task Done: ')
    print(df.loc[id])

def MarkTaskAsUndone(id):
    id = int(id)
    global df
    df.loc[int(id), 'end'] = 'NaN' 
    df.loc[int(id), 'status'] = 'todo'
    df.to_json(df_filename)
    print('Task Done: ')
    print(df.loc[id])

def RemoveTask(id):
    id = int(id)
    global df
    df = df.drop(id)
    df.to_json(df_filename)

def Main():
    global df
    parser = argparse.ArgumentParser(description="I'm Revna - your personal, get-shit-done assistant.")
    parser.add_argument("-a", "--add",     type=str, help="Add an item to the todo list")
    parser.add_argument("-A", "--all",     help="List all tasks", action='store_true')
    parser.add_argument("-d", "--doing",   type=str, help="Mark task as doing")
    parser.add_argument("-D", "--done",    type=str, help="Mark task as done")
    parser.add_argument("-s", "--status",  type=str, help="The status of the task ( todo | doing | done )")
    parser.add_argument("-l", "--list",    action='store_true', help="List all pending tasks.")
    parser.add_argument("-g", "--go",      action='store_true', help="Revna, let's go!")
    parser.add_argument("-r", "--remove",  type=str, help="Remove a task")
    parser.add_argument("--due",           type=str, help="Add a due date to an item")
    parser.add_argument("--debug",         action='store_true', help="Start debugging Revna.")
    parser.add_argument("--clean",         action='store_true', help="Clean out all removed tickets.")
    args = parser.parse_args()

    if args.debug:
        import pdb; pdb.set_trace()

    elif args.list:
        print(df[ df['status'] != 'done'])

    elif args.all:
        print(df)

    elif args.go:
        GetPending()
    
    # READ/WRITE commands below.
    if args.add:
        CreateTodo(args.add)

    elif args.remove:
        # import pdb; pdb.set_trace()
        print('Removing Task: ', args.remove)
        RemoveTask(args.remove)

    elif args.done:
        MarkTaskAsDone(args.done)

    elif args.undone:
        MarkTaskAsUndone(args.undone)

    elif args.remove:
        RemoveTask(args.remove)

    else:
        print("Here's what you have to do today...\n")
        GetPending()


if __name__ == '__main__':
    Main()