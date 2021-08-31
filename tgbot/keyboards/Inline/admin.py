from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.Inline.back import back_call


def admin_keyboard() -> InlineKeyboardMarkup:
    """
    Admin Keyboard
    :return: InlineKeyboardMarkup
    """
    add_item = InlineKeyboardButton(text='➕ Добавить товар', callback_data='add_item')
    advertisement = InlineKeyboardButton(text='📩 Рассылка', callback_data='advertisement')
    back = InlineKeyboardButton(text='🔙 Назад', callback_data=back_call.new(to="main"))
    return InlineKeyboardMarkup(row_width=2).add(add_item, advertisement, back)


def go_to_admin() -> InlineKeyboardMarkup:
    """
    Back to admin panel keyboard
    :return: InlineKeyboardMarkup
    """
    back = InlineKeyboardButton(text='🔙 Назад', callback_data=back_call.new(to="admin"))
    return InlineKeyboardMarkup().add(back)