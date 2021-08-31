from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.Inline.back import back_call


def profile_keyboard() -> InlineKeyboardMarkup:
    """
    Profile Keyboard
    :return: InlineKeyboardMarkup
    """
    get_link = InlineKeyboardButton(text='🔗 Получить реф. ссылку',
                                    callback_data='get_ref_url')
    back = InlineKeyboardButton(text='🔙 Назад', callback_data=back_call.new(to='main'))
    return InlineKeyboardMarkup(row_width=1).add(get_link, back)
