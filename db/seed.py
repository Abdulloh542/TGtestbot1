from sqlalchemy import select

from db.models import Category, Product


CATEGORY_PRODUCTS = {
    "Ichimliklar": [
        {
            "name": "Limonad",
            "description": "Tabiiy limon sharbati bilan tayyorlangan sovuq ichimlik.",
            "price": 12000,
            "photo_url": "https://source.unsplash.com/featured/600x400?lemonade",
        },
        {
            "name": "Mojito (alkogolsiz)",
            "description": "Yalpiz va ohakli tetiklantiruvchi mojito.",
            "price": 18000,
            "photo_url": "https://source.unsplash.com/featured/600x400?mojito",
        },
        {
            "name": "Muzli choy",
            "description": "Tabiiy qora choy va limon bilan muzli ichimlik.",
            "price": 14000,
            "photo_url": "https://source.unsplash.com/featured/600x400?iced-tea",
        },
        {
            "name": "Apelsin fresh",
            "description": "Yangi siqilgan apelsin sharbati.",
            "price": 20000,
            "photo_url": "https://source.unsplash.com/featured/600x400?orange-juice",
        },
        {
            "name": "Olma fressh",
            "description": "Yangi siqilgan olma sharbati.",
            "price": 18000,
            "photo_url": "https://source.unsplash.com/featured/600x400?apple-juice",
        },
        {
            "name": "Anor sharbati",
            "description": "Vitaminlarga boy anor sharbati.",
            "price": 22000,
            "photo_url": "https://source.unsplash.com/featured/600x400?pomegranate-juice",
        },
        {
            "name": "Mineral suv",
            "description": "Gazli mineral suv, sovuq holatda.",
            "price": 8000,
            "photo_url": "https://source.unsplash.com/featured/600x400?mineral-water",
        },
        {
            "name": "Mevali smuzi",
            "description": "Rezavor mevalar asosida smuzi.",
            "price": 21000,
            "photo_url": "https://source.unsplash.com/featured/600x400?berry-smoothie",
        },
    ],
    "Shirinliklar": [
        {
            "name": "Shokoladli tort bo'lagi",
            "description": "Yumshoq shokoladli tortning bir bo'lagi.",
            "price": 25000,
            "photo_url": "https://source.unsplash.com/featured/600x400?chocolate-cake",
        },
        {
            "name": "Asalli tort",
            "description": "Qatlamli asalli tort, klassik ta'm.",
            "price": 23000,
            "photo_url": "https://source.unsplash.com/featured/600x400?honey-cake",
        },
        {
            "name": "Dolchinli rulon",
            "description": "Issiq dolchinli bulka.",
            "price": 15000,
            "photo_url": "https://source.unsplash.com/featured/600x400?cinnamon-roll",
        },
        {
            "name": "Ponchik",
            "description": "Yumshoq va shirin ponchik.",
            "price": 12000,
            "photo_url": "https://source.unsplash.com/featured/600x400?donut",
        },
        {
            "name": "Brauni",
            "description": "Qalin shokoladli brauni.",
            "price": 19000,
            "photo_url": "https://source.unsplash.com/featured/600x400?brownie",
        },
        {
            "name": "Pechene",
            "description": "Yangi pishirilgan pechene to'plami.",
            "price": 14000,
            "photo_url": "https://source.unsplash.com/featured/600x400?cookies",
        },
        {
            "name": "Chizkeyk",
            "description": "Kremli chizkeyk bo'lagi.",
            "price": 24000,
            "photo_url": "https://source.unsplash.com/featured/600x400?cheesecake",
        },
        {
            "name": "Baklava",
            "description": "Yong'oq va asal bilan tayyorlangan baklava.",
            "price": 26000,
            "photo_url": "https://source.unsplash.com/featured/600x400?baklava",
        },
    ],
}


async def seed_demo_data(session) -> None:
    existing = await session.execute(select(Category))
    if existing.scalars().first():
        return

    categories = [Category(name=name) for name in CATEGORY_PRODUCTS]
    session.add_all(categories)
    await session.flush()

    products = []
    for category in categories:
        for item in CATEGORY_PRODUCTS[category.name]:
            products.append(
                Product(
                    category_id=category.id,
                    name=item["name"],
                    description=item["description"],
                    price=item["price"],
                    photo_url=item["photo_url"],
                )
            )
    session.add_all(products)
    await session.commit()
