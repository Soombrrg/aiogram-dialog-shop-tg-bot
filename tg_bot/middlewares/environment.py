from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from tg_bot.db.db_repo import Repo


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker, repo: Repo) -> None:
        super().__init__()
        self.session_pool = session_pool
        self.repo = repo
        self.skip_patterns = ["error", "update"]

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
        *args
    ) -> Any:
        if event.event_type in self.skip_patterns:
            return await handler(event, data)
        async with self.session_pool() as session:
            data.update(session=session, repo=self.repo)
            return await handler(event, data)
