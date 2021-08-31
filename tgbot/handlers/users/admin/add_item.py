
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ContentType

from tgbot.filters.admin import IsAdmin
from tgbot.keyboards.Inline.admin import go_to_admin
from tgbot.misc.states import AddItem
from tgbot.misc.telegraph import photo_link
from tgbot.models.items import add_item


async def enter_name(c: CallbackQuery, state: FSMContext):
    await c.message.edit_text('✏️ Введите название товара', reply_markup=go_to_admin())
    await AddItem.name.set()
    async with state.proxy() as data:
        data['msg'] = c.message.message_id


async def get_name(m: Message, state: FSMContext):
    msg = await m.answer('✏️ Введите описание товара', reply_markup=go_to_admin())
    async with state.proxy() as data:
        data['name'] = m.text
        message = data['msg']
        data['msg'] = msg.message_id
    await m.bot.edit_message_reply_markup(message_id=message, chat_id=m.chat.id)
    await AddItem.description.set()


async def get_description(m: Message, state: FSMContext):
    msg = await m.answer('✏ Введите стоимость товара', reply_markup=go_to_admin())
    async with state.proxy() as data:
        data['description'] = m.text
        message = data['msg']
        data['msg'] = msg.message_id
    await m.bot.edit_message_reply_markup(message_id=message, chat_id=m.chat.id)
    await AddItem.price.set()


async def get_price(m: Message, state: FSMContext):
    if m.text.isnumeric():
        msg = await m.answer('✏ Отправьте фотографию товара', reply_markup=go_to_admin())
        await AddItem.photo.set()
    else:
        msg = await m.answer('✏ Введите верную стоимость товара', reply_markup=go_to_admin())
    async with state.proxy() as data:
        data['price'] = m.text
        message = data['msg']
        data['msg'] = msg.message_id
    await m.bot.edit_message_reply_markup(message_id=message, chat_id=m.chat.id)


async def get_photo(m: Message, state: FSMContext):
    photo = m.photo[-1]
    link = await photo_link(photo)
    async with state.proxy() as data:
        name = data['name']
        description = data['description']
        price = data['price']
    await add_item(name=name, description=description, price=price, photo=link, session=m.bot['db']())
    await m.answer_photo(photo=link, caption=f'🛍 Товар был успешно добавлен!\n\n'
                                             f'📝 Название: {name}\n'
                                             f'💬 Описание: {description}\n'
                                             f'💸 Стоимость: {price} руб.\n')
    await state.finish()


def register_add_item(dp: Dispatcher):
    dp.register_callback_query_handler(enter_name, IsAdmin(), text='add_item')
    dp.register_message_handler(get_name, IsAdmin(), state=AddItem.name)
    dp.register_message_handler(get_description, IsAdmin(), state=AddItem.description)
    dp.register_message_handler(get_price, IsAdmin(), state=AddItem.price)
    dp.register_message_handler(get_photo, IsAdmin(), state=AddItem.photo, content_types=ContentType.PHOTO)
