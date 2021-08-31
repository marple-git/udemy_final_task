from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from glQiwiApi import QiwiWrapper

from tgbot.config import load_config
from tgbot.keyboards.Inline.back import delete_message
from tgbot.keyboards.Inline.items import buy_call, payment_methods, payment_call, pay_card, card_call
from tgbot.misc.states import BuyItem
from tgbot.models.items import get_item
from tgbot.models.users import User


async def enter_amount(c: CallbackQuery, callback_data: dict, state: FSMContext):
    await c.answer()
    message = await c.message.answer('✏️ Введите количество товара', reply_markup=delete_message())
    await BuyItem.amount.set()
    async with state.proxy() as data:
        data['msg'] = message.message_id
        data['item_id'] = callback_data['item_id']


async def get_amount(m: Message, state: FSMContext):
    if m.text.isnumeric() and int(m.text) > 0:
        message = await m.answer('✏ Введите адрес доставки', reply_markup=delete_message())
        await BuyItem.shipping_address.set()
    else:
        message = await m.answer('✏️ Введите верное количество товара', reply_markup=delete_message())
    async with state.proxy() as data:
        data['amount'] = m.text
        msg = data['msg']
        data['msg'] = message.message_id
    await m.bot.edit_message_reply_markup(chat_id=m.chat.id, message_id=msg)


async def get_address(m: Message, state: FSMContext):
    message = await m.answer('❗️ Выберите удобный способ оплаты', reply_markup=payment_methods())
    await BuyItem.payment.set()
    async with state.proxy() as data:
        data['address'] = m.text
        msg = data['msg']
        data['msg'] = message.message_id
    await m.bot.edit_message_reply_markup(chat_id=m.chat.id, message_id=msg)


async def card_payment(c: CallbackQuery, state: FSMContext, user: User):
    async with state.proxy() as data:
        item_id = int(data['item_id'])
        amount = int(data['amount'])
        address = data['address']
    config = load_config()
    item = await get_item(session=c.bot['db'](), item_id=item_id)
    pay_amount = item.price * amount - user.balance
    if user.balance >= item.price*amount:
        await state.finish()
        await user.update_user(session=c.bot['db'](), updated_fields={'balance': user.balance - item.price*amount})
        return await c.message.edit_text(f'🛍 Поздравляем с покупкой!\n'
                                         f'Ожидайте доставки по адресу {address}\n'
                                         f'Покупка была совершена с помощью баланса в боте.')
    async with QiwiWrapper(secret_p2p=config.tg_bot.secret) as w:
        row = await w.create_p2p_bill(amount=pay_amount,
                                      comment=f'{item.name} | {pay_amount} RUB')
    await c.message.edit_text(f'Вы выбрали пополнение <b>Киви/Карта</b> \n'
                              f'<b>Сумма оплаты:</b> {pay_amount} руб.\n\n'
                              f'Чтобы отказаться - нажмите <b>«Назад»</b>',
                              reply_markup=pay_card(url=row.pay_url, bill_id=row.bill_id))


async def check_payment(c: CallbackQuery, callback_data: dict, state: FSMContext, user: User):
    async with state.proxy() as data:
        address = data['address']
    bill_id = callback_data['bill_id']
    config = load_config()
    async with QiwiWrapper(secret_p2p=config.tg_bot.secret) as w:
        status = await w.check_p2p_bill_status(bill_id=bill_id)
    if status != 'PAID':
        return await c.answer('Оплата не найдена', show_alert=True)
    await user.update_user(session=c.bot['db'](), updated_fields={'balance': user.balance-user.balance})
    await c.message.edit_text(f'🛍 Поздравляем с покупкой!\n'
                              f'Ожидайте доставки по адресу {address}')
    await state.finish()


def register_buy_item(dp: Dispatcher):
    dp.register_callback_query_handler(enter_amount, buy_call.filter())
    dp.register_message_handler(get_amount, state=BuyItem.amount)
    dp.register_message_handler(get_address, state=BuyItem.shipping_address)
    dp.register_callback_query_handler(card_payment, payment_call.filter(method='card'), state=BuyItem.payment)
    dp.register_callback_query_handler(check_payment, card_call.filter(), state=BuyItem.payment)
