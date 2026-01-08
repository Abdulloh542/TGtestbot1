from sqlalchemy import select

from db.models import User


CITY_FEES = {
    "Toshkent": 15000,
    "Samarqand": 25000,
    "Buxoro": 25000,
    "Boshqa": 25000,
}


async def get_or_create_user(session, user_id: int) -> User:
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user:
        return user
    user = User(id=user_id)
    session.add(user)
    await session.commit()
    return user


async def update_user(session, user_id: int, **kwargs) -> User:
    user = await get_or_create_user(session, user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    await session.commit()
    return user


def delivery_fee_for(user: User, delivery_type: str) -> int:
    if delivery_type == "Olib ketish":
        return 0
    return CITY_FEES.get(user.city, 25000)
