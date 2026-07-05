from sqlalchemy import Column, Integer, ForeignKey, Float, String

from src.main.api.db.base import Base


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    number = Column(String, unique=True, nullable=False)
    balance = Column(Float, nullable=False)

    def __repr__(self):
        return "<Account(id={self.id}, user_id={self.user_id}, number={self.number}, balance={self.balance})>"