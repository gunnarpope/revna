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

class Todo():
    def __init__(self, task, project=None, status='todo',  due=None, level='low', category=None):
        self.category = category 
        self.task     = task
        self.level    = level 
        self.status   = status
        self.origin   = dt.isoformat(dt.now())
        self.due      = due

def GetPending():
    print(df[ df['status'] != 'done'])

REVNA_ROOT = os.getenv('REVNA_ROOT')
filename = REVNA_ROOT + 'todo/list.json'

df_filename = REVNA_ROOT + 'todo/todo.json'
df = pd.read_json(df_filename)
df.head()

parser = argparse.ArgumentParser(description="I'm Revna, your personal assistant for getting shit done.")
parser.add_argument("-t", "--todo",     type=str, help="Add an item to the todo list")
parser.add_argument("-d", "--due",      type=str, help="Add a due date to an item")
parser.add_argument("-s", "--status",   type=str, help="The status of the task ( todo | doing | done )")
parser.add_argument("-i", "--importance",    type=str, help="The importance level of the task ( low | med | high )")
parser.add_argument("-c", "--category", type=str, help="The category of the task.")
parser.add_argument("-l", "--list",     type=str, help="List all pending tasks.")
parser.add_argument("-g", "--go",       type=str, help="Revna, let's go!")

args = parser.parse_args()

if args.todo:
    print('Todo: ', args.todo)

    task = Todo(task=args.todo, level=args.importance, status=args.status, due=args.due)

    df_new = pd.DataFrame(task.__dict__, index=[1])
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_json(df_filename )

elif args.list:
    df[ df['status'] != 'done'].head()

elif args.go:
    print("Hello, Gunnar.")
    print("Here are your tasks for today:")
    GetPending()


