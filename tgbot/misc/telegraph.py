from io import BytesIO

import aiohttp
from aiogram import Bot
from aiogram import types


async def photo_link(photo: types.photo_size.PhotoSize) -> str:
    bot = Bot.get_current()
    with await photo.download(BytesIO()) as file:
        form = aiohttp.FormData()
        form.add_field(
            name='file',
            value=file,
        )
        async with bot.session.post('https://telegra.ph/upload', data=form) as response:
            img_src = await response.json()

    return 'http://telegra.ph/' + img_src[0]["src"]
