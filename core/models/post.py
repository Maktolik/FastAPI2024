from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Post(UserRelationMixin, Base):
    # _user_id_unique = False
    # _user_id_nullable = False
    _user_back_populates = "posts"
    # __tablename__ = "posts"
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r}, user = {self.user.id})"

    def __repr__(self) -> str:
        return str(self)
