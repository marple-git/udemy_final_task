from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.keyboards.Inline.profile import profile_keyboard
from tgbot.models.users import User


async def show_profile(c: CallbackQuery, user: User):
    return await c.message.edit_text(f'<b>👨🏼‍💻 Рады видеть тебя, {c.from_user.first_name}!</b>\n\n'
                                     f'<b>🔅 Telegram ID:</b> {c.from_user.id}\n'
                                     f'<b>🔅 Баланс:</b> ${user.balance}',
                                     reply_markup=profile_keyboard())


async def get_invite_link(c: CallbackQuery):
    bot = await c.bot.get_me()
    await c.message.answer(f'Вот ваша ссылка: t.me/{bot.username}?start=u{c.from_user.id}')


def register_profile(dp: Dispatcher):
    dp.register_callback_query_handler(show_profile, text='profile')
    dp.register_callback_query_handler(get_invite_link, text='get_ref_url')
