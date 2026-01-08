from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import (
    categories_keyboard,
    product_detail_keyboard,
    products_keyboard,
)
from keyboards.inline import main_menu_keyboard
from services.cart import add_to_cart
from services.products import get_categories, get_product, get_products_by_category

router = Router()


@router.callback_query(F.data == "menu:products")
async def show_categories(callback: CallbackQuery, session):
    categories = await get_categories(session)
    await callback.message.edit_text(
        "Kategoriyani tanlang:", reply_markup=categories_keyboard(categories)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cat:"))
async def show_products(callback: CallbackQuery, session):
    category_id = int(callback.data.split(":")[1])
    products = await get_products_by_category(session, category_id)
    await callback.message.edit_text(
        "Mahsulotlar ro'yxati:",
        reply_markup=products_keyboard(products, category_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("prod:"))
async def show_product_detail(callback: CallbackQuery, session, state: FSMContext):
    product_id = int(callback.data.split(":")[1])
    product = await get_product(session, product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi", show_alert=True)
        return

    data = await state.get_data()
    qty_map = data.get("qty_map", {})
    quantity = qty_map.get(product_id, 1)

    caption = (
        f"{product.name}\n\n{product.description}\n"
        f"Narx: {product.price} so'm"
    )
    await callback.message.answer_photo(
        product.photo_url,
        caption=caption,
        reply_markup=product_detail_keyboard(product_id, quantity),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("qty:"))
async def adjust_quantity(callback: CallbackQuery, state: FSMContext):
    _, action, product_id = callback.data.split(":")
    product_id = int(product_id)
    data = await state.get_data()
    qty_map = data.get("qty_map", {})
    current = qty_map.get(product_id, 1)
    if action == "inc":
        current += 1
    elif action == "dec":
        current = max(1, current - 1)
    qty_map[product_id] = current
    await state.update_data(qty_map=qty_map)
    await callback.message.edit_reply_markup(
        reply_markup=product_detail_keyboard(product_id, current)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cart:add:"))
async def add_product_to_cart(callback: CallbackQuery, session, state: FSMContext):
    product_id = int(callback.data.split(":")[2])
    data = await state.get_data()
    qty_map = data.get("qty_map", {})
    quantity = qty_map.get(product_id, 1)
    await add_to_cart(session, callback.from_user.id, product_id, quantity)
    await callback.message.answer(
        "Mahsulot savatga qo'shildi.", reply_markup=main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "noop")
async def noop_callback(callback: CallbackQuery):
    await callback.answer()
