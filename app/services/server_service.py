
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import schemas
from app.repositories import server_repository as repo


def create_server(
    db: Session,
    data: schemas.ServerCreate,
):
    if repo.get_by_hostname(db, data.hostname) is not None:
        raise HTTPException(
            status_code=409,
            detail="主机名已存在",
        )

    try:
        return repo.create(db, data)
    except IntegrityError:
        # 处理并发请求导致的唯一约束冲突
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="主机名已存在",
        )


def list_servers(db: Session):
    return repo.get_all(db)


def get_server(db: Session, server_id: int):
    server = repo.get_by_id(db, server_id)

    if server is None:
        raise HTTPException(
            status_code=404,
            detail="服务器不存在",
        )

    return server


def update_server(
    db: Session,
    server_id: int,
    data: schemas.ServerUpdate,
):
    server = repo.get_by_id(db, server_id)

    if server is None:
        raise HTTPException(
            status_code=404,
            detail="服务器不存在",
        )

    try:
        return repo.update(db, server, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="更新失败，数据与现有记录冲突",
        )


def delete_server(db: Session, server_id: int):
    server = repo.get_by_id(db, server_id)

    if server is None:
        raise HTTPException(
            status_code=404,
            detail="服务器不存在",
        )

    repo.delete(db, server)
