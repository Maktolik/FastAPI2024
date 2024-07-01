from typing import Annotated

from fastapi import APIRouter, Path

from users import crud
from users.schemas import CreateUser

router = APIRouter(prefix="/users")


@router.get("/latest/")
def users_latest():
    return {"users": {"id": 1, "username": "Animeinblood", "games": "dota"}}


@router.get("/{user_id}/")
def user_info(user_id: Annotated[int, Path(ge=0, lt=1000)]):
    return {
        "user": {"id": user_id},
    }


@router.post("/")
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)
