import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, ForeignKey, Float, Text, UniqueConstraint,LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True,nullable=False)
    name = Column(String(50),nullable=False)
    age = Column(BigInteger,nullable=False)
    photo = Column(Text, nullable=False)
    status = Column(String(20), default='unregister')
    create_at = Column(sa.DateTime, server_default=func.now())
    updated_at= Column(sa.DateTime, server_default=func.now(), onupdate=datetime.datetime.now())

    wallet = relationship('Wallet', uselist=False, back_populates='owner',lazy="joined")

    __table_args__ = (
        UniqueConstraint('photo'),
    )

    def __str__(self):
        return f"ID:{self.user_id}, Name:{self.name}"


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(BigInteger, primary_key=True,nullable=False)
    owner_id = Column(BigInteger, ForeignKey('users.user_id',ondelete='CASCADE'),nullable=False)
    balance = Column(Float, default=0)
    owner = relationship('User', back_populates='wallet',lazy='joined')

    transactions = relationship('Transaction', back_populates='wallet',lazy='selectin')

    def __str__(self):
        return F"ID: {self.id}"


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(BigInteger, primary_key=True)
    wallet_id = Column(BigInteger, ForeignKey('wallets.id',ondelete='CASCADE'),nullable=False)
    amount = Column(Float)
    timestamp = Column(sa.DateTime, server_default=func.now())

    wallet = relationship('Wallet', back_populates='transactions')


