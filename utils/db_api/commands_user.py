from datetime import datetime

from loader import async_session
from utils.db_api.models import User




async def get_user(user_id: int) -> User:
    async with async_session() as session:
        return await session.get(User, user_id)


async def create_user(user_id: int, name: str, age: int, photo: str) -> User:
    async with async_session()as session:
        user = User(user_id=user_id, name=name, age=age, photo=photo)
        session.add(user)
        await session.commit()
        return user


async def update_user(user_id: int, name: str = None, age: int = None, photo: str = None) -> User:
    async with async_session() as session:
        user = await session.get(User, user_id)
        if name is not None:
            user.name = name
        if age is not None:
            user.age = age
        if photo is not None:
            user.photo = photo
        user.update_at = datetime.now()
        await session.commit()
        return user


async def delete_user(user_id: int):
    async with async_session() as session:
        user = await session.get(User, user_id)
        session.delete(user)
        await session.commit()

__all__ = ['delete_user','create_user','update_user','get_user']