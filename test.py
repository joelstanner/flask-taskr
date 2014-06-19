#test.py

import os
import unittest

from app import app, db
from app.models import User
from config import basedir

TEST_DB = 'test.db'

class Users(unittest.TestCase):
    
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
        
    #Each test should start with 'test'
    def test_user_setup(self):
        new_user = User("testuser","testuser@testuser.org","testuser01")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "testuser"
        
        
        
if __name__ == '__main__':
    unittest.main()