from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .post import Post


class User(Base):
    # __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(12), unique=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
