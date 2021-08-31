from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

buy_call = CallbackData("buy_item", "item_id")


def buy_item(item_id: int) -> InlineKeyboardMarkup:
    """
    Buy Item Keyboard
    :param item_id: Item ID
    :return: InlineKeyboardMarkup
    """
    buy = InlineKeyboardButton(text='🛒 Купить', callback_data=buy_call.new(item_id=item_id))
    return InlineKeyboardMarkup().add(buy)