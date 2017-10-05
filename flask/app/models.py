from app import db

""" 
A user is someone who is a customer of the tv provider and has an account 
a user has the following properties:

    Attributes:
        UserID: An integer number representing the user.
        Gender: A character representing the users gender
        Age: An Integer number representing the users age
        Occupation: An Integer number corresponding to a profession
        Zipcode: An integer number representing user home location        
"""
class User(db.Model):
    UserID = db.Column(db.Integer, unique=True, primary_key=True)
    #Gender = db.Column(db.String(1))
    #Age = db.Column(db.Integer)
    #Occupation = db.Column(db.Integer)
    #Zipcode = db.Column(db.Integer)


class Movie(db.Model):
    MovieID= db.Column(db.Integer, unique = True, primary_key=True)
    Title = db.Column(db.String(255))
    Genre = db.Column(db.String(255))

class topMovies(db.Model):
    topMovieID = db.Column(db.Integer, unique = True, primary_key = True)
    Title = db.Column(db.String(255))
    Genre = db.Column(db.String(255))