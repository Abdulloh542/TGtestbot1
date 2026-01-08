from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from keyboards.inline import confirm_keyboard, delivery_keyboard, main_menu_keyboard
from services.orders import create_order

router = Router()


class CheckoutStates(StatesGroup):
    contact = State()
    address = State()
    delivery = State()
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
    await state.set_state(CheckoutStates.confirm)
    data = await state.get_data()
    text = (
        "Buyurtmani tasdiqlaysizmi?\n"
        f"Kontakt: {data.get('contact')}\n"
        f"Manzil: {data.get('address')}\n"
        f"Yetkazib berish: {delivery}"
    )
    await callback.message.edit_text(text, reply_markup=confirm_keyboard())
    await callback.answer()


@router.callback_query(F.data == "checkout:confirm")
async def checkout_confirm(callback: CallbackQuery, session, state: FSMContext, config):
    data = await state.get_data()
    order = await create_order(
        session,
        callback.from_user.id,
        data.get("contact", ""),
        data.get("address", ""),
        data.get("delivery", ""),
    )
    if not order:
        await callback.message.edit_text(
            "Savat bo'sh. Buyurtma yaratilmadi.", reply_markup=main_menu_keyboard()
        )
        await state.clear()
        await callback.answer()
        return

    await callback.message.edit_text(
        f"Buyurtmangiz qabul qilindi! ID: {order.id}\nJami: {order.total_amount} so'm",
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
    await callback.message.edit_text(
        "Buyurtma bekor qilindi.", reply_markup=main_menu_keyboard()
    )
    await callback.answer()
