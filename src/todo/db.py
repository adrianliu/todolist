import os
import json
import sqlite3
from models import Task

# From: https://goo.gl/YzypOI
def singleton(cls):
  instances = {}
  def getinstance():
    if cls not in instances:
      instances[cls] = cls()
    return instances[cls]
  return getinstance

class DB(object):
  """
  DB driver for the Todo app - deals with writing entities
  to the DB and reading entities from the DB
  """

  def __init__(self):
    self.conn = sqlite3.connect("todo.db", check_same_thread=False)
    # TODO - Create all other tables here
    self.create_task_table()

  def create_task_table(self):
    """
    Create a Task table. Silently error-handles
    (try-except) because the table might already exist.
    """
    try:
      self.conn.execute("""
        CREATE TABLE task
        (ID TEXT PRIMARY KEY NOT NULL,
        NAME TEXT NOT NULL,
        DESCRIPTION TEXT NOT NULL,
        TAGS TEXT NOT NULL,
        DUE_DATE INT NOT NULL,
        CREATED_AT DATETIME DEFAULT (STRFTIME('%d-%m-%Y   %H:%M', 'NOW','localtime')));
      """)
    except Exception as e: print e

  def delete_task_table(self):
    # TODO - Implement this to delete a task table
    self.conn.execute("""
      DROP TABLE task;
      """)
    self.conn.commit()


  def create_task(self, task):
    """
    VALUES (task.id, task.name, task.description, task.tags, task.due_date);
    Insert a task to task table.
    """
    if not isinstance(task, Task):
      return
    self.conn.execute("""
      INSERT INTO task (ID,NAME,DESCRIPTION,TAGS,DUE_DATE)
      VALUES (?,?,?,?,?)""", (task.id, task.name, task.description, task.tags, task.due_date))
    self.conn.commit()

  def delete_task(self, task_id):
    """
    Delete the specific task from task table.
    """
    self.conn.execute("""
      DELETE from task where ID= (?)""",(task_id,))
    self.conn.commit()

  def delete_all_tasks(self):
    """
    Delete all tasks from task table.
    """
    self.conn.execute("""
      DELETE from task;
      """)
    self.conn.commit()

  def query_all_tasks(self):
    """
    Query tasks from Task table.
    """
    cursor = self.conn.execute("""
      SELECT * FROM task;
    """)

    tasks = []
    for row in cursor:
      id = row[0]
      name = row[1]
      description = row[2]
      tags = row[3]
      due_date = row[4]
      task = Task(name, description, tags, due_date, id)
      tasks.append(task.to_dict())
    return tasks


# Only <=1 instance of the DB driver
# exists within the app at all times
DB = singleton(DB)
