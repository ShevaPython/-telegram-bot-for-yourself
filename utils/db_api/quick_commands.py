from utils.db_api.db_gino import db
from utils.db_api.schemas.models import User
from asyncpg import UniqueViolationError


async def add_user(user_id):
    try:
        user = await User.query.where(User.user_id == user_id).gino.first()
        if not user:
            await User.create(user_id =user_id)

    except UniqueViolationError as err:
        print(F'пользователь не добавлен ошибка {err}')


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def count_all_users():
    count_users = await db.func.count(User.user_id).gino.scalar()
    return count_users


async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def update_user_data(user_id, state):
    user = await User.query.where(User.user_id == user_id).gino.first()
    async with state.proxy() as data:
        await user.update(
                          name=data['name'],
                          age=data['age'],
                          photo=data['photo'],
                          status=data['status']).apply()
