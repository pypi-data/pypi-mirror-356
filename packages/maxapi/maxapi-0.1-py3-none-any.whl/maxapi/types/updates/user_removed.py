from typing import TYPE_CHECKING, Any, Optional

from pydantic import Field

from .update import Update
from ...types.users import User

if TYPE_CHECKING:
    from ...bot import Bot


class UserRemoved(Update):
    admin_id: Optional[int] = None
    chat_id: Optional[int] = None
    user: User
    bot: Optional[Any] = Field(default=None, exclude=True)
    
    if TYPE_CHECKING:
        bot: Optional[Bot]

    def get_ids(self):
        return (self.chat_id, self.admin_id)