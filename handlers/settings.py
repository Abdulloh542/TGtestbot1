from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.inline import (
    city_keyboard,
    language_keyboard,
    main_menu_keyboard,
    profile_keyboard,
    settings_keyboard,
)
from services.users import get_or_create_user, update_user

router = Router()


@router.callback_query(F.data == "menu:settings")
async def settings_menu(callback: CallbackQuery, session):
    user = await get_or_create_user(session, callback.from_user.id)
    await callback.message.answer(
        "Sozlamalar:", reply_markup=settings_keyboard(user)
    )
    await callback.answer()


@router.callback_query(F.data == "settings:lang")
async def settings_language(callback: CallbackQuery):
    await callback.message.answer("Tilni tanlang:", reply_markup=language_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("lang:"))
async def set_language(callback: CallbackQuery, session):
    lang = callback.data.split(":")[1]
    await update_user(session, callback.from_user.id, language=lang)
    await callback.message.answer("Til yangilandi.", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "settings:city")
async def settings_city(callback: CallbackQuery):
    await callback.message.answer("Shaharni tanlang:", reply_markup=city_keyboard())
    await callback.answer()


@router.callback_query(F.data.startswith("city:"))
async def set_city(callback: CallbackQuery, session):
    city = callback.data.split(":")[1]
    await update_user(session, callback.from_user.id, city=city)
    await callback.message.answer("Shahar saqlandi.", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "settings:notif")
async def toggle_notifications(callback: CallbackQuery, session):
    user = await get_or_create_user(session, callback.from_user.id)
    await update_user(
        session,
        callback.from_user.id,
        notifications_enabled=not user.notifications_enabled,
    )
    user = await get_or_create_user(session, callback.from_user.id)
    await callback.message.answer(
        "Bildirishnomalar holati yangilandi.",
        reply_markup=settings_keyboard(user),
    )
    await callback.answer()


@router.callback_query(F.data == "settings:profile")
async def settings_profile(callback: CallbackQuery, session):
    user = await get_or_create_user(session, callback.from_user.id)
    phone = user.phone or "—"
    address = user.address or "—"
    await callback.message.answer(
        f"Profil:\nTelefon: {phone}\nManzil: {address}",
        reply_markup=profile_keyboard(),
    )
    await callback.answer()
