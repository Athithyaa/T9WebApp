from flask import Flask, render_template, request, redirect, session
from datetime import timedelta
import uuid
from database.db import db_session, init_db
from models.Company import Company
from models.User import User
from models.Analytics import Analytics
from models.Review import Review
from forms import *
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import AlchemyLanguageV1

from ma_schema.AnalyticsSchema import AnalyticsSchema
from ma_schema.UserSchema import UserSchema
from ma_schema import CompanySchema
from ma_schema.ReviewSchema import ReviewSchema

import uuid
from models.Analytics import Analytics

WATSON_USERNAME = '1be2c698-56e7-47d4-9944-6e4d81c9b07d',
WATSON_PASSWORD = 'sPr4XOsPtNSX'
ALCHEMY_API_KEY = '07551e54797d7b593f3595653a7cad5b1803d3a6'
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


@app.route('/getreviews', methods=['GET'])
def getreviews():
    rSchema = ReviewSchema()
    return rSchema.dumps(Review.query.all()).data


@app.route('/postreview', methods=['GET', 'POST'])
def postreview():
    return render_template('pages/placeholder.post.html', form=PostReviewForm())


@app.route('/analytics')
def analytics():

    aSchema = AnalyticsSchema()
    cSchema = CompanySchema()
    #sentJson = reqData['review']

    content = "Facebook, you suck!"
    company_name = "twitter"

    if getCompany(company_name) == "None":
        cJson = constructCompany(company_name)
        com = cSchema.load(cJson, session=db_session).data
        id = com['id']
        db_session.add(com)
        db_session.commit()
        review_count = 1
        sentJson = constructNewAnalytics(id, content)
    else:
        com = getReviewCountForCompany(company_name)
        id = com['id']
        count =com['r_cnt']

        existing_ana = getExistingAnalyticsForCompany(id)
        sentJson = constructRunningAnalytics(existing_ana, count, content)


    #print sentJson
    ana = aSchema.load(sentJson, session=db_session).data
    db_session.merge(ana)
    db_session.commit()

    return render_template('pages/placeholder.home.html')


def getExistingAnalyticsForCompany(company_id):
    aSchema = AnalyticsSchema()
    ana = Analytics.query.filter_by(id=company_id).first()
    aJson = aSchema.dump(obj=ana).data
    return aJson

def getCompany(company_name):
    cSchema = CompanySchema()
    comp = Company.query.filter_by(name=company_name).first()
    if comp:
        cJson = cSchema.dump(obj=comp).data
        return cJson
    else:
        return "NotFound"

def constructRunningAnalytics(existing_ana, current_review_count, content):

    sentJson = {}


    tone_analyzer = ToneAnalyzerV3(
        username='1be2c698-56e7-47d4-9944-6e4d81c9b07d',
        password=WATSON_PASSWORD,
        version='2016-05-19')

    alchemy_language = AlchemyLanguageV1(api_key='07551e54797d7b593f3595653a7cad5b1803d3a6')
    sentiment = alchemy_language.sentiment(text=content)

    sentJson['sentiment_score'] = computeRunningAverage( existing_ana['sentiment_score'],sentiment['docSentiment']['score'], current_review_count)
    if sentJson['sentiment_score'] > 0:
        sentJson['sentiment_type'] = "positive"
    else:
        sentJson['sentiment_type'] = "negative"


    sentimentData = tone_analyzer.tone(text=content)

    sentJson['anger'] = computeRunningAverage(existing_ana['anger'],sentimentData["document_tone"]["tone_categories"][0]["tones"][0]["score"], current_review_count)
    sentJson['disgust'] = computeRunningAverage(existing_ana['disgust'],sentimentData["document_tone"]["tone_categories"][0]["tones"][1]["score"], current_review_count)
    sentJson['fear'] = computeRunningAverage(existing_ana['fear'],sentimentData["document_tone"]["tone_categories"][0]["tones"][2]["score"], current_review_count)
    sentJson['joy'] = computeRunningAverage(existing_ana['joy'],sentimentData["document_tone"]["tone_categories"][0]["tones"][1]["score"], current_review_count)
    sentJson['sadness'] = computeRunningAverage(existing_ana['sadness'],sentimentData["document_tone"]["tone_categories"][0]["tones"][1]["score"], current_review_count)

    sentJson['openness'] = computeRunningAverage(existing_ana['openness'], sentimentData["document_tone"]["tone_categories"][2]["tones"][0]["score"], current_review_count)
    sentJson['conscientiousness'] = computeRunningAverage(existing_ana['openness'], sentimentData["document_tone"]["tone_categories"][2]["tones"][1]["score"], current_review_count)
    sentJson['extraversion'] = computeRunningAverage(existing_ana['openness'], sentimentData["document_tone"]["tone_categories"][2]["tones"][2]["score"], current_review_count)
    sentJson['aggreablesness'] = computeRunningAverage(existing_ana['openness'], sentimentData["document_tone"]["tone_categories"][2]["tones"][3]["score"], current_review_count)
    sentJson['neuroticism'] = computeRunningAverage(existing_ana['openness'], sentimentData["document_tone"]["tone_categories"][2]["tones"][0]["score"], current_review_count)

    return sentJson


def computeRunningAverage(old_average, curr_average , count):
    new_avg = float((old_average * count + curr_average)/(count + 1))
    return new_avg

def constructNewAnalytics(id, content):

    sentJson = {}


    tone_analyzer = ToneAnalyzerV3(
        username='1be2c698-56e7-47d4-9944-6e4d81c9b07d',
        password=WATSON_PASSWORD,
        version='2016-05-19')

    alchemy_language = AlchemyLanguageV1(api_key='07551e54797d7b593f3595653a7cad5b1803d3a6')
    sentiment = alchemy_language.sentiment(text=content)

    sentJson['id'] = str(uuid.uuid1())
    sentJson['company_id'] = id
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
    return sentJson

def getReviewCountForCompany(company_name):
    cSchema = CompanySchema()
    comp = Company.query.filter_by(name=company_name).first()
    cJson = cSchema.dump(obj=comp).data
    return cJson

def constructCompany(company_name):
    compJson = {}
    compJson[u'id'] = str(uuid.uuid1())
    compJson['name'] = company_name
    compJson['r_cnt'] = 1
    return compJson

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
    db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if __name__ == "__main__":
    init_db()
    app.debug = True
    app.run()
