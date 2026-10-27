
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    hostname: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    ip: Mapped[str] = mapped_column(String(45))
    cpu_cores: Mapped[int] = mapped_column(Integer)
    memory_gb: Mapped[int] = mapped_column(Integer)
