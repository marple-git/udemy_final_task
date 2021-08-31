from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentTypes
from aiogram_broadcaster import MessageBroadcaster

from tgbot.filters.admin import IsAdmin
from tgbot.keyboards.Inline.admin import go_to_admin
from tgbot.misc.states import Advertisement
from tgbot.models.users import User


async def enter_message(c: CallbackQuery, state: FSMContext):
    await c.message.answer('✏️ Отправьте сообщение для рассылки', reply_markup=go_to_admin())
    await Advertisement.message.set()
    async with state.proxy() as data:
        data['msg'] = c.message.message_id


async def get_message(m: Message, state: FSMContext):
    async with state.proxy() as data:
        message = data['msg']
    await m.bot.edit_message_reply_markup(chat_id=m.chat.id, message_id=message)
    users = await User.get_all_users(session=m.bot['db']())
    await m.reply('✉️ Рассылка запущена.', reply_markup=go_to_admin())
    await state.finish()
    broadcaster = MessageBroadcaster(users, m)
    await broadcaster.run()
    await m.reply(f'🉐 <b>Рассылка была завершена!</b>\n\n'
                  f'📤 <b>Отправлено:</b> {len(broadcaster._successful)}/{len(broadcaster.chats)}')


def register_advertisement(dp: Dispatcher):
    dp.register_callback_query_handler(enter_message, IsAdmin(), text='advertisement')
    dp.register_message_handler(get_message, IsAdmin(), state=Advertisement.message, content_types=ContentTypes.ANY)
