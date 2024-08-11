from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.backend.db import Base
from app.models import *
from app.models.user import User


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    stock = Column(Integer)
    supplier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    rating = Column(Float)
    is_active = Column(Boolean, default=True)

    category = relationship("Category", back_populates="products")


from sqlalchemy.schema import CreateTable
# print(CreateTable(Product.__table__))
