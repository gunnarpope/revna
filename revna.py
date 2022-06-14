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
    def __init__(self, task, project=None, status='undone',  due=None, level='low', category=None):
        self.category = category 
        self.task     = task
        self.level    = level 
        self.status   = status
        self.origin   = dt.isoformat(dt.now())
        self.due      = due


REVNA_ROOT = os.getenv('REVNA_ROOT')
filename = REVNA_ROOT + 'todo/list.json'

with open(filename, 'rb') as f:
    tasks = dict(json.load(f))

df_filename = REVNA_ROOT + 'todo/todo.json'
df = pd.read_json(df_filename)
df.head()

parser = argparse.ArgumentParser(description="I'm Revna, your personal assistant for getting shit done.")
parser.add_argument("-t", type=str, help="Add an item to the todo list")
parser.add_argument("-d", type=str, help="Add a due date to an item")
args = parser.parse_args()

print(args)
print(tasks)
print('All tasks: ', tasks['todo'])

if args.t:
    print('Todo: ', args.t)
    task = Todo(task=args.t)
    df_new = pd.DataFrame(task.__dict__, index=[1])
    df = pd.concat([df, df_new], ignore_index=True)
    df.to_json(df_filename )
if args.d:
    print('Due date: ', args.due)


print(df.head())

