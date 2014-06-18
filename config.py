#config.py

import os

#grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
CSRF_ENABLED = True
SECRET_KEY = 'g%GK9L47Nc(F2C&8Tvj+yrA'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# The database URI
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH