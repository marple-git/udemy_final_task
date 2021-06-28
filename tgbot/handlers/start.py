from aiogram import Dispatcher
from aiogram.types import Message
import time


async def start(m: Message):
    await m.answer('Привет, товарищ ' + m.from_user.first_name)


def register(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])