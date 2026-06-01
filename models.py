from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field


class ItemType(str, Enum):
    weapon = "weapon"
    armor = "armor"
    potion = "potion"


class Player(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(min_length=2, max_length=20, description="플레이어 이름")
    level: int = Field(default=1, ge=1, description="레벨")
    gold: int = Field(default=500, ge=0, description="보유 골드")


class PlayerCreate(SQLModel):
    username: str = Field(min_length=2, max_length=20, description="플레이어 이름")
    level: int = Field(default=1, ge=1, description="레벨")
    gold: int = Field(default=500, ge=0, description="보유 골드")


class PlayerUpdate(SQLModel):
    username: str | None = Field(default=None, min_length=2, max_length=20)
    level: int | None = Field(default=None, ge=1)
    gold: int | None = Field(default=None, ge=0)


class GameItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=50, description="아이템 이름")
    type: ItemType = Field(description="아이템 종류: weapon / armor / potion")
    power: int = Field(ge=0, description="아이템 능력치")
    price: int = Field(gt=0, description="가격 (골드)")
    stock: int = Field(default=0, ge=0, description="재고")


class GameItemCreate(SQLModel):
    name: str = Field(min_length=1, max_length=50, description="아이템 이름")
    type: ItemType = Field(description="아이템 종류: weapon / armor / potion")
    power: int = Field(ge=0, description="아이템 능력치")
    price: int = Field(gt=0, description="가격 (골드)")
    stock: int = Field(default=0, ge=0, description="재고")


class GameItemUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    type: ItemType | None = Field(default=None)
    power: int | None = Field(default=None, ge=0)
    price: int | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)


class Purchase(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="player.id", description="구매한 플레이어 ID")
    item_id: int = Field(foreign_key="gameitem.id", description="구매한 아이템 ID")
    quantity: int = Field(default=1, gt=0, description="구매 수량")
    total_price: int = Field(gt=0, description="총 결제 골드")
    purchased_at: datetime = Field(default_factory=datetime.now, description="구매 시각")


class PurchaseCreate(SQLModel):
    player_id: int = Field(description="구매한 플레이어 ID")
    item_id: int = Field(description="구매한 아이템 ID")
    quantity: int = Field(default=1, gt=0, description="구매 수량")
