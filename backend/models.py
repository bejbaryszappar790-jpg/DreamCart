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


class Product(Base):
    __tablename__ = "Product"

    product_id = Column(Integer, primary_key= True, index = True)
    saleman_id = Column(Integer, ForeignKey("Saleman.saleman_id"), nullable = False, index = True)
    product_name = Column(String, nullable = False)
    product_image_url = Column(String, nullable = False)
    product_sex = Column(String, nullable = False)


class Attribute(Base):
    __tablename__ = "Attribute"

    attribute_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("Product.product_id"), index=True)
    attribute_type = Column(String, nullable = False)
    attribute_brand = Column(String, nullable = False)
    attribute_value = Column(String, nullable = False)
    


