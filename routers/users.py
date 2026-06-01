from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from models import User, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", summary="전체 유저 목록 조회")
def get_users(
    is_active: bool | None = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    query = select(User)

    if is_active is not None:
        query = query.where(User.is_active == is_active)

    return session.exec(query.offset(skip).limit(limit)).all()


@router.get("/{user_id}", summary="특정 유저 조회")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다")
    return user


@router.post("", summary="새 유저 생성", status_code=201)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.put("/{user_id}", summary="유저 전체 수정")
def update_user(user_id: int, user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다")
    db_user.sqlmodel_update(user.model_dump())
    session.commit()
    session.refresh(db_user)
    return db_user


@router.patch("/{user_id}", summary="유저 부분 수정")
def patch_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다")
    db_user.sqlmodel_update(user.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}", summary="유저 삭제")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다")
    session.delete(db_user)
    session.commit()
    return {"message": "삭제 완료", "deleted_user": db_user}
