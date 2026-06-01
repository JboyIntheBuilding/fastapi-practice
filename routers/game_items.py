from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from models import GameItem, GameItemCreate, GameItemUpdate, ItemType

router = APIRouter(prefix="/game-items", tags=["GameItems"])


@router.get("", summary="전체 아이템 조회")
def get_items(
    type: ItemType | None = None,
    max_price: int | None = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    query = select(GameItem)
    if type is not None:
        query = query.where(GameItem.type == type)
    if max_price is not None:
        query = query.where(GameItem.price <= max_price)
    return session.exec(query.offset(skip).limit(limit)).all()


@router.get("/{item_id}", summary="특정 아이템 조회")
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(GameItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    return item


@router.post("", summary="아이템 등록", status_code=201)
def create_item(item: GameItemCreate, session: Session = Depends(get_session)):
    db_item = GameItem.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.patch("/{item_id}", summary="아이템 수정")
def patch_item(item_id: int, item: GameItemUpdate, session: Session = Depends(get_session)):
    db_item = session.get(GameItem, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    db_item.sqlmodel_update(item.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{item_id}", summary="아이템 삭제")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    db_item = session.get(GameItem, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    session.delete(db_item)
    session.commit()
    return {"message": "삭제 완료", "deleted_item": db_item}
