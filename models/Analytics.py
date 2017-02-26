from database.db import Base
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Analytics(Base):
    __tablename__ = 'Analytics'
    id = Column(String, primary_key=True)
    company_id = Column(String(100), ForeignKey("Company.id"), nullable=False)

    sentiment_score = Column(Float)
    sentiment_type = Column(String(30))

    anger = Column(Float)
    disgust = Column(Float)
    fear  = Column(Float)
    joy = Column(Float)
    sadness = Column(Float)

    openness = Column(Float)
    conscientiousness = Column(Float)
    extraversion = Column(Float)
    neuroticism = Column(Float)
    aggreablesness = Column(Float)

    def __repr__(self):
        return "<id:" + str(self.id) + " " + "anger" + " " + str(self.anger) + ">"