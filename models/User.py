from database.db import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(Base, UserMixin):
    __tablename__ = 'User'
    id = Column(String, primary_key=True)
    name = Column(String(120))
    password = Column(String(300))
    reviews = relationship("Review", primaryjoin="User.id==Review.user_id")

    def __repr__(self):
        return "<User:" + self.id + " " + self.name + ">"

