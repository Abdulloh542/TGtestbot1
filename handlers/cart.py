from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, KeyboardButton, ReplyKeyboardMarkup

from keyboards.inline import cart_item_keyboard, cart_keyboard, main_menu_keyboard
from handlers.checkout import CheckoutStates
from services.cart import clear_cart, get_cart_items, update_quantity

router = Router()


@router.callback_query(F.data == "menu:cart")
async def show_cart(callback: CallbackQuery, session):
    items = await get_cart_items(session, callback.from_user.id)
    if not items:
        await callback.message.answer("Savat bo'sh.", reply_markup=main_menu_keyboard())
        await callback.answer()
        return

    total = sum(item.quantity * item.product.price for item in items)
    text = f"Savatdagi mahsulotlar:\nJami: {total} so'm"
    await callback.message.answer(text, reply_markup=cart_keyboard(items))
    await callback.answer()


@router.callback_query(F.data.startswith("cart:item:"))
async def show_cart_item(callback: CallbackQuery, session):
    item_id = int(callback.data.split(":")[2])
    items = await get_cart_items(session, callback.from_user.id)
    item = next((i for i in items if i.id == item_id), None)
    if not item:
        await callback.answer("Mahsulot topilmadi", show_alert=True)
        return
    text = f"{item.product.name}\nNarx: {item.product.price} so'm"
    await callback.message.answer(
        text, reply_markup=cart_item_keyboard(item.id, item.quantity)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cart:inc:"))
async def cart_inc(callback: CallbackQuery, session):
    item_id = int(callback.data.split(":")[2])
    items = await get_cart_items(session, callback.from_user.id)
    item = next((i for i in items if i.id == item_id), None)
    if not item:
        await callback.answer("Mahsulot topilmadi", show_alert=True)
        return
    await update_quantity(session, item.id, item.quantity + 1)
    await callback.message.edit_reply_markup(
        reply_markup=cart_item_keyboard(item.id, item.quantity + 1)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cart:dec:"))
async def cart_dec(callback: CallbackQuery, session):
    item_id = int(callback.data.split(":")[2])
    items = await get_cart_items(session, callback.from_user.id)
    item = next((i for i in items if i.id == item_id), None)
    if not item:
        await callback.answer("Mahsulot topilmadi", show_alert=True)
        return
    new_qty = max(1, item.quantity - 1)
    await update_quantity(session, item.id, new_qty)
    await callback.message.edit_reply_markup(
        reply_markup=cart_item_keyboard(item.id, new_qty)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cart:remove:"))
async def cart_remove(callback: CallbackQuery, session):
    item_id = int(callback.data.split(":")[2])
    await update_quantity(session, item_id, 0)
    await callback.message.answer(
        "Mahsulot savatdan olib tashlandi.", reply_markup=main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "cart:clear")
async def cart_clear(callback: CallbackQuery, session):
    await clear_cart(session, callback.from_user.id)
    await callback.message.answer("Savat tozalandi.", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "cart:checkout")
async def cart_checkout(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CheckoutStates.contact)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Kontakt yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await callback.message.answer("Kontakt raqamingizni yuboring.", reply_markup=keyboard)
    await callback.answer()
