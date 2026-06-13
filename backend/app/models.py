from backend.app.database import Base
from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Numeric,
    UniqueConstraint
)
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key= True, index= True)
    user_f_name = Column(String, nullable = False)
    user_l_name = Column(String, nullable = False)
    user_phone = Column(String, nullable = False)
    user_email = Column(String, nullable = False, unique = True)
    user_hashed_password = Column(String, nullable = False)
    user_role = Column(String, nullable = False)


class Salesman_Data(Base):
    __tablename__ = "Salesman_Data"

    sale_id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey("User.user_id"), index = True, nullable = False)
    sale_iin = Column(Integer, index = True, nullable = False)
    sale_biin = Column(Integer, index = True, nullable = False)


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
    user_id = Column(Integer, ForeignKey("User.User_id"), index = True)
    category_id = Column(Integer, ForeignKey("Category.category_id"), nullable = False, index = True)
    parent_name = Column(String, nullable = False)
    parent_sex = Column(String, nullable = False)
    parent_community = Column(String, nullable = False)

class Variant(Base):
    __tablename__ = "Variant"
    var_id = Column(Integer, primary_key = True, index = True)
    parent_id = Column(Integer, ForeignKey("Parent_Product.parent_id"), nullable = False, index = True)
    user_id = Column(Integer, ForeignKey("User.user_id"), nullable = False, index = True)
    var_order = Column(Integer, nullable = False, index = True)
    var_image_url = Column(String, nullable = False)
    var_price = Column(Numeric(10, 2), nullable = False)

    __table_args__=(
        UniqueConstraint(
            "user_id", "parent_id", "var_order", name = "description_parent_salesman"
        )
    )

class Attribute(Base):
    __tablename__ = "Attribute"

    att_id = Column(Integer, primary_key = True, index = True)
    var_id = Column(Integer, ForeignKey("Variant.var_id"), nullable = False, index = True)
    att_name = Column(String, nullable = False)
    att_value = Column(String, nullable = False)
    
     
class Stock(Base):
    __tablename__ = "Stock"

    stock_id = Column(Integer, primary_key = True, index = True)
    var_id = Column(Integer, ForeignKey("Variant.var_id"), nullable = False, index = True)
    stock_quantity = Column(Integer, nullable = False)


class Cart_Item(Base):
    __tablename__ = "Cart"
    cart_id = Column(Integer, primary_key=True, index = True)
    var_id = Column(Integer, ForeignKey("Variant.var_id"), nullable = False, index = True)
    user_id = Column(Integer, ForeignKey("User.user_id"), index = True)


class Orders(Base):
    __tablename__ = "Order"
    order_id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey("User.user_id"), index = True)
    purchase_time = Column(DateTime(timezone = True), server_default = func.now())
    total_amount = Column(Numeric(10, 2))
    payment_status = Column(String, default= "pending")

class Order_Item(Base):
    __tablename__ = "Order_Item"
    order_item_id = Column(Integer, primary_key = True, index = True)
    order_id = Column(Integer, ForeignKey("Order.order_id"), index = True)
    var_id = Column(Integer, ForeignKey("Variant.var_id"), nullable = False, index = True)
    price_at_purchase = Column(Numeric(10, 2), nullable = False)
