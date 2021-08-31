from aiogram.dispatcher.filters import BoundFilter

from tgbot.models.users import User


class IsAdmin(BoundFilter):
    async def check(self, obj) -> bool:
        """
        Фильтр для проверки на администратора
        :return: Boolean
        """
        row = await User.get_user(chat_id=obj.from_user,
                                  session=obj.bot['db']())
        return row.admin
