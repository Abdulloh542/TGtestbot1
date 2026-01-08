from sqlalchemy import delete, func, select
from sqlalchemy.orm import selectinload

from db.models import CartItem, Product


async def get_cart_items(session, user_id: int):
    result = await session.execute(
        select(CartItem)
        .where(CartItem.user_id == user_id)
        .options(selectinload(CartItem.product))
        .order_by(CartItem.id)
    )
    return result.scalars().all()


async def add_to_cart(session, user_id: int, product_id: int, quantity: int = 1):
    result = await session.execute(
        select(CartItem).where(
            CartItem.user_id == user_id, CartItem.product_id == product_id
        )
    )
    item = result.scalars().first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        session.add(item)
    await session.commit()
    return item


async def update_quantity(session, item_id: int, quantity: int):
    result = await session.execute(select(CartItem).where(CartItem.id == item_id))
    item = result.scalars().first()
    if not item:
        return None
    if quantity <= 0:
        await session.delete(item)
    else:
        item.quantity = quantity
    await session.commit()
    return item


async def remove_item(session, item_id: int):
    await session.execute(delete(CartItem).where(CartItem.id == item_id))
    await session.commit()


async def clear_cart(session, user_id: int):
    await session.execute(delete(CartItem).where(CartItem.user_id == user_id))
    await session.commit()


async def cart_total(session, user_id: int) -> int:
    result = await session.execute(
        select(func.coalesce(func.sum(CartItem.quantity * Product.price), 0))
        .select_from(CartItem)
        .join(Product, CartItem.product_id == Product.id)
        .where(CartItem.user_id == user_id)
    )
    return int(result.scalar_one())
