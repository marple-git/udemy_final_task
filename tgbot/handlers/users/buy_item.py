from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.Inline.back import delete_message
from tgbot.keyboards.Inline.items import buy_call


async def enter_amount(c: CallbackQuery):
    await c.message.edit_text('✏️ Введите количество товара', reply_markup=delete_message())


def register_buy_item(dp: Dispatcher):
    dp.register_callback_query_handler(enter_amount, buy_call.filter())