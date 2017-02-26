from flask import Flask, render_template, request, redirect, session
from datetime import timedelta
import uuid
from database.db import db_session, init_db
from models.Company import Company
from models.User import User
from models.Review import Review
from ma_schema.UserSchema import UserSchema
from forms import *
import os

app = Flask(__name__)
app.secret_key = 's3cr3t'


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/post')
def post():
    return render_template('pages/placeholder.post.html',form=PostReviewForm())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        lgn = User.query.filter_by(email=email.lower()).first()
        if lgn.password == password:
            return render_template('pages/placeholder.home.html')
        else:
            return render_template('forms/login.html', form=form)
    else:
        form = LoginForm(request.form)
        return render_template('forms/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = {}
        uSchema = UserSchema()
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        u['id'] = str(uuid.uuid4())
        u['name'] = username
        u['email'] = email
        u['password'] = password
        user = uSchema.load(u, session=db_session).data
        db_session.add(user)
        db_session.commit()
        return render_template('pages/placeholder.home.html')
    else:
        form = RegisterForm(request.form)
        return render_template('forms/register.html', form=form)


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if __name__ == "__main__":
    init_db()
    app.debug = True
    app.run()
