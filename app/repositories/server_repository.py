
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Server
from app.schemas import ServerCreate, ServerUpdate


def get_by_id(db: Session, server_id: int) -> Server | None:
    return db.get(Server, server_id)


def get_by_hostname(db: Session, hostname: str) -> Server | None:
    return db.scalar(
        select(Server).where(Server.hostname == hostname)
    )


def get_all(db: Session) -> list[Server]:
    return list(
        db.scalars(select(Server).order_by(Server.id)).all()
    )


def create(db: Session, data: ServerCreate) -> Server:
    server = Server(**data.model_dump())
    db.add(server)
    db.commit()
    db.refresh(server)
    return server


def update(
    db: Session,
    server: Server,
    data: ServerUpdate,
) -> Server:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(server, field, value)

    db.commit()
    db.refresh(server)
    return server


def delete(db: Session, server: Server) -> None:
    db.delete(server)
    db.commit()
