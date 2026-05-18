from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

users: dict = {
    1: {"username": "alice", "email": "alice@example.com", "is_active": True},
    2: {"username": "bob", "email": "bob@example.com", "is_active": True},
}


class User(BaseModel):
    username: str
    email: str
    is_active: bool = True


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    is_active: bool | None = None


@router.get("", summary="전체 유저 목록 조회")
def get_users(is_active: bool | None = None, skip: int = 0, limit: int = 10):
    result = dict(users)

    if is_active is not None:
        result = {k: v for k, v in result.items() if v["is_active"] == is_active}

    return dict(list(result.items())[skip: skip + limit])


@router.get("/{user_id}", summary="특정 유저 조회")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다")
    return users[user_id]


@router.post("", summary="새 유저 생성", status_code=201)
def create_user(user: User):
    new_id = max(users.keys()) + 1
    users[new_id] = user.model_dump()
    return {"id": new_id, "user": users[new_id]}


@router.put("/{user_id}", summary="유저 전체 수정")
def update_user(user_id: int, user: User):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다")
    users[user_id] = user.model_dump()
    return {"id": user_id, "user": users[user_id]}


@router.patch("/{user_id}", summary="유저 부분 수정")
def patch_user(user_id: int, user: UserUpdate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다")
    stored = users[user_id]
    update_data = user.model_dump(exclude_unset=True)
    stored.update(update_data)
    return {"id": user_id, "user": stored}


@router.delete("/{user_id}", summary="유저 삭제")
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다")
    deleted = users.pop(user_id)
    return {"message": "삭제 완료", "deleted_user": deleted}
