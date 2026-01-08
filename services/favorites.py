from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from db.models import Favorite


async def toggle_favorite(session, user_id: int, product_id: int) -> bool:
    result = await session.execute(
        select(Favorite).where(
            Favorite.user_id == user_id, Favorite.product_id == product_id
        )
    )
    existing = result.scalars().first()
    if existing:
        await session.delete(existing)
        await session.commit()
        return False
    favorite = Favorite(user_id=user_id, product_id=product_id)
    session.add(favorite)
    await session.commit()
    return True


async def is_favorite(session, user_id: int, product_id: int) -> bool:
    result = await session.execute(
        select(Favorite).where(
            Favorite.user_id == user_id, Favorite.product_id == product_id
        )
    )
    return result.scalars().first() is not None


async def list_favorites(session, user_id: int):
    result = await session.execute(
        select(Favorite)
        .where(Favorite.user_id == user_id)
        .options(selectinload(Favorite.product))
    )
    return result.scalars().all()


async def clear_favorites(session, user_id: int):
    await session.execute(delete(Favorite).where(Favorite.user_id == user_id))
    await session.commit()
