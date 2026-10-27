
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.services import server_service
from app.security import require_token

router = APIRouter(
    prefix="/servers",
    tags=["服务器管理"],
    dependencies=[Depends(require_token)],
)

DbSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=schemas.ServerOut,
    status_code=status.HTTP_201_CREATED,
)
def create_server(data: schemas.ServerCreate, db: DbSession):
    return server_service.create_server(db, data)


@router.get("", response_model=list[schemas.ServerOut])
def list_servers(db: DbSession):
    return server_service.list_servers(db)


@router.get("/{server_id}", response_model=schemas.ServerOut)
def get_server(server_id: int, db: DbSession):
    return server_service.get_server(db, server_id)


@router.patch("/{server_id}", response_model=schemas.ServerOut)
def update_server(
    server_id: int,
    data: schemas.ServerUpdate,
    db: DbSession,
):
    return server_service.update_server(db, server_id, data)


@router.delete(
    "/{server_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_server(server_id: int, db: DbSession):
    server_service.delete_server(db, server_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
