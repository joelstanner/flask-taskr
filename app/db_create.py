#db_create.py

import sqlite3
from config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()
    c.execute("""CREATE TABLE ftasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL,
                status INTEGER NOT NULL)""")
    
    #insert dummy data
    c.execute('INSERT INTO ftasks (name, due_date, priority, status) VALUES ("Finish this tutorial", "06/20/2014", 10, 1)')
    c.execute('INSERT INTO ftasks (name, due_date, priority, status) VALUES ("Finish Real Python Course 2", "06/21/2014", 10, 1)')
    
    