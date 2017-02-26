from database.db import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Company(Base):
    __tablename__ = 'Company'
    id = Column(String, primary_key=True)
    name = Column(String(100))
    r_cnt = Column(Integer)
    reviews = relationship("Review", primaryjoin="Company.id==Review.company_id")

    def __repr__(self):
        return "<Company:" + self.id + " " + self.name + ">"
