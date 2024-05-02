from typing import Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

"""
RefreshToken 저장용 별도 테이블.
"""
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="refresh_token", lazy='joined')

"""
user모델 베이스
mysql등 DB에 이이 user테이블이 있는 경우가 있기에 만에 하나를 대비해서 users로 네이밍
"""
class User(Base):
    __tablename__ = "users" #db에 이미 user 테이블이 있음. 그래서 users로 변경
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(200), index=True)
    password: Mapped[str] = mapped_column(String(512)) # hash된 비밀번호. 얼마나 길어질지 모름.
    salt: Mapped[str] = mapped_column(String(100)) # 비밀번호 hash용 salt. 별도 테이블로 빼는게 좋을수도 있음
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
    deleted_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True) # soft delete도 그렇고 있는 편이 나중에 편함.

    UniqueConstraint('username', 'deleted_at', name='unique_username') # username와 deleted_at는 사실상 세트로 봐야 함. active면 deleted_at는 null상태. 탈퇴했으면 deleted_at에 값 있음.

    refresh_token = relationship("RefreshToken", back_populates="user")

    # 비즈니스 로직. 도메인 모델 패턴 지향.
    def update_username(self, username: str):
        self.username = username

    def update_password(self, password: str):
        self.password = password

    def update_deleted_at(self, date:Optional[DateTime] = func.now()):
        self.deleted_at = date