
from watson_developer_cloud import AlchemyLanguageV1
import json
ALCHEMY_API_KEY = '07551e54797d7b593f3595653a7cad5b1803d3a6'
alchemy_language = AlchemyLanguageV1(api_key='07551e54797d7b593f3595653a7cad5b1803d3a6')

sentiment = alchemy_language.sentiment(text='Hello, you suck dude!')


print sentiment['docSentiment']['type']
