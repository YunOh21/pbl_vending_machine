from sqlalchemy import *
from sqlalchemy.orm import *

Base = declarative_base()

class Product(Base):
    __tablename__ = 'Product'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    company_name = Column(String, nullable=False)
    kcal = Column(Integer)
    caffeine = Column(Integer)
    carbon_acid = Column(Boolean)
    sugar = Column(Integer)
    text_info = Column(String)
    image_path = Column(String, nullable=False)
    
    
class Order(Base):
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('Product.id'), nullable=False)
    order_at = Column(TIMESTAMP)
    payment_type = Column(CHAR(4))
    cash_amount = Column(INTEGER)
    card_info = Column(String)
    cash_change = Column(INTEGER)
    
    
class Receipt(Base):
    __tablename__ = 'Receipt'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('Order.id'), nullable=False)