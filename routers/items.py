from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from models import Item, ItemCreate, ItemUpdate

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("", summary="전체 아이템 목록 조회")
def get_items(
    available: bool | None = None,
    name: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
):
    query = select(Item)

    if available is not None:
        query = query.where(Item.is_available == available)
    if name is not None:
        query = query.where(Item.name.contains(name))
    if min_price is not None:
        query = query.where(Item.price >= min_price)
    if max_price is not None:
        query = query.where(Item.price <= max_price)

    return session.exec(query.offset(skip).limit(limit)).all()


@router.get("/{item_id}", summary="특정 아이템 조회")
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    return item


@router.post("", summary="새 아이템 생성", status_code=201)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.put("/{item_id}", summary="아이템 전체 수정")
def update_item(item_id: int, item: ItemCreate, session: Session = Depends(get_session)):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    db_item.sqlmodel_update(item.model_dump())
    session.commit()
    session.refresh(db_item)
    return db_item


@router.patch("/{item_id}", summary="아이템 부분 수정")
def patch_item(item_id: int, item: ItemUpdate, session: Session = Depends(get_session)):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    db_item.sqlmodel_update(item.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{item_id}", summary="아이템 삭제")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    session.delete(db_item)
    session.commit()
    return {"message": "삭제 완료", "deleted_item": db_item}
