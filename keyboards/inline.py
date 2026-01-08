from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛍 Mahsulotlar", callback_data="menu:products")],
            [InlineKeyboardButton(text="🧺 Savat", callback_data="menu:cart")],
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


def product_detail_keyboard(product_id: int, quantity: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data=f"qty:dec:{product_id}"),
                InlineKeyboardButton(text=str(quantity), callback_data="noop"),
                InlineKeyboardButton(text="➕", callback_data=f"qty:inc:{product_id}"),
            ],
            [InlineKeyboardButton(text="🧺 Savatga", callback_data=f"cart:add:{product_id}")],
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
        [InlineKeyboardButton(text=f"Buyurtma #{order.id}", callback_data=f"order:{order.id}")]
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


def admin_panel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🆕 Yangi buyurtmalar", callback_data="admin:new")],
            [InlineKeyboardButton(text="🔎 ID bo'yicha topish", callback_data="admin:find")],
            [InlineKeyboardButton(text="✅ Bajarildi", callback_data="admin:done")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin:cancel")],
            [InlineKeyboardButton(text="📊 Statistika", callback_data="admin:stats")],
            [InlineKeyboardButton(text="📁 CSV eksport", callback_data="admin:export")],
        ]
    )
