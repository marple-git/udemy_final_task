from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

authorize_call = CallbackData("authorize", "type")


def authorize_keyboard() -> InlineKeyboardMarkup:
    """
    Choose Authorize Method Keyboard
    :return: InlineKeyboardMarkup
    """
    subscribe = InlineKeyboardButton(text='Подписка', callback_data=authorize_call.new(type='subscribe'))
    invite_code = InlineKeyboardButton(text='Код приглашения', callback_data=authorize_call.new(type="invite_code"))
    return InlineKeyboardMarkup().add(subscribe, invite_code)


def check_subscription() -> InlineKeyboardMarkup:
    """
    Check Subscription Keyboard
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup().add(
           InlineKeyboardButton(text='Проверить подписку', callback_data=authorize_call.new(type="check_subscription")))
