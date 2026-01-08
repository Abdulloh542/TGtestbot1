from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from keyboards.inline import (
    confirm_keyboard,
    delivery_keyboard,
    main_menu_keyboard,
    payment_keyboard,
    promo_keyboard,
)
from services.cart import cart_total
from services.orders import create_order
from services.promos import get_discount_percent
from services.users import delivery_fee_for, get_or_create_user, update_user

router = Router()


class CheckoutStates(StatesGroup):
    contact = State()
    address = State()
    delivery = State()
    payment = State()
    promo = State()
    confirm = State()


@router.message(CheckoutStates.contact)
async def checkout_contact(message: Message, state: FSMContext):
    if message.contact and message.contact.phone_number:
        contact = message.contact.phone_number
    else:
        contact = message.text.strip()
    await state.update_data(contact=contact)
    await state.set_state(CheckoutStates.address)
    await message.answer("Manzilingizni yozing.", reply_markup=ReplyKeyboardRemove())


@router.message(CheckoutStates.address)
async def checkout_address(message: Message, state: FSMContext):
    address = message.text.strip()
    await state.update_data(address=address)
    await state.set_state(CheckoutStates.delivery)
    await message.answer("Yetkazib berish turini tanlang:", reply_markup=delivery_keyboard())


@router.callback_query(CheckoutStates.delivery, F.data.startswith("delivery:"))
async def checkout_delivery(callback: CallbackQuery, state: FSMContext):
    delivery = callback.data.split(":")[1]
    await state.update_data(delivery=delivery)
    await state.set_state(CheckoutStates.payment)
    await callback.message.answer("To'lov turini tanlang:", reply_markup=payment_keyboard())
    await callback.answer()


@router.callback_query(CheckoutStates.payment, F.data.startswith("pay:"))
async def checkout_payment(callback: CallbackQuery, state: FSMContext):
    payment = callback.data.split(":")[1]
    await state.update_data(payment=payment)
    await state.set_state(CheckoutStates.promo)
    await callback.message.answer(
        "Promo kod bo'lsa kiriting yoki o'tkazib yuboring:", reply_markup=promo_keyboard()
    )
    await callback.answer()


@router.callback_query(CheckoutStates.promo, F.data == "promo:skip")
async def checkout_promo_skip(callback: CallbackQuery, state: FSMContext, session):
    await state.update_data(promo_code=None)
    await _send_confirm(callback.message, state, session, callback.from_user.id)
    await callback.answer()


@router.message(CheckoutStates.promo)
async def checkout_promo_message(message: Message, state: FSMContext, session):
    promo_code = message.text.strip()
    await state.update_data(promo_code=promo_code)
    await _send_confirm(message, state, session, message.from_user.id)


async def _send_confirm(message, state: FSMContext, session, user_id: int):
    data = await state.get_data()
    user = await get_or_create_user(session, user_id)
    subtotal = await cart_total(session, user_id)
    delivery_fee = delivery_fee_for(user, data.get("delivery", ""))
    discount_percent = get_discount_percent(data.get("promo_code"))
    discount_amount = int(subtotal * (discount_percent / 100))
    total = max(subtotal + delivery_fee - discount_amount, 0)
    text = (
        "Buyurtmani tasdiqlaysizmi?\n"
        f"Kontakt: {data.get('contact')}\n"
        f"Manzil: {data.get('address')}\n"
        f"Yetkazib berish: {data.get('delivery')}\n"
        f"To'lov: {data.get('payment')}\n"
        f"Jami: {total} so'm"
    )
    await message.answer(text, reply_markup=confirm_keyboard())
    await state.set_state(CheckoutStates.confirm)


@router.callback_query(CheckoutStates.confirm, F.data == "checkout:confirm")
async def checkout_confirm(callback: CallbackQuery, session, state: FSMContext, config):
    data = await state.get_data()
    user = await get_or_create_user(session, callback.from_user.id)
    subtotal = await cart_total(session, callback.from_user.id)
    delivery_fee = delivery_fee_for(user, data.get("delivery", ""))
    discount_percent = get_discount_percent(data.get("promo_code"))
    discount_amount = int(subtotal * (discount_percent / 100))
    order = await create_order(
        session,
        callback.from_user.id,
        data.get("contact", ""),
        data.get("address", ""),
        data.get("delivery", ""),
        data.get("payment", "Naqd"),
        delivery_fee,
        discount_amount,
        data.get("promo_code"),
    )
    if not order:
        await callback.message.answer(
            "Savat bo'sh. Buyurtma yaratilmadi.", reply_markup=main_menu_keyboard()
        )
        await state.clear()
        await callback.answer()
        return

    await update_user(
        session,
        callback.from_user.id,
        phone=data.get("contact"),
        address=data.get("address"),
    )
    await callback.message.answer(
        f"✅ Buyurtma qabul qilindi! ID: {order.id}",
        reply_markup=main_menu_keyboard(),
    )
    await state.clear()

    if config.admin_ids:
        for admin_id in config.admin_ids:
            await callback.bot.send_message(
                admin_id,
                f"🆕 Yangi buyurtma #{order.id}\nJami: {order.total_amount} so'm",
            )
    await callback.answer()


@router.callback_query(F.data == "checkout:cancel")
async def checkout_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(
        "Buyurtma bekor qilindi.", reply_markup=main_menu_keyboard()
    )
    await callback.answer()
