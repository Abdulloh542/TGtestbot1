from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from keyboards.inline import main_menu_keyboard
from services.tickets import create_ticket

router = Router()


class SupportStates(StatesGroup):
    message = State()


@router.callback_query(F.data == "menu:support")
async def support_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SupportStates.message)
    await callback.message.edit_text("Savolingizni yozing, biz tez orada javob beramiz.")
    await callback.answer()


@router.message(SupportStates.message)
async def support_message(message: Message, state: FSMContext, session):
    ticket = await create_ticket(session, message.from_user.id, message.text)
    await message.answer(
        f"Murojaatingiz qabul qilindi. Ticket ID: {ticket.id}",
        reply_markup=main_menu_keyboard(),
    )
    await state.clear()
