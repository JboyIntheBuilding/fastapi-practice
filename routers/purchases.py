from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from models import Purchase, PurchaseCreate, Player, GameItem

router = APIRouter(prefix="/purchases", tags=["Purchases"])


@router.get("", summary="전체 구매 내역 조회")
def get_purchases(player_id: int | None = None, session: Session = Depends(get_session)):
    query = select(Purchase)
    if player_id is not None:
        query = query.where(Purchase.player_id == player_id)
    return session.exec(query).all()


@router.post("", summary="아이템 구매", status_code=201)
def purchase_item(purchase: PurchaseCreate, session: Session = Depends(get_session)):
    player = session.get(Player, purchase.player_id)
    if not player:
        raise HTTPException(status_code=404, detail="플레이어를 찾을 수 없습니다")

    item = session.get(GameItem, purchase.item_id)
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")

    if item.stock < purchase.quantity:
        raise HTTPException(status_code=400, detail=f"재고 부족 (현재 재고: {item.stock})")

    total_price = item.price * purchase.quantity
    if player.gold < total_price:
        raise HTTPException(status_code=400, detail=f"골드 부족 (필요: {total_price}, 보유: {player.gold})")

    player.gold -= total_price
    item.stock -= purchase.quantity

    db_purchase = Purchase(
        player_id=purchase.player_id,
        item_id=purchase.item_id,
        quantity=purchase.quantity,
        total_price=total_price,
    )
    session.add(db_purchase)
    session.commit()
    session.refresh(db_purchase)
    return {
        "purchase": db_purchase,
        "player_gold_remaining": player.gold,
    }
