from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.inline import main_menu_keyboard, orders_keyboard
from services.orders import get_order_detail, get_user_orders

router = Router()


@router.callback_query(F.data == "menu:orders")
async def show_orders(callback: CallbackQuery, session):
    orders = await get_user_orders(session, callback.from_user.id)
    if not orders:
        await callback.message.edit_text(
            "Hozircha buyurtmalar yo'q.", reply_markup=main_menu_keyboard()
        )
        await callback.answer()
        return
    await callback.message.edit_text(
        "Buyurtmalaringiz:", reply_markup=orders_keyboard(orders)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("order:"))
async def order_detail(callback: CallbackQuery, session):
    order_id = int(callback.data.split(":")[1])
    order = await get_order_detail(session, order_id)
    if not order or order.user_id != callback.from_user.id:
        await callback.answer("Buyurtma topilmadi", show_alert=True)
        return

    items_text = "\n".join(
        f"- {item.product.name} x{item.quantity}"
        for item in order.items
    )
    text = (
        f"Buyurtma #{order.id}\n"
        f"Holat: {order.status}\n"
        f"Jami: {order.total_amount} so'm\n"
        f"Manzil: {order.address}\n"
        f"Mahsulotlar:\n{items_text}"
    )
    await callback.message.edit_text(text, reply_markup=main_menu_keyboard())
    await callback.answer()
