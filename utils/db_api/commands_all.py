import calendar

from sqlalchemy import func
from datetime import datetime
from typing import List

from sqlalchemy import select

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from utils.db_api.models import User, Wallet, Transaction


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

    async def create_user(self, user_id: int, name: str, age: int, photo: str, status: str):
        try:
            new_user = User(
                user_id=user_id,
                name=name,
                age=age,
                photo=photo,
                status=status
            )
            wallet = Wallet(owner_id=new_user.user_id)
            new_user.wallet = wallet
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

    async def get_user_balance(self, user_id: int) -> float:
        try:
            user = await self.session.get(User, user_id)

            if user and user.wallet:
                user_balance = user.wallet
                return user_balance.balance

            return 0  # Если пользователя или кошелька нет, возвращаем 0
        except SQLAlchemyError as e:
            print(f"Ошибка при получении баланса пользователя: {e}")
            raise

    async def update_user_balance(self, user_id: int, value: int) -> float:
        try:
            user = await self.session.get(User, user_id)
            if user and user.wallet:
                user.wallet.balance += float(value)
                await self.session.commit()
                return user.wallet.balance
            return 0

        except SQLAlchemyError as e:
            print(f"Ошибка при пополнении баланса пользователя: {e}")
            raise


class WalletCommands:
    """Взаимодействие с кошельком и транзакциями"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_wallet_balance(self, owner_id: int, amount: float) -> float:
        try:
            wallet = await self.session.execute(select(Wallet).filter(Wallet.owner_id == owner_id))
            row = wallet.scalar_one_or_none()

            if row:
                row.balance += amount
                await self.session.commit()
                return row.balance

            return 0

        except SQLAlchemyError as e:
            print(f"Ошибка при обновлении баланса кошелька: {e}")
            await self.session.rollback()
            raise

    async def create_transaction(self, wallet_id: int, amount: float) -> Transaction:
        try:
            transaction = Transaction(wallet_id=wallet_id, amount=amount)
            self.session.add(transaction)
            await self.session.commit()
            return transaction
        except SQLAlchemyError as e:
            print(f"Ошибка при создании транзакции: {e}")
            await self.session.rollback()
            raise

    async def get_wallet(self, owner_id: int) -> Wallet:
        try:
            result = await self.session.execute(select(Wallet).filter(Wallet.owner_id == owner_id))
            row = result.fetchone()
            return row[0] if row else None
        except SQLAlchemyError as e:
            print(f"Ошибка при получении кошелька: {e}")


class TransactionCommands:
    def __init__(self, session):
        self.session = session

    async def get_transactions_by_month(self, wallet_id: int, month: str) -> List[Transaction]:
        try:
            # Разбираем входную строку с месяцем для получения месяца и года
            month_int, year_int = map(int, month.split('.'))

            # Вычисляем начальную и конечную даты месяца
            start_date = datetime(year_int, month_int, 1)
            end_date = start_date.replace(day=calendar.monthrange(year_int, month_int)[1], hour=23, minute=59,
                                          second=59)

            transactions = await self.session.execute(
                select(Transaction)
                .filter(Transaction.wallet_id == wallet_id)
                .filter(func.date_trunc('month', Transaction.timestamp) == start_date)
                .filter(Transaction.timestamp <= end_date)
                .options(selectinload(Transaction.wallet))
            )
            transactions = transactions.scalars().all()

            return transactions

        except SQLAlchemyError as e:
            print(f"Ошибка при получении транзакций за месяц: {e}")
            raise


__all__ = ['UserCommand', 'WalletCommands']
