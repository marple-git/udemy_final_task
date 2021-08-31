from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

buy_call = CallbackData("buy_item", "item_id")
payment_call = CallbackData("payment", "method")
card_call = CallbackData("card", "bill_id")


def buy_item(item_id: int) -> InlineKeyboardMarkup:
    """
    Buy Item Keyboard
    :param item_id: Item ID
    :return: InlineKeyboardMarkup
    """
    buy = InlineKeyboardButton(text='🛒 Купить', callback_data=buy_call.new(item_id=item_id))
    return InlineKeyboardMarkup().add(buy)


def payment_methods() -> InlineKeyboardMarkup:
    """
    Payment Methods Keyboard
    :return: InlineKeyboardMarkup
    """
    card = InlineKeyboardButton(text=' 💳 Qiwi/Card', callback_data=payment_call.new(method='card'))
    return InlineKeyboardMarkup().add(card)


def pay_card(bill_id: str, url: str) -> InlineKeyboardMarkup:
    """
    Payment Keyboard
    :param url: P2P Payment URL
    :param bill_id: P2P Bill ID
    :return: InlineKeyboardMarkup
    """

    pay = InlineKeyboardButton(text='💰 Оплатить', url=url)
    check = InlineKeyboardButton(text='♻️ Проверить', callback_data=card_call.new(bill_id=bill_id))
    back = InlineKeyboardButton(text='❌ Отмена', callback_data='delete_message')
    return InlineKeyboardMarkup(row_width=2).add(pay, check, back)
