

from typing import TYPE_CHECKING

from ..types.chats import Chats

from ..types.users import User

from ..enums.http_method import HTTPMethod
from ..enums.api_path import ApiPath

from ..connection.base import BaseConnection


if TYPE_CHECKING:
    from ..bot import Bot


class GetMe(BaseConnection):
    def __init__(self, bot: 'Bot'):
        self.bot = bot

    async def request(self) -> User:
        return await super().request(
            method=HTTPMethod.GET, 
            path=ApiPath.ME,
            model=User,
            params=self.bot.params
        )