# test_tasks.py


import os
import unittest

from app import app, db
from app.models import User, FTasks
from config import basedir

from datetime import datetime, date

TEST_DB = 'test.db'

class TasksTest(unittest.TestCase):
    
    #This is a special method that is executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        
    #This is a special method that is excuted after each test
    def tearDown(self):
        db.drop_all()
    
    
    # helper methods
    def login(self, username, password):
        return self.app.post('users/', data=dict(
            name=username,
            password=password), follow_redirects=True)
        
    def logout(self):
        return self.app.get('users/logout', follow_redirects=True)
    
    def register(self):
        return self.app.post('users/register/', data=dict(
            name='thisguy2',
            email = 'thisguy2@thisguy.com',
            password = 'password12345',
            confirm = 'password12345'
        ), follow_redirects=True)
        
    def create_user(self):
        new_user = User("thisguy", "thisguy@thisguy.com", "password12345")
        db.session.add(new_user)
        db.session.commit()
        
    def create_task(self):
        return self.app.post('tasks/add/', data =
                            dict(
                                name = 'Awesome stuff - do it',
                                due_date = '07/01/2014',
                                priority = '1',
                                posted_date = '06/21/2014',
                                status = '1'
                            ), follow_redirects=True)
    

    # views tests
    def test_users_can_add_tasks(self):
        self.create_user()
        self.login('thisguy','password12345')
        self.app.get('tasks/tasks/', follow_redirects=True)
        response = self.create_task()
        assert 'New entry was successfuly posted.  Thank you.' in response.data
        
    def test_users_can_complete_tasks(self):
        self.create_user()
        self.login('thisguy','password12345')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('tasks/complete/1/', follow_redirects=True)
        assert 'The task was marked as complete.' in response.data
        #print response.data
        
    def test_users_can_delete_tasks(self):
        self.create_user()
        self.login('thisguy','password12345')
        self.app.get('tasks/tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('tasks/delete/1/', follow_redirects=True)
        assert 'The task was deleted.' in response.data
        
    def test_users_cannot_add_tasks_when_error(self):
        self.create_user()
        self.login('thisguy','password12345')
        self.app.get('tasks/tasks/', follow_redirects=True)
        response = self.app.post('tasks/add/', data=dict(
            name = 'Kick some ass',
            due_date = '07/01/2014',
            priority = '1',
            posted_date = '',
            status = '1'
        ), follow_redirects=True)
        #print response.data
        assert 'Error in the Posted date (mm/dd/yyyy) field - This field is required.' in response.data
        
        
    # testing the models
    def test_users_can_add_tasks_model(self):
        self.create_user()
        self.login('thisguy','password12345')
        self.app.get('tasks/tasks/', follow_redirects=True)
        new_task = FTasks("Goto Space", date.today(),
                          "1", date.today(), "1", "1")
        db.session.add(new_task)
        db.session.commit()
        test = db.session.query(FTasks).all()
        for t in test:
            t.name
        assert t.name == "Goto Space"


if __name__ == '__main__':
    unittest.main()