from app import app
from flask import render_template, redirect, url_for, request
from data.user_data.user import user
from data.content.movie import movie
from machine_learning.prediction.svd_train_val import get_rating


@app.route('/')
def index():
    return render_template('loginView.html');

@app.route('/operatorView')
def operator_view():
    return render_template('operatorView.html');

@app.route('/userView')
def user_view():


    myUser = user(1, 'F', 1, 10, 48067);
    myMovie = movie(1, "Toy Story (1995)", "Animation|Children's|Comedy")



    rating = get_rating(myUser.getUserID(), myMovie.getMovieID());




    return render_template('userView.html', myUser=myUser, myMovie = myMovie, myRating = rating);

# route for handling the login page logic
@app.route('/loginView', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('operator_view'));
    return render_template('/loginView.html', error=error);

