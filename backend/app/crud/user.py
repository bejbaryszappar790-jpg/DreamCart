from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.models import User, Salesman_Data
from backend.app.security.password import get_hashed_password


async def register_user(db : AsyncSession, 
                            user_f_name : str,
                            user_l_name : str, 
                            user_phone : str, 
                            user_email : str,
                            user_plain_password : str,
                            user_role : str,
                            sale_iin : str | None,
                            sale_biin : str | None
                            ) -> User | None:
    
    new_hashed_password = get_hashed_password(user_plain_password)
    new_user = User(user_email = user_email, 
                       user_f_name = user_f_name, 
                       user_l_name = user_l_name,  
                       user_phone = user_phone, 
                       user_hashed_password = new_hashed_password,
                       user_role = user_role
                       )
    
    if user_role == "salesman":
        if sale_biin is None or sale_iin is None:
            return None
        
        if not sale_biin.isdigit() or not sale_iin.isdigit():
            return None


    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    if user_role == "customer":
        return new_user
    
    elif user_role == "salesman":
        new_sale_data = Salesman_Data(
            user_id = new_user.user_id,
            sale_biin = sale_biin,
            sale_iin = sale_iin
        )
    
        db.add(new_sale_data)
        await db.commit()
    

    return new_user


async def search_user_by_email(db : AsyncSession, 
                              user_email : str) -> User | None:
    query = select(User).where(User.user_email == user_email)

    result = await db.execute(query)
    return result.scalars().first()


async def search_user_by_id(db : AsyncSession,
                            user_id : int) -> User | None:

    query = (
        select(User)
        .where(User.user_id == user_id)
    )

    result = await db.execute(query)
    return result.scalars().first()




