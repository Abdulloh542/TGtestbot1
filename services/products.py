from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models import Category, Product


async def get_categories(session):
    result = await session.execute(select(Category).order_by(Category.id))
    return result.scalars().all()


async def get_products_by_category(session, category_id: int):
    result = await session.execute(
        select(Product).where(Product.category_id == category_id).order_by(Product.id)
    )
    return result.scalars().all()


async def get_product(session, product_id: int) -> Product | None:
    result = await session.execute(
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.category))
    )
    return result.scalars().first()
