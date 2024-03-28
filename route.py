from typing import Annotated

from fastapi import APIRouter, Depends

from repository import BetRepository
from schemas import BetAdd, Bet, BetAdd, BetID, BetUpdate

router = APIRouter(
    prefix="/bets",
    tags=["Bets"],
)
outcomerouter = APIRouter(
    prefix="/events",
    tags=["OutcomeBets"]
)


@router.post("")
async def add_bets(
        bet: Annotated[BetAdd, Depends()],
) -> BetID:
    bet_id = await BetRepository.add_one(bet)
    return BetID.model_validate({"ok": True, "task_id": bet_id})


@router.get("")
async def get_bets() -> list[Bet]:
    bets = await BetRepository.find_all()
    return bets


@outcomerouter.put("/{event_id}")
async def update_task(event_id: Annotated[BetUpdate, Depends()]) -> bool:
    outcome = await BetRepository.outcome_by_id(event_id)
    return outcome
