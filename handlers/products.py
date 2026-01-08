from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.state import State, StatesGroup

from keyboards.inline import (
    categories_keyboard,
    favorites_keyboard,
    main_menu_keyboard,
    product_detail_keyboard,
    products_keyboard,
)
from services.cart import add_to_cart
from services.favorites import is_favorite, list_favorites, toggle_favorite
from services.products import get_categories, get_product, get_products_by_category
from services.products import search_products

router = Router()


class SearchStates(StatesGroup):
    query = State()


@router.callback_query(F.data == "menu:products")
async def show_categories(callback: CallbackQuery, session):
    categories = await get_categories(session)
    await callback.message.answer(
        "Kategoriyani tanlang:", reply_markup=categories_keyboard(categories)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cat:"))
async def show_products(callback: CallbackQuery, session):
    category_id = int(callback.data.split(":")[1])
    products = await get_products_by_category(session, category_id)
    await callback.message.answer(
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
    favorite = await is_favorite(session, callback.from_user.id, product_id)
    await callback.message.answer_photo(
        product.photo_url,
        caption=caption,
        reply_markup=product_detail_keyboard(product_id, quantity, favorite),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("qty:"))
async def adjust_quantity(callback: CallbackQuery, state: FSMContext, session):
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
    favorite = await is_favorite(session, callback.from_user.id, product_id)
    await callback.message.edit_reply_markup(
        reply_markup=product_detail_keyboard(product_id, current, favorite)
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


@router.callback_query(F.data == "menu:search")
async def search_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchStates.query)
    await callback.message.answer("Qidiruv uchun mahsulot nomini yozing.")
    await callback.answer()


@router.message(SearchStates.query)
async def search_result(message: Message, session, state: FSMContext):
    query = message.text.strip()
    results = await search_products(session, query)
    if not results:
        await message.answer("Hech narsa topilmadi.", reply_markup=main_menu_keyboard())
        await state.clear()
        return
    await message.answer(
        "Topilgan mahsulotlar:", reply_markup=products_keyboard(results, 0)
    )
    await state.clear()


@router.callback_query(F.data.startswith("fav:toggle:"))
async def toggle_favorite_handler(callback: CallbackQuery, session, state: FSMContext):
    product_id = int(callback.data.split(":")[2])
    added = await toggle_favorite(session, callback.from_user.id, product_id)
    data = await state.get_data()
    qty_map = data.get("qty_map", {})
    quantity = qty_map.get(product_id, 1)
    await callback.message.edit_reply_markup(
        reply_markup=product_detail_keyboard(product_id, quantity, added)
    )
    await callback.answer("Sevimlilar yangilandi")


@router.callback_query(F.data == "menu:favorites")
async def show_favorites(callback: CallbackQuery, session):
    favorites = await list_favorites(session, callback.from_user.id)
    if not favorites:
        await callback.message.answer("Sevimlilar bo'sh.", reply_markup=main_menu_keyboard())
        await callback.answer()
        return
    await callback.message.answer(
        "Sevimli mahsulotlar:", reply_markup=favorites_keyboard(favorites)
    )
    await callback.answer()
