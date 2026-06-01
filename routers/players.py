from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from models import Player, PlayerCreate, PlayerUpdate

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("", summary="전체 플레이어 조회")
def get_players(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return session.exec(select(Player).offset(skip).limit(limit)).all()


@router.get("/{player_id}", summary="특정 플레이어 조회")
def get_player(player_id: int, session: Session = Depends(get_session)):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="플레이어를 찾을 수 없습니다")
    return player


@router.post("", summary="플레이어 생성", status_code=201)
def create_player(player: PlayerCreate, session: Session = Depends(get_session)):
    db_player = Player.model_validate(player)
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player


@router.patch("/{player_id}", summary="플레이어 정보 수정")
def patch_player(player_id: int, player: PlayerUpdate, session: Session = Depends(get_session)):
    db_player = session.get(Player, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="플레이어를 찾을 수 없습니다")
    db_player.sqlmodel_update(player.model_dump(exclude_unset=True))
    session.commit()
    session.refresh(db_player)
    return db_player


@router.delete("/{player_id}", summary="플레이어 삭제")
def delete_player(player_id: int, session: Session = Depends(get_session)):
    db_player = session.get(Player, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="플레이어를 찾을 수 없습니다")
    session.delete(db_player)
    session.commit()
    return {"message": "삭제 완료", "deleted_player": db_player}
