from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🛍 Mahsulotlar", callback_data="menu:products"),
                InlineKeyboardButton(text="🔎 Qidiruv", callback_data="menu:search"),
            ],
            [
                InlineKeyboardButton(text="🧺 Savat", callback_data="menu:cart"),
                InlineKeyboardButton(text="⭐️ Sevimlilar", callback_data="menu:favorites"),
            ],
            [InlineKeyboardButton(text="📦 Buyurtmalarim", callback_data="menu:orders")],
            [InlineKeyboardButton(text="💬 Savol berish", callback_data="menu:support")],
            [InlineKeyboardButton(text="☎️ Aloqa", callback_data="menu:contact")],
            [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="menu:settings")],
        ]
    )


def categories_keyboard(categories):
    keyboard = [
        [InlineKeyboardButton(text=category.name, callback_data=f"cat:{category.id}")]
        for category in categories
    ]
    keyboard.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:home")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def products_keyboard(products, category_id: int):
    keyboard = [
        [InlineKeyboardButton(text=product.name, callback_data=f"prod:{product.id}")]
        for product in products
    ]
    keyboard.append(
        [InlineKeyboardButton(text="⬅️ Kategoriyalar", callback_data="menu:products")]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def product_detail_keyboard(product_id: int, quantity: int, is_favorite: bool):
    fav_text = "⭐️ Sevimlidan olish" if is_favorite else "☆ Sevimlilarga qo'shish"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data=f"qty:dec:{product_id}"),
                InlineKeyboardButton(text=str(quantity), callback_data="noop"),
                InlineKeyboardButton(text="➕", callback_data=f"qty:inc:{product_id}"),
            ],
            [
                InlineKeyboardButton(
                    text="🧺 Savatga qo‘shish", callback_data=f"cart:add:{product_id}"
                )
            ],
            [InlineKeyboardButton(text=fav_text, callback_data=f"fav:toggle:{product_id}")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:products")],
        ]
    )


def cart_keyboard(items):
    keyboard = []
    for item in items:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{item.product.name} x{item.quantity}",
                    callback_data=f"cart:item:{item.id}",
                )
            ]
        )
    keyboard.append([InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="cart:checkout")])
    keyboard.append([InlineKeyboardButton(text="🧹 Savatni tozalash", callback_data="cart:clear")])
    keyboard.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:home")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def cart_item_keyboard(item_id: int, quantity: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data=f"cart:dec:{item_id}"),
                InlineKeyboardButton(text=str(quantity), callback_data="noop"),
                InlineKeyboardButton(text="➕", callback_data=f"cart:inc:{item_id}"),
            ],
            [InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"cart:remove:{item_id}")],
            [InlineKeyboardButton(text="⬅️ Savat", callback_data="menu:cart")],
        ]
    )


def orders_keyboard(orders):
    keyboard = [
        [
            InlineKeyboardButton(
                text=f"#{order.id} ({order.status})", callback_data=f"order:{order.id}"
            )
        ]
        for order in orders
    ]
    keyboard.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:home")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def delivery_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚚 Kuryer", callback_data="delivery:Kuryer")],
            [InlineKeyboardButton(text="🏪 Olib ketish", callback_data="delivery:Olib ketish")],
        ]
    )


def confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="checkout:confirm")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="checkout:cancel")],
        ]
    )


def payment_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💵 Naqd", callback_data="pay:Naqd")],
            [InlineKeyboardButton(text="💳 Karta", callback_data="pay:Karta")],
        ]
    )


def promo_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏭ O'tkazib yuborish", callback_data="promo:skip")]
        ]
    )


def settings_keyboard(user):
    notif_text = "ON" if user.notifications_enabled else "OFF"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Til", callback_data="settings:lang")],
            [InlineKeyboardButton(text="📍 Shahar", callback_data="settings:city")],
            [
                InlineKeyboardButton(
                    text=f"🔔 Bildirishnomalar: {notif_text}",
                    callback_data="settings:notif",
                )
            ],
            [InlineKeyboardButton(text="👤 Profil", callback_data="settings:profile")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:home")],
        ]
    )


def language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang:uz")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:settings")],
        ]
    )


def city_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Toshkent", callback_data="city:Toshkent")],
            [InlineKeyboardButton(text="Samarqand", callback_data="city:Samarqand")],
            [InlineKeyboardButton(text="Buxoro", callback_data="city:Buxoro")],
            [InlineKeyboardButton(text="Boshqa", callback_data="city:Boshqa")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:settings")],
        ]
    )


def profile_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧹 Savatni tozalash", callback_data="cart:clear")],
            [
                InlineKeyboardButton(
                    text="🗑 Support tarixini tozalash",
                    callback_data="support:clear",
                )
            ],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:settings")],
        ]
    )


def favorites_keyboard(favorites):
    keyboard = [
        [
            InlineKeyboardButton(
                text=fav.product.name, callback_data=f"prod:{fav.product_id}"
            )
        ]
        for fav in favorites
    ]
    keyboard.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="menu:home")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def admin_status_keyboard(order_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ CONFIRMED", callback_data=f"admin:status:{order_id}:CONFIRMED"
                ),
                InlineKeyboardButton(
                    text="🚚 ON_THE_WAY",
                    callback_data=f"admin:status:{order_id}:ON_THE_WAY",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✔️ DONE", callback_data=f"admin:status:{order_id}:DONE"
                ),
                InlineKeyboardButton(
                    text="❌ CANCELLED",
                    callback_data=f"admin:status:{order_id}:CANCELLED",
                ),
            ],
        ]
    )


def admin_panel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🆕 Yangi buyurtmalar", callback_data="admin:new")],
            [InlineKeyboardButton(text="🔎 ID bo'yicha topish", callback_data="admin:find")],
            [InlineKeyboardButton(text="🔁 Statusni o'zgartirish", callback_data="admin:status")],
            [InlineKeyboardButton(text="📢 Broadcast", callback_data="admin:broadcast")],
            [InlineKeyboardButton(text="📊 Statistika", callback_data="admin:stats")],
            [InlineKeyboardButton(text="📁 CSV eksport", callback_data="admin:export")],
        ]
    )


def support_cancel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="support:cancel")]
        ]
    )
