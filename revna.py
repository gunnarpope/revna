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

def CreateTodo(args):
    global df
    task = Todo(task=args.add, status='todo', due=args.due)

    df_new = pd.DataFrame(task.__dict__, index=[1])
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_json(df_filename)
    print(df)

class Todo():
    def __init__(self, task, status='todo',  due=None, group=None):
        self.task     = task
        self.status   = status
        self.start    = dt.now().strftime('%Y-%m-%d')
        self.due      = due
        self.group    = group  
        self.end      = None 

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
    df.loc[id, 'end'] = dt.now().strftime('%Y-%m-%d')
    df.loc[id, 'status'] = 'done'
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

def Edit(idx=None, task=None, group=None, status=None, due=None, end=None):

    if idx:

        if task:
            df.loc[idx, 'task'] = task
        if status:
            df.loc[idx, 'status'] = status 
        if group:
            df.loc[idx, 'group'] = group 
        if due:
            df.loc[idx, 'due'] = due 
        if end:
            df.loc[idx, 'end'] = end 

    df.to_json(df_filename)

def Main():
    global df
    parser = argparse.ArgumentParser(description="I'm Revna - your personal, get-shit-done assistant.")
    parser.add_argument("-a", "--add",     type=str, help="Add an item to the todo list")
    parser.add_argument("-A", "--all",     help="List all tasks", action='store_true')
    parser.add_argument("-d", "--doing",   type=str, help="Mark task as doing")
    parser.add_argument("-D", "--done",    type=str, help="Mark task as done")
    parser.add_argument("-e", "--edit",    type=str, help="Edit a row, by index number. $revna -e N --group groupname")
    parser.add_argument("-s", "--status",  type=str, help="The status of the task ( todo | doing | done )")
    parser.add_argument("-l", "--list",    action='store_true', help="List all pending tasks.")
    parser.add_argument("--group",   type=str, help=" The name of the group to edit.")
    parser.add_argument("--task",   type=str, help=" The name of the task to edit.")
    parser.add_argument("-r", "--remove",  type=str, help="Remove a task")
    parser.add_argument("--due",           type=str, help="Add a due date to an item")
    parser.add_argument("--end",           type=str, help="Add a due date to an item")
    parser.add_argument("--debug",         action='store_true', help="Start debugging Revna.")
    parser.add_argument("--clean",         action='store_true', help="Clean out all removed tickets.")
    args = parser.parse_args()

    if args.debug:
        import pdb; pdb.set_trace()
    
    if args.edit:
        idx = int(args.edit)
        Edit(idx=idx, task=args.task, group=args.group, status=args.status, due=args.due, end=args.end)
        GetPending()
        

    elif args.list:
        print(df[ df['status'] != 'done'])

    elif args.all:
        print(df)

    
    # READ/WRITE commands below.
    elif args.add:
        CreateTodo(args)

    elif args.remove:

        print('Removing Task: ', args.remove)
        RemoveTask(args.remove)

    elif args.done:
        MarkTaskAsDone(args.done)

    else:
        GetPending()

    


if __name__ == '__main__':
    Main()
