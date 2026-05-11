from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# DB 대신 메모리(딕셔너리)에 데이터 저장
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


# GET - 전체 목록 조회
# Query 파라미터: /items?available=true&max_price=1000
@app.get("/items", summary="전체 아이템 목록 조회")
def get_items(available: bool | None = None, max_price: float | None = None):
    result = items
    if available is not None:
        result = {k: v for k, v in result.items() if v["is_available"] == available}
    if max_price is not None:
        result = {k: v for k, v in result.items() if v["price"] <= max_price}
    return result


# GET - 특정 아이템 조회
@app.get("/items/{item_id}", summary="특정 아이템 조회")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    return items[item_id]


# POST - 새 아이템 생성
@app.post("/items", summary="새 아이템 생성")
def create_item(item: Item):
    new_id = max(items.keys()) + 1
    items[new_id] = item.model_dump()
    return {"id": new_id, "item": items[new_id]}


# PUT - 아이템 전체 수정 (모든 필드를 다 보내야 함)
@app.put("/items/{item_id}", summary="아이템 전체 수정")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    items[item_id] = item.model_dump()
    return {"id": item_id, "item": items[item_id]}


# PATCH - 아이템 일부 수정 (바꿀 필드만 보내도 됨)
@app.patch("/items/{item_id}", summary="아이템 부분 수정")
def patch_item(item_id: int, item: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    stored = items[item_id]
    update_data = item.model_dump(exclude_unset=True)
    stored.update(update_data)
    return {"id": item_id, "item": stored}


# DELETE - 아이템 삭제
@app.delete("/items/{item_id}", summary="아이템 삭제")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    deleted = items.pop(item_id)
    return {"message": "삭제 완료", "deleted_item": deleted}
