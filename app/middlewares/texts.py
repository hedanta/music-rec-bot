from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware

from app.texts import Texts


class TextsMiddleware(BaseMiddleware):
    def __init__(self, texts: Texts) -> None:
        self._texts = texts

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        data["texts"] = self._texts
        return await handler(event, data)
