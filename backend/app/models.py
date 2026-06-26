from enum import Enum
from backend.app.database import Base
from sqlalchemy import(
    String,
    ForeignKey,
    DateTime,
    Numeric,
    UniqueConstraint
)
from decimal import Decimal
from sqlalchemy.sql import func
from sqlalchemy import Enum as SAENUM
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class User(Base):
    __tablename__ = "User"

    
    user_id : Mapped[int] = mapped_column(primary_key = True, index = True)
    user_f_name : Mapped[str] = mapped_column(String(30), nullable = False)
    user_l_name : Mapped[str] = mapped_column(String(30), nullable = False)
    user_phone : Mapped[str] = mapped_column(String(50), nullable = False)
    user_email : Mapped[str] = mapped_column(String(50), unique = True, nullable = False)
    user_hashed_password : Mapped[str] = mapped_column(String(70), nullable = False)
    user_role : Mapped[str] = mapped_column(String(20), nullable = False)



class Salesman_Data(Base):
    __tablename__ = "Salesman_Data"

    sale_id : Mapped[int] = mapped_column(primary_key = True, index = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("User.user_id"), index = True, nullable = False)
    sale_iin : Mapped[str] = mapped_column(String(20), index = True, nullable = False)
    sale_biin : Mapped[str] = mapped_column(String(20), index = True, nullable = False)
    


class Admin(Base):
    __tablename__ = "Admin"
    

    admin_id : Mapped[int] = mapped_column(primary_key = True, index = True)
    admin_name : Mapped[str] = mapped_column(String(30), nullable = False)
    
    

class Category(Base):
    __tablename__ = "Category"
    
    category_id : Mapped[int] = mapped_column(primary_key = True, index = True)
    category_name : Mapped[str] = mapped_column(String(30), nullable = False) 
    
    

class Parent_Product(Base):
    __tablename__ = "Parent_Product"


    parent_id : Mapped[int] = mapped_column(primary_key = True, index = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("User.user_id"), index = True, nullable = False)
    category_id : Mapped[int] = mapped_column(ForeignKey("Category.category_id"), index = True, nullable = False)
    parent_name : Mapped[str] = mapped_column(String(50), nullable = False)
    parent_sex : Mapped[str] = mapped_column(String(10), nullable = False)
    parent_community : Mapped[str] = mapped_column(String(20), nullable = False)


class Variant(Base):
    __tablename__ = "Variant"

    var_id : Mapped[int] = mapped_column(primary_key = True, index = True)
    parent_id : Mapped[int] = mapped_column(ForeignKey("Parent_Product.parent_id"), index = True, nullable = False)
    user_id : Mapped[int] = mapped_column(ForeignKey("User.user_id"), index = True, nullable = False)
    var_order : Mapped[int] = mapped_column(nullable = False, index = True)
    var_image_url : Mapped[str] = mapped_column(String(40), nullable = False)
    var_price : Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable = False)

    __table_args__=(
        UniqueConstraint(
            "user_id", "parent_id", "var_order", name = "description_parent_salesman"
        ),
    )

class Attribute(Base):
    __tablename__ = "Attribute"


    att_id : Mapped[int] = mapped_column(primary_key = True, index = True)
    var_id : Mapped[int] = mapped_column(ForeignKey("Variant.var_id"), index = True, nullable = False)
    att_name : Mapped[str] = mapped_column(String(40), nullable = False)
    att_value : Mapped[str] = mapped_column(String(40), nullable = False)
    
    

class Stock(Base):
    __tablename__ = "Stock"


    stock_id : Mapped[int] = mapped_column(primary_key = True, index = True)
    var_id : Mapped[int] = mapped_column(ForeignKey("Variant.var_id"), nullable = False, index = True)
    stock_quantity : Mapped[int] = mapped_column(nullable = False)


class Cart_Item(Base):
    __tablename__ = "Cart"


    cart_id : Mapped[int] = mapped_column(primary_key = True, index = True)
    var_id : Mapped[int] = mapped_column(ForeignKey("Variant.var_id"), nullable = False, index = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("User.user_id"), nullable = False, index = True)
    cart_quantity : Mapped[int] = mapped_column(nullable = False)
    

class Payment_Status(str, Enum):
    PENDING = "Pending"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"

class Orders(Base):
    __tablename__ = "Order"

    order_id : Mapped[int] = mapped_column(primary_key = True, index = True)
    user_id : Mapped[int] = mapped_column(ForeignKey("User.user_id"), nullable = False, index = True)
    purchase_time : Mapped[datetime] = mapped_column(DateTime(timezone = True), server_default = func.now())
    total_amount : Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable = False)
    payment_status : Mapped[Payment_Status] = mapped_column(
        SAENUM(Payment_Status),
        default = Payment_Status.PENDING,
        nullable = False
    )
    

class Order_Item(Base):
    __tablename__ = "Order_Item"
    order_item_id : Mapped[int] = mapped_column(primary_key = True, index = True)
    order_id : Mapped[int] = mapped_column(ForeignKey("Order.order_id"), nullable = False, index = True)
    cart_id : Mapped[int | None] = mapped_column(ForeignKey("Cart.cart_id", ondelete = "SET NULL"), nullable = True, index = True)
    var_id : Mapped[int] = mapped_column(ForeignKey("Variant.var_id"), nullable = False, index = True)
    price_at_purchase : Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable = False)
    order_quantity : Mapped[int] = mapped_column(nullable = False)
    