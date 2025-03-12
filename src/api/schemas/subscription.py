import asyncio
from typing import AsyncGenerator

import strawberry


@strawberry.type
class TestingSubscription:

    @strawberry.subscription()
    async def get_count(self, target: int = 50) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(2)
