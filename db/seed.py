from sqlalchemy import select

from db.models import Category, Product


PLACEHOLDER_PHOTOS = [
    "https://placehold.co/600x400/png?text=Mahsulot+1",
    "https://placehold.co/600x400/png?text=Mahsulot+2",
    "https://placehold.co/600x400/png?text=Mahsulot+3",
    "https://placehold.co/600x400/png?text=Mahsulot+4",
    "https://placehold.co/600x400/png?text=Mahsulot+5",
]


async def seed_demo_data(session) -> None:
    existing = await session.execute(select(Category))
    if existing.scalars().first():
        return

    categories = [
        Category(name="Ichimliklar"),
        Category(name="Shirinliklar"),
        Category(name="Maishiy")
    ]
    session.add_all(categories)
    await session.flush()

    products = []
    for idx, category in enumerate(categories, start=1):
        for num in range(1, 6):
            products.append(
                Product(
                    category_id=category.id,
                    name=f"Mahsulot {idx}-{num}",
                    description=f"Mahsulot {idx}-{num} haqida qisqacha ma'lumot.",
                    price=10000 + num * 1500,
                    photo_url=PLACEHOLDER_PHOTOS[(num - 1) % len(PLACEHOLDER_PHOTOS)],
                )
            )
    session.add_all(products)
    await session.commit()
