from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["Items"])

items: dict = {
    1: {"name": "사과", "price": 1000, "is_available": True},
    2: {"name": "바나나", "price": 500, "is_available": True},
}


class Item(BaseModel):
    name: str
    price: float
    is_available: bool = True


class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    is_available: bool | None = None


@router.get("", summary="전체 아이템 목록 조회")
def get_items(
    available: bool | None = None,
    name: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort: str | None = None,
    skip: int = 0,
    limit: int = 10,
):
    result = dict(items)

    if available is not None:
        result = {k: v for k, v in result.items() if v["is_available"] == available}
    if name is not None:
        result = {k: v for k, v in result.items() if name in v["name"]}
    if min_price is not None:
        result = {k: v for k, v in result.items() if v["price"] >= min_price}
    if max_price is not None:
        result = {k: v for k, v in result.items() if v["price"] <= max_price}

    sorted_items = sorted(result.items(), key=lambda x: (
        x[1]["price"] if sort == "price_asc" else
        -x[1]["price"] if sort == "price_desc" else
        x[0]
    ))

    return dict(sorted_items[skip: skip + limit])


@router.get("/{item_id}", summary="특정 아이템 조회")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    return items[item_id]


@router.post("", summary="새 아이템 생성", status_code=201)
def create_item(item: Item):
    new_id = max(items.keys()) + 1
    items[new_id] = item.model_dump()
    return {"id": new_id, "item": items[new_id]}


@router.put("/{item_id}", summary="아이템 전체 수정")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    items[item_id] = item.model_dump()
    return {"id": item_id, "item": items[item_id]}


@router.patch("/{item_id}", summary="아이템 부분 수정")
def patch_item(item_id: int, item: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    stored = items[item_id]
    update_data = item.model_dump(exclude_unset=True)
    stored.update(update_data)
    return {"id": item_id, "item": stored}


@router.delete("/{item_id}", summary="아이템 삭제")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    deleted = items.pop(item_id)
    return {"message": "삭제 완료", "deleted_item": deleted}
