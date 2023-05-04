import sqlalchemy

from utils.db_api.db_gino import TimedBaseModel
from sqlalchemy import Column, BigInteger, String, sql


class User(TimedBaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    name = Column(String(50))
    age = Column(BigInteger)
    photo = Column(String(200))
    status = Column(String(20))

    query: sql.select

    def __repr__(self):
        return F"{self.user_id} {self.name}"
