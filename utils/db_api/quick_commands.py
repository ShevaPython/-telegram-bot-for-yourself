# from datetime import datetime
#
# from utils.db_api.con_database import Session
# from utils.db_api.models import User
# from asyncpg import UniqueViolationError
#
# #
# # async def add_user(user_id):
# #     try:
# #         user = await User.query.where(User.user_id == user_id).gino.first()
# #         if not user:
# #             await User.create(user_id =user_id)
# #
# #     except UniqueViolationError as err:
# #         print(F'пользователь не добавлен ошибка {err}')
# #
# #
# # async def select_all_users():
# #     users = await User.query.gino.all()
# #     return users
# #
# #
# # async def count_all_users():
# #     count_users = await db.func.count(User.user_id).gino.scalar()
# #     return count_users
# #
# #
# # async def select_user(user_id):
# #     user = await User.query.where(User.user_id == user_id).gino.first()
# #     return user
# #
# #
# # async def update_user_data(user_id, state):
# #     user = await User.query.where(User.user_id == user_id).gino.first()
# #     async with state.proxy() as data:
# #         await user.update(
# #                           name=data['name'],
# #                           age=data['age'],
# #                           photo=data['photo'],
# #                           status=data['status']).apply()
#
#
#
# async def get_user(user_id: int) -> User:
#     async with Session() as session:
#         return await session.get(User, user_id)
#
#
# async def create_user(user_id: int, name: str, age: int, photo: str) -> User:
#     async with Session() as session:
#         user = User(user_id=user_id, name=name, age=age, photo=photo)
#         session.add(user)
#         await session.commit()
#         return user
#
#
# async def update_user(user_id: int, name: str = None, age: int = None, photo: str = None) -> User:
#     async with Session() as session:
#         user = await session.get(User, user_id)
#         if name is not None:
#             user.name = name
#         if age is not None:
#             user.age = age
#         if photo is not None:
#             user.photo = photo
#         user.update_at = datetime.datetime.now()
#         await session.commit()
#         return user
#
#
# async def delete_user(user_id: int):
#     async with Session() as session:
#         user = await session.get(User, user_id)
#         session.delete(user)
#         await session.commit()