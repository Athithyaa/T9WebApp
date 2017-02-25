from database.db import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Company(Base):
    __tablename__ = 'Companies'
    id = Column(String, primary_key=True)
    name = Column(String(100))
    r_cnt = Column(Integer)
    reviews = relationship("Company")

    def __repr__(self):
        return "<Company:" + self.id + " " + self.name + ">"
