from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

back_call = CallbackData("back", "to")


def back_menu(to: str = 'main') -> InlineKeyboardMarkup:
    """
    Back Menu
    :param to: Back to
    :return: InlineKeyboardMarkup
    """
    back = InlineKeyboardButton(text='🔙 Назад', callback_data=back_call.new(to=to))
    return InlineKeyboardMarkup().add(back)


def delete_message() -> InlineKeyboardMarkup:
    """
    Delete Message Keyboard
    :return: InlineKeyboardMarkup
    """
    delete = InlineKeyboardButton(text='❌ Отмена', callback_data='delete_message')
    return InlineKeyboardMarkup().add(delete)
