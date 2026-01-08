from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from keyboards.inline import main_menu_keyboard, support_cancel_keyboard
from db.models import Ticket, TicketMessage
from services.tickets import create_ticket

router = Router()


class SupportStates(StatesGroup):
    message = State()


@router.callback_query(F.data == "menu:support")
async def support_start(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SupportStates.message)
    await callback.message.answer(
        "Savolingizni yozing, biz tez orada javob beramiz.",
        reply_markup=support_cancel_keyboard(),
    )
    await callback.answer()


@router.message(SupportStates.message)
async def support_message(message: Message, state: FSMContext, session, config):
    ticket = await create_ticket(session, message.from_user.id, message.text)
    await message.answer("✅ Yuborildi", reply_markup=main_menu_keyboard())
    await state.clear()

    if config and config.admin_ids:
        for admin_id in config.admin_ids:
            await message.bot.send_message(
                admin_id,
                f"🆕 Ticket #{ticket.id}\nUser ID: {message.from_user.id}\n{message.text}",
            )


@router.callback_query(F.data == "support:cancel")
async def support_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Bekor qilindi.", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "support:clear")
async def support_clear(callback: CallbackQuery, session):
    await session.execute(
        TicketMessage.__table__.delete().where(TicketMessage.ticket_id.in_(
            select(Ticket.id).where(Ticket.user_id == callback.from_user.id)
        ))
    )
    await session.execute(
        Ticket.__table__.delete().where(Ticket.user_id == callback.from_user.id)
    )
    await session.commit()
    await callback.message.answer("Support tarixingiz tozalandi.", reply_markup=main_menu_keyboard())
    await callback.answer()
