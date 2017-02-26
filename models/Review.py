from sqlalchemy import ForeignKey
from database.db import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Review(Base):
    __tablename__ = 'Review'
    id = Column(String, primary_key=True)
    user_id = Column(String(100), ForeignKey("User.id"), nullable=False)
    company_id = Column(String(100), ForeignKey("Company.id"), nullable=False)
    content = Column(String(100))
    user = relationship("User", foreign_keys="Review.user_id")
    company = relationship("Company", foreign_keys="Review.company_id")
    date = Column(String(100))

    def __repr__(self):
        return "<Review:" + self.id + " " + self.content + ">"
