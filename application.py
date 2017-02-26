from flask import Flask, render_template, request, redirect
import uuid
from database.db import db_session, init_db
from flask_login import LoginManager,login_required,login_user,logout_user
from models.Company import Company
from models.User import User
from models.Review import Review
from ma_schema.UserSchema import UserSchema
from forms import *
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
app.secret_key = 's3cr3t'


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = {}
        uSchema = UserSchema()
        username = request.form['name']
        password = request.form['password']
        u['id'] = ""
        u['name'] = username
        u['password'] = password
        user = uSchema.load(u, session=db_session).data
        login_user(user)
        return redirect(request.args.get("next"))
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
        u['id'] = str(uuid.uuid4())
        u['name'] = username
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
