if __name__ == "__main__":
    import sys

    sys.path.append(".")

import os
import random

import asyncpg
from asyncpg.connection import Connection
from seeddata import comments
from seeddata import items
from seeddata import users

from app.db.repositories.comments import CommentsRepository
from app.db.repositories.items import ItemsRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.services.authentication import check_email_is_taken
from app.services.authentication import check_username_is_taken
from app.services.items import check_item_exists
from app.services.items import get_slug_for_item


class SeedDataLoader:
    def __init__(self, conn: Connection):
        self.conn = conn
        self.users_repo = UsersRepository(conn)
        self.items_repo = ItemsRepository(conn)
        self.comments_repo = CommentsRepository(conn)

    async def run(self):
        await self.clear_data()
        await self.load_users()
        await self.load_items()
        await self.load_comments()

    async def clear_data(self):
        await self.conn.execute(
            """
            DELETE
            FROM users
            WHERE email != 'danesolberg@gmail.com'
        """
        )
        await self.conn.execute(
            """
            DELETE
            FROM items
        """
        )
        await self.conn.execute(
            """
            DELETE
            FROM comments
        """
        )

    async def user_exists(self, user: dict) -> bool:
        return await check_username_is_taken(
            self.users_repo, user["username"]
        ) or await check_email_is_taken(self.users_repo, user["email"])

    async def make_user_unique(self, user: dict) -> None:
        while await self.user_exists(user):
            user["username"] += "x"
            user["email"] += "x"

    async def make_item_unique(self, item: dict) -> None:
        slug = get_slug_for_item(item["title"])
        while await check_item_exists(self.items_repo, slug):
            item["title"] += "x"
            slug = get_slug_for_item(item["title"])

    async def load_users(self):
        for user in users:
            await self.make_user_unique(user)
            await self.users_repo.create_user(**user)

    async def load_items(self):
        for item in items:
            await self.make_item_unique(item)
            slug = get_slug_for_item(item["title"])
            await self.items_repo.create_item(
                **item, slug=slug, seller=User(**random.choice(users))
            )

    async def load_comments(self):
        for comment in comments:
            item_data = random.choice(items)
            item_slug = get_slug_for_item(item_data["title"])
            item_object = await self.items_repo.get_item_by_slug(slug=item_slug)
            await self.comments_repo.create_comment_for_item(
                body=comment["body"],
                item=item_object,
                user=User(**random.choice(users)),
            )


async def main():
    database_url = os.environ["DATABASE_URL"].replace("postgres://", "postgresql://")
    conn = await asyncpg.connect(str(database_url))
    loader = SeedDataLoader(conn)
    await loader.run()


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
