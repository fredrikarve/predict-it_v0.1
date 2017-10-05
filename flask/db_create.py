#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
#from app import models

#Creating the database and adding some fake users.


import os.path
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

    #Adding fake users to the database.


    # u = models.User(UserID=1, Gender='m', Age=12, Occupation=15, Zipcode=4123)
    # db.session.add(u)
    # u = models.User(UserID=2, Gender='m', Age=20, Occupation=10, Zipcode=12345)
    # db.session.add(u)
    # u = models.User(UserID=3, Gender='f', Age=10, Occupation=12, Zipcode=12323)
    # db.session.add(u)
    # db.session.commit()

    #Querying to the db to see if the users were added.
    #all_users = models.User.query.all()

    #print('All the users:')
    #for i in all_users:
    #    print(i.Gender, i.Zipcode)
    #    print(' \n ')