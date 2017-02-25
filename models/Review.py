from sqlalchemy import ForeignKey
from database.db import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Review(Base):
    __tablename__ = 'Reviews'
    id = Column(String, primary_key=True)
    user_id = Column(String(100), ForeignKey("User.id"), nullable=False)
    company_id = Column(String(100), ForeignKey("Company.id"), nullable=False)
    content = Column(String(100))
    user = relationship("User", ForeignKey("User.id"))
    company = relationship("Company", ForeignKey("Company.id"))

    def __repr__(self):
        return "<Review:" + self.id + " " + self.content + ">"
