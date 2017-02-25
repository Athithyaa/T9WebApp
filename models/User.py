from database.db import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'Users'

    id = Column(String, primary_key=True)
    name = Column(String(120))
    reviews = relationship("Review")

    def __repr__(self):
        return "<User:" + self.id + " " + self.name + ">"

