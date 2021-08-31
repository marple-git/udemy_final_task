from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.keyboards.Inline.admin import admin_keyboard


async def show_admin_panel(c: CallbackQuery):
    return await c.message.edit_text('♻️ Вы попали в меню администратора', reply_markup=admin_keyboard())


def register_admin_panel(dp: Dispatcher):
    dp.register_callback_query_handler(show_admin_panel, text='admin_panel')
