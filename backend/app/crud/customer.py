from backend.app.models import Customer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.security.password import get_hashed_password


async def register_customer(db : AsyncSession, 
                            cus_f_name : str,
                            cus_l_name : str, 
                            cus_phone : str, 
                            cus_email : str,
                            cus_plain_password : str) -> Customer | None:
    
    new_hashed_password = get_hashed_password(cus_plain_password)
    new_cus = Customer(cus_email = cus_email, 
                       cus_f_name = cus_f_name, 
                       cus_l_name = cus_l_name,  
                       cus_phone = cus_phone, 
                       cus_hashed_password = new_hashed_password)
    
    db.add(new_cus)
    await db.commit()
    await db.refresh(new_cus)
    return new_cus


async def search_cus_by_email(db : AsyncSession, 
                              cus_email : str) -> Customer | None:
    query = select(Customer).where(Customer.cus_email == cus_email)

    result = await db.execute(query)
    return result.scalars().first()




