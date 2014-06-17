#db_create.py

from views import db
from models import FTasks
from datetime import date

#create the db and the tables
db.create_all()

#insert dummy data
#db.session.add(FTasks("Finish this tutorial", date(2014, 3, 13), 10, 1))
#db.session.add(FTasks("Finish real python", date(2014, 3, 13), 10, 1))

#commit to db
db.session.commit()