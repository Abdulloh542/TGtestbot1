from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from keyboards.inline import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "Assalomu alaykum! Shop botimizga xush kelibsiz.\n"
        "Asosiy menyudan kerakli bo'limni tanlang."
    )
    await message.answer(text, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "menu:home")
async def menu_home(callback: CallbackQuery):
    text = "Asosiy menyu:"
    await callback.message.edit_text(text, reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:contact")
async def menu_contact(callback: CallbackQuery):
    text = "Aloqa: +998 90 123 45 67\nEmail: support@example.com"
    await callback.message.edit_text(text, reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu:settings")
async def menu_settings(callback: CallbackQuery):
    text = "Sozlamalar bo'limi tez orada qo'shiladi."
    await callback.message.edit_text(text, reply_markup=main_menu_keyboard())
    await callback.answer()
