from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base
from app.models import *
from app.models.user import User
import datetime

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    rating_id = Column(Integer, ForeignKey('rating.id'))
    comment = Column(String)
    comment_date = Column(datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S"))
    is_active = Column(Boolean, default=True)


# from sqlalchemy.schema import CreateTable
# print(CreateTable(Reviews.__table__))