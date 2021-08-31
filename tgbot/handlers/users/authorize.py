from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.config import CHANNELS, INVITE_CODES
from tgbot.functions.subscription import check
from tgbot.keyboards.Inline.authorize import authorize_call, check_subscription
from tgbot.misc.states import Authorization
from tgbot.models.users import User


async def authorize_subscribe(c: CallbackQuery):
    text = 'Оформите подписку на следующие каналы:\n\n'
    for channel_id in CHANNELS:
        channel = await c.bot.get_chat(channel_id)
        link = await channel.export_invite_link()
        text += f'<b>{channel.title}</b> - <a href="{link}">клик</a>'
    return await c.message.edit_text(text, reply_markup=check_subscription())


async def check_sub(c: CallbackQuery, user: User):
    await c.answer()
    text = ''
    subscribed_on = 0
    for channel_id in CHANNELS:
        status = await check(user_id=c.from_user.id, channel=channel_id)
        channel = await c.bot.get_chat(channel_id)
        if status:
            text += f'Подписка на канал <b>{channel.title}</b> оформлена!\n\n'
            subscribed_on += 1
        else:
            invite_link = await channel.export_invite_link()
            text += (f'Подписка на канал <b>{channel.title}</b> не оформлена! '
                     f'<a href="{invite_link}">Нужно подписаться.</a>\n\n')
    if subscribed_on == len(CHANNELS):
        text = '🥰 Поздравляю, вы получили доступ к боту, введите /start для работы'
        await user.update_user(session=c.bot['db'](), updated_fields={
            'allowed': True
        })
    await c.message.edit_text(text)


async def show_invite_code_input(c: CallbackQuery):
    await c.message.edit_text('Введите код приглашения:')
    await Authorization.code.set()


async def get_code(m: Message, user: User, state: FSMContext):
    if m.text in INVITE_CODES:
        await m.answer('🥰 Поздравляю, вы получили доступ к боту, введите /start для работы')
        await user.update_user(session=m.bot['db'](), updated_fields={
            'allowed': True
        })
    else:
        await m.answer('Кажется, вы ввели неверный код.')
    await state.finish()


def register_authorize(dp: Dispatcher):
    dp.register_callback_query_handler(authorize_subscribe, authorize_call.filter(type="subscribe"))
    dp.register_callback_query_handler(check_sub, authorize_call.filter(type="check_subscription"))
    dp.register_callback_query_handler(show_invite_code_input, authorize_call.filter(type="invite_code"))
    dp.register_message_handler(get_code, state=Authorization.code)
