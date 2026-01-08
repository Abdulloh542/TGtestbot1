from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models import CartItem, Order, OrderItem, Product


async def create_order(
    session,
    user_id: int,
    contact: str,
    address: str,
    delivery: str,
    payment_method: str,
    delivery_fee: int,
    discount_amount: int,
    promo_code: str | None,
):
    cart_items = await session.execute(
        select(CartItem)
        .where(CartItem.user_id == user_id)
        .options(selectinload(CartItem.product))
    )
    items = cart_items.scalars().all()
    if not items:
        return None

    subtotal = sum(item.quantity * item.product.price for item in items)
    total = max(subtotal + delivery_fee - discount_amount, 0)
    order = Order(
        user_id=user_id,
        contact=contact,
        address=address,
        delivery_type=delivery,
        payment_method=payment_method,
        delivery_fee=delivery_fee,
        discount_amount=discount_amount,
        promo_code=promo_code,
        total_amount=total,
    )
    session.add(order)
    await session.flush()

    for item in items:
        session.add(
            OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price,
            )
        )

    for item in items:
        await session.delete(item)

    await session.commit()
    return order


async def get_user_orders(session, user_id: int, limit: int = 10):
    result = await session.execute(
        select(Order)
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .limit(limit)
    )
    return result.scalars().all()


async def get_order_detail(session, order_id: int):
    result = await session.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
    )
    return result.scalars().first()


async def get_new_orders(session):
    result = await session.execute(
        select(Order)
        .where(Order.status == "NEW")
        .order_by(Order.created_at.desc())
        .limit(20)
    )
    return result.scalars().all()


async def update_order_status(session, order_id: int, status: str):
    result = await session.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        return None
    order.status = status
    await session.commit()
    return order
