from datetime import datetime

from aiogram.dispatcher import FSMContext
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from utils.db_api.models import User

class UserCommand:
    """Команды для управления таблицей юзер CRUD"""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, user_id: int) -> User:
        try:
            return await self.session.get(User, user_id)
        except SQLAlchemyError as e:
            print(f"Ошибка при получении пользователя: {e}")
            raise

    async def create_user(self, user_id: int, state: FSMContext):
        try:
            async with state.proxy() as data:
                new_user = User(
                    user_id=user_id,
                    name=data['name'],
                    age=data['age'],
                    photo=data['photo'],
                    status=data['status']
                )

                self.session.add(new_user)
                await self.session.commit()
        except SQLAlchemyError as e:
            print(f"Ошибка при создании пользователя: {e}")
            await self.session.rollback()
            raise

    async def update_user(self, user_id: int, name: str = None, age: int = None, photo: str = None) -> User:
        try:
            user = await self.session.get(User, user_id)
            if name is not None:
                user.name = name
            if age is not None:
                user.age = age
            if photo is not None:
                user.photo = photo
            user.updated_at = datetime.now()
            await self.session.commit()
            return user
        except SQLAlchemyError as e:
            print(f"Ошибка при обновлении пользователя: {e}")
            await self.session.rollback()
            raise

    async def delete_user(self, user_id: int):
        try:
            user = await self.session.get(User, user_id)
            self.session.delete(user)
            await self.session.commit()
        except SQLAlchemyError as e:
            print(f"Ошибка при удалении пользователя: {e}")
            await self.session.rollback()
            raise


#
# class UserCommand:
#     """Команды для управления таблицей юзер CRUD"""
#     def __init__(self, session: AsyncSession):
#         self.session = session
#
#     async def get_user(self, user_id: int) -> User:
#         try:
#             async with async_session() as session:
#                 return await session.get(User, user_id)
#         except SQLAlchemyError as e:
#             print(f"Ошибка при получении пользователя: {e}")
#             raise
#
#     async def create_user(self, user_id: int, state: FSMContext):
#         try:
#             async with async_session() as session:
#                 async with state.proxy() as data:
#                     new_user = User(
#                         user_id=user_id,
#                         name=data['name'],
#                         age=data['age'],
#                         photo=data['photo'],
#                         status=data['status']
#                     )
#
#                     session.add(new_user)
#                     await session.commit()
#         except SQLAlchemyError as e:
#             print(f"Ошибка при создании пользователя: {e}")
#             await session.rollback()
#             raise
#
#     async def update_user(self, user_id: int, name: str = None, age: int = None, photo: str = None) -> User:
#         try:
#             async with async_session() as session:
#                 user = await session.get(User, user_id)
#                 if name is not None:
#                     user.name = name
#                 if age is not None:
#                     user.age = age
#                 if photo is not None:
#                     user.photo = photo
#                 user.updated_at = datetime.now()
#                 await session.commit()
#                 return user
#         except SQLAlchemyError as e:
#             print(f"Ошибка при обновлении пользователя: {e}")
#             await session.rollback()
#             raise
#
#     async def delete_user(self, user_id: int):
#         try:
#             async with async_session() as session:
#                 user = await session.get(User, user_id)
#                 session.delete(user)
#                 await session.commit()
#         except SQLAlchemyError as e:
#             print(f"Ошибка при удалении пользователя: {e}")
#             await session.rollback()
#             raise


__all__ = ['UserCommand']
