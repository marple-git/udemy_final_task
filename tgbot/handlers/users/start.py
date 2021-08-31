import re

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from tgbot.config import load_config
from tgbot.keyboards.Inline.authorize import authorize_keyboard
from tgbot.keyboards.Inline.items import buy_item
from tgbot.keyboards.Inline.start import start_keyboard
from tgbot.models.items import get_item
from tgbot.models.users import User


async def start(m: Message, user: User):
    config = load_config(".env")
    if not user.admin and m.chat.id in config.tg_bot.admin_ids:
        await user.update_user(session=m.bot['db'](), updated_fields={
            'admin': True
        })
    if user.allowed:
        return await m.answer('<b>Главное меню</b>', reply_markup=start_keyboard(is_admin=user.admin))
    else:
        return await m.answer('❗️ У вас нет доступа.\n'
                              'Вы можете получить доступ следующими путями:\n'
                              '1. Ввести код\n'
                              '2. Перейти по реферальной ссылке\n'
                              '3. Подписаться на наши каналы', reply_markup=authorize_keyboard())


async def start_with_ref_link(m: Message, user: User):
    if user.allowed:
        return await m.reply('❗️ Вы уже авторизованы')
    args = int(m.get_args()[1:])
    referrer = await user.get_user(session=m.bot['db'](), chat_id=args)
    if not referrer:
        return await m.reply('❗️ К сожалению, данная ссылка недействительна.')
    await user.update_user(session=m.bot['db'](), updated_fields={'allowed': True})
    await user.update_user(session=m.bot['db'](), updated_fields={'balance': referrer.balance + 10}, chat_id=referrer.chat_id)
    await m.bot.send_message(referrer.chat_id, f'🙈 Вы получили $10 за то, что пригласили пользователя {m.from_user.get_mention()}')
    return await m.reply('🥰 Поздравляю, вы получили доступ! Введите /start')


async def show_item(m: Message, user: User):
    if not user.allowed:
        return await m.answer('❗️ У вас нет доступа.\n'
                              'Вы можете получить доступ следующими путями:\n'
                              '1. Ввести код\n'
                              '2. Перейти по реферальной ссылке\n'
                              '3. Подписаться на наши каналы')
    args = m.get_args()
    item_id = int(args[1:])
    item = await get_item(session=m.bot['db'](), item_id=item_id)
    await m.answer_photo(item.photo, caption=f'❗️ Вы выбрали товар №{item.id}\n\n'
                                             f'🦋 Название: {item.name}\n'
                                             f'📝 Описание: {item.description}\n'
                                             f'💸 Стоимость: {item.price} руб.',
                                             reply_markup=buy_item(item_id=item_id))


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_with_ref_link, CommandStart(deep_link=re.compile(r'u(\d+)')))
    dp.register_message_handler(show_item, CommandStart(deep_link=re.compile(r'i(\d+)')))
    dp.register_message_handler(start, CommandStart())
