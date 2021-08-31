from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, \
    InlineKeyboardButton

from tgbot.models.items import get_items
from tgbot.models.users import User


async def empty_query(query: InlineQuery, state: FSMContext, user: User):
    if not user.allowed:
        return await query.answer(
                     results=[],
                     switch_pm_text='Бот недоступен. Подключить бота',
                     switch_pm_parameter='connect_user',
                     cache_time=5)

    print(query.query)
    items = await get_items(session=query.bot['db'](), name=query.query)
    bot_username = (await query.bot.get_me()).username
    bot_link = 'https://t.me/{bot_username}?start=i{item_id}'
    articles = [InlineQueryResultArticle(
        id=str(item.id),
        title=item.name,
        description=f'Цена: ${item.price}',
        input_message_content=InputTextMessageContent(
            message_text=item.name,
            parse_mode='HTML'
        ),
        thumb_url=item.photo,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Показать товар',
                                     url=bot_link.format(bot_username=bot_username, item_id=item.id))
            ]
        ])
    ) for item in items]

    await query.answer(articles, cache_time=5, switch_pm_text='Выберите товар', switch_pm_parameter='select_item')


def register_find_items(dp: Dispatcher):
    dp.register_inline_handler(empty_query, state='*')
