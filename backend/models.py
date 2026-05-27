from backend.database import Base
from sqlalchemy import(
    Column,
    Boolean,
    Integer,
    String,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    Numeric
)
from decimal import Decimal
from sqlalchemy.sql import func


class Customer(Base):
    __tablename__ = "Customer"

    cus_id = Column(Integer, primary_key= True, index= True)
    cus_f_name = Column(String, nullable = False)
    cus_l_name = Column(String, nullable = False)
    cus_phone = Column(String, nullable = False)
    cus_email = Column(String, nullable = False, unique = True)
    cus_hashed_password = Column(String, nullable = False)


class Saleman(Base):
    __tablename__ = "Saleman"

    saleman_id = Column(Integer, primary_key=True, index = True)
    saleman_f_name = Column(String, nullable = False)
    saleman_l_name = Column(String, nullable = False)
    sale_phone = Column(String, nullable = False)
    sale_email = Column(String, nullable = False, unique = True)
    sale_hashed_password = Column(String, nullable = False)
    sale_IP_number = Column(String, nullable = False)


class Admin(Base):
    __tablename__ = "Admin"
    
    admin_id = Column(Integer, primary_key = True, index = True)
    admin_name = Column(String, nullable = False)
    

class Category(Base):
    __tablename__ = "Category"
    category_id = Column(Integer, primary_key = True, index = True)
    category_name = Column(String, nullable = False)
    

class Parent_Product(Base):
    __tablename__ = "Parent_Product"

    parent_id = Column(Integer, primary_key = True, index = True)
    category_id = Column(Integer, ForeignKey("Category.category_id"), nullable = False, index = True)
    parent_name = Column(String, nullable = False)
    parent_sex = Column(String, nullable = False)
    parent_community = Column(String, nullable = False)

class Product_Description(Base):
    des_id = Column(Integer, primary_key = True, index = True)
    Catego
class Child_Product(Base):
    __tablename__ = "Child_Product"

    child_id = Column(Integer, primary_key = True, index = True)
     
class Stock(Base):
    __tablename__ = "Product_Variant_Stock"

    stock_id = Column(Integer, primary_key = True, index = True)
    certain_id = Column(Integer, ForeignKey("Certain_Product.certain_id"), index = True)
    stock_quantity = Column(Integer, nullable = False)


class Cart_Item(Base):
    __tablename__ = "Cart"
    cart_id = Column(Integer, primary_key=True, index = True)
    certain_id = Column(Integer, ForeignKey("Certain_Product.certain_id"), index = True)
    cus_id = Column(Integer, ForeignKey("Customer.cus_id"), index = True)


class Order(Base):
    __tablename__ = "Order"
    order_id = Column(Integer, primary_key=True, index = True)
    cus_id = Column(Integer, ForeignKey("Customer.cus_id"), index = True)
    purchase_time = Column(DateTime(timezone = True), server_default = func.now())
    total_amount = Column(Numeric(10, 2))
    payment_status = Column(String, default= "pending")

class Order_Item(Base):
    __tablename__ = "Order_Item"
    order_item_id = Column(Integer, primary_key = True, index = True)
    order_id = Column(Integer, ForeignKey("Order.order_id"), index = True)
    certain_id = Column(Integer, ForeignKey("Certain_Product.certain_id"), index = True)
    price_at_purchase = Column(Numeric(10, 2), nullable = False)


    

    