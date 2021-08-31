from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard(is_admin: bool) -> InlineKeyboardMarkup:
    """
    Start Keyboard
    :param is_admin: User Status
    :return: InlineKeyboardMarkup
    """
    profile = InlineKeyboardButton(text='👨🏼‍💻 Профиль', callback_data='profile')
    find_items = InlineKeyboardButton(text='🛍 Выбрать товар', switch_inline_query_current_chat='')
    admin = InlineKeyboardButton(text='🎛 Панель управления', callback_data='admin_panel')
    markup = InlineKeyboardMarkup(row_width=2).add(profile, find_items)
    markup = markup.add(admin) if is_admin else markup
    return markup
