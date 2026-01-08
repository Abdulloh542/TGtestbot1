import csv
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile, Message
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from db.models import Order, OrderItem
from keyboards.inline import admin_panel_keyboard
from services.orders import get_new_orders, get_order_detail, update_order_status
from services.tickets import add_ticket_message, get_ticket

router = Router()


class AdminStates(StatesGroup):
    find_id = State()
    mark_done = State()
    cancel_order = State()


def _is_admin(source: Message | CallbackQuery, config) -> bool:
    return source.from_user.id in config.admin_ids


@router.message(Command("admin"))
async def admin_panel(message: Message, config):
    if not _is_admin(message, config):
        await message.answer("Sizda admin huquqi yo'q.")
        return
    await message.answer("Admin panel:", reply_markup=admin_panel_keyboard())


@router.callback_query(F.data.startswith("admin:"))
async def admin_actions(callback: CallbackQuery, state: FSMContext, config, session):
    if not _is_admin(callback, config):
        await callback.answer("Ruxsat yo'q", show_alert=True)
        return

    action = callback.data.split(":")[1]
    if action == "new":
        await show_new_orders(callback, session)
    elif action == "find":
        await state.set_state(AdminStates.find_id)
        await callback.message.edit_text("Buyurtma ID ni yuboring:")
    elif action == "done":
        await state.set_state(AdminStates.mark_done)
        await callback.message.edit_text("Bajarildi deb belgilash uchun ID yuboring:")
    elif action == "cancel":
        await state.set_state(AdminStates.cancel_order)
        await callback.message.edit_text("Bekor qilish uchun ID yuboring:")
    elif action == "stats":
        await show_stats(callback, session)
    elif action == "export":
        await export_csv(callback, session)
    await callback.answer()


@router.message(AdminStates.find_id)
async def admin_find_order(message: Message, state: FSMContext, session):
    try:
        order_id = int(message.text.strip())
    except ValueError:
        await message.answer("Iltimos, raqam yuboring.")
        return

    order = await get_order_detail(session, order_id)
    if not order:
        await message.answer("Buyurtma topilmadi.", reply_markup=admin_panel_keyboard())
        await state.clear()
        return

    items_text = "\n".join(
        f"- {item.product.name} x{item.quantity}"
        for item in order.items
    )
    text = (
        f"Buyurtma #{order.id}\n"
        f"Holat: {order.status}\n"
        f"Kontakt: {order.contact}\n"
        f"Manzil: {order.address}\n"
        f"Yetkazib berish: {order.delivery_type}\n"
        f"Jami: {order.total_amount} so'm\n"
        f"Mahsulotlar:\n{items_text}"
    )
    await message.answer(text, reply_markup=admin_panel_keyboard())
    await state.clear()


@router.message(AdminStates.mark_done)
async def admin_mark_done(message: Message, state: FSMContext, session):
    try:
        order_id = int(message.text.strip())
    except ValueError:
        await message.answer("Iltimos, raqam yuboring.")
        return

    order = await update_order_status(session, order_id, "DONE")
    if not order:
        await message.answer("Buyurtma topilmadi.", reply_markup=admin_panel_keyboard())
    else:
        await message.answer("Buyurtma bajarildi.", reply_markup=admin_panel_keyboard())
    await state.clear()


@router.message(AdminStates.cancel_order)
async def admin_cancel(message: Message, state: FSMContext, session):
    try:
        order_id = int(message.text.strip())
    except ValueError:
        await message.answer("Iltimos, raqam yuboring.")
        return

    order = await update_order_status(session, order_id, "CANCELLED")
    if not order:
        await message.answer("Buyurtma topilmadi.", reply_markup=admin_panel_keyboard())
    else:
        await message.answer("Buyurtma bekor qilindi.", reply_markup=admin_panel_keyboard())
    await state.clear()


@router.message(Command("reply"))
async def admin_reply(message: Message, session, config):
    if not _is_admin(message, config):
        await message.answer("Sizda admin huquqi yo'q.")
        return
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Foydalanish: /reply <ticketId> <xabar>")
        return

    ticket_id = int(parts[1])
    reply_text = parts[2]

    ticket = await add_ticket_message(session, ticket_id, "ADMIN", reply_text)
    if not ticket:
        await message.answer("Ticket topilmadi.")
        return

    details = await get_ticket(session, ticket_id)
    if details:
        await message.bot.send_message(details.user_id, f"Admin javobi: {reply_text}")
    await message.answer("Javob yuborildi.")


async def show_new_orders(callback: CallbackQuery, session):
    orders = await get_new_orders(session)
    if not orders:
        await callback.message.edit_text(
            "Yangi buyurtmalar yo'q.", reply_markup=admin_panel_keyboard()
        )
        return

    lines = [f"#{order.id} | {order.total_amount} so'm" for order in orders]
    text = "Yangi buyurtmalar:\n" + "\n".join(lines)
    await callback.message.edit_text(text, reply_markup=admin_panel_keyboard())


async def show_stats(callback: CallbackQuery, session):
    total_orders = await session.scalar(select(func.count(Order.id)))
    new_orders = await session.scalar(
        select(func.count(Order.id)).where(Order.status == "NEW")
    )
    revenue = await session.scalar(select(func.coalesce(func.sum(Order.total_amount), 0)))
    text = (
        f"Statistika:\nJami buyurtmalar: {total_orders}\n"
        f"Yangi buyurtmalar: {new_orders}\n"
        f"Umumiy tushum: {revenue} so'm"
    )
    await callback.message.edit_text(text, reply_markup=admin_panel_keyboard())


async def export_csv(callback: CallbackQuery, session):
    result = await session.execute(
        select(Order)
        .options(selectinload(Order.items).selectinload(OrderItem.product))
        .order_by(Order.created_at.desc())
    )
    orders = result.scalars().all()
    export_dir = Path("exports")
    export_dir.mkdir(exist_ok=True)
    file_path = export_dir / "orders.csv"

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "order_id",
                "status",
                "user_id",
                "contact",
                "address",
                "delivery_type",
                "total_amount",
                "items",
                "created_at",
            ]
        )
        for order in orders:
            items = "; ".join(
                f"{item.product.name} x{item.quantity}" for item in order.items
            )
            writer.writerow(
                [
                    order.id,
                    order.status,
                    order.user_id,
                    order.contact,
                    order.address,
                    order.delivery_type,
                    order.total_amount,
                    items,
                    order.created_at.isoformat(),
                ]
            )

    document = FSInputFile(str(file_path))
    await callback.message.answer_document(document)
    await callback.message.answer("CSV tayyor.", reply_markup=admin_panel_keyboard())
