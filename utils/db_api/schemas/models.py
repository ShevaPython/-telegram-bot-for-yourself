import datetime
import sqlalchemy as sa
from sqlalchemy import Column, BigInteger, String, ForeignKey, FLOAT, TEXT, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User( Base ):
    __tablename__ = 'users'

    user_id = Column( BigInteger, primary_key=True )
    name = Column( String( 50 ) )
    age = Column( BigInteger )
    photo = Column( TEXT )
    status = Column( String( 20 ), default='unregister' )
    create_at = Column( sa.DateTime, server_default=func.now() )
    update_at = Column( sa.DateTime, server_default=func.now(), onupdate=datetime.datetime.now() )

    wallets = relationship( 'Wallet', uselist=False, back_populates='owner' )

    __table_args__ = (
        UniqueConstraint( 'photo' ),
    )

    def __repr__(self):
        return F"ID:{self.user_id},Name:{self.name}"


class Wallet( Base ):
    __tablename__ = 'wallets'

    id = Column( BigInteger, prinary_key=True )
    owner_id = Column( BigInteger, ForeignKey( 'users.user_id' ) )
    balance = Column( FLOAT, default=0 )
    owner = relationship( 'User', back_populates='wallet' )


class Transaction( Base ):
    __tablemane__ = 'transactions'
    id = Column( BigInteger, primary_key=True )
    wallet_id = Column( BigInteger, ForeignKey( 'wallets.id' ) )
    amount = Column( FLOAT )
    timestamp = Column( sa.DateTime, server_default=func.now() )
    wallet = relationship( 'Wallet', back_populates='transactions' )
