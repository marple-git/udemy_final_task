from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards.Inline.admin import admin_keyboard
from tgbot.keyboards.Inline.back import back_call
from tgbot.keyboards.Inline.start import start_keyboard
from tgbot.models.users import User


async def back(c: CallbackQuery, callback_data: dict, user: User, state: FSMContext):
    await state.finish()
    to = callback_data['to']
    if to == 'main':
        return await c.message.edit_text('<b>Главное меню</b>', reply_markup=start_keyboard(is_admin=user.admin))
    elif to == 'admin':
        return await c.message.edit_text('♻️ Вы попали в меню администратора', reply_markup=admin_keyboard())


async def delete_message(c: CallbackQuery, state: FSMContext):
    await state.finish()
    await c.message.delete()


def register_back(dp: Dispatcher):
    dp.register_callback_query_handler(back, back_call.filter(), state='*')
    dp.register_callback_query_handler(delete_message, text='delete_message', state='*')
