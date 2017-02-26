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
import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import AlchemyLanguageV1
import requests
from ma_schema.AnalyticsSchema import AnalyticsSchema
from ma_schema.UserSchema import UserSchema

import uuid
from models.Analytics import Analytics

WATSON_USERNAME = '1be2c698-56e7-47d4-9944-6e4d81c9b07d',
WATSON_PASSWORD = 'sPr4XOsPtNSX'
ALCHEMY_API_KEY = '07551e54797d7b593f3595653a7cad5b1803d3a6'
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
    aSchema = AnalyticsSchema()
    over = Analytics.query.all()
    uSchema = UserSchema()
    print over
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/analytics')
def analytics():

    aSchema = AnalyticsSchema()
    #sentJson = reqData['review']

    content = "Facebook, you suck!"

    sentJson = {}

    tone_analyzer = ToneAnalyzerV3(
        username='1be2c698-56e7-47d4-9944-6e4d81c9b07d',
        password=WATSON_PASSWORD,
        version='2016-05-19')

    alchemy_language = AlchemyLanguageV1(api_key='07551e54797d7b593f3595653a7cad5b1803d3a6')
    sentiment = alchemy_language.sentiment(text=content)

    sentJson['id'] = str(uuid.uuid1())
    sentJson['sentiment_score'] = sentiment['docSentiment']['score']
    sentJson['sentiment_type'] = sentiment['docSentiment']['type']

    sentimentData = tone_analyzer.tone(text=content)

    sentJson['anger'] = sentimentData["document_tone"]["tone_categories"][0]["tones"][0]["score"]
    sentJson['disgust'] = sentimentData["document_tone"]["tone_categories"][0]["tones"][1]["score"]
    sentJson['fear'] = sentimentData["document_tone"]["tone_categories"][0]["tones"][2]["score"]
    sentJson['joy'] = sentimentData["document_tone"]["tone_categories"][0]["tones"][3]["score"]
    sentJson['sadness'] = sentimentData["document_tone"]["tone_categories"][0]["tones"][4]["score"]

    sentJson['openness'] = sentimentData["document_tone"]["tone_categories"][2]["tones"][0]["score"]
    sentJson['conscientiousness'] = sentimentData["document_tone"]["tone_categories"][2]["tones"][1]["score"]
    sentJson['extraversion'] = sentimentData["document_tone"]["tone_categories"][2]["tones"][2]["score"]
    sentJson['aggreablesness'] = sentimentData["document_tone"]["tone_categories"][2]["tones"][3]["score"]
    sentJson['neuroticism'] = sentimentData["document_tone"]["tone_categories"][2]["tones"][4]["score"]

    #print sentJson
    ana = aSchema.load(sentJson, session=db_session).data
    db_session.add(ana)
    db_session.commit()

    return render_template('pages/placeholder.home.html')


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
