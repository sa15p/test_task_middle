from sqlalchemy import select, update

from database import new_session, BetOrm
from schemas import BetAdd, Bet, BetUpdate


class BetRepository:
    @classmethod
    async def add_one(cls, data: BetAdd) -> int:
        async with new_session() as session:
            bet_dict = data.model_dump()

            bet = BetOrm(**bet_dict)
            print(bet_dict)
            session.add(bet)
            await session.flush()
            await session.commit()
            return bet.id

    @classmethod
    async def find_all(cls) -> list[Bet]:
        async with new_session() as session:
            query = select(BetOrm)
            result = await session.execute(query)
            bet_models = result.scalars().all()
            bet_schemas = [Bet.model_validate(bet_model) for bet_model in bet_models]
            return bet_schemas

    @classmethod
    async def outcome_by_id(cls, data: BetUpdate) -> bool:
        async with new_session() as session:
            query = select(BetOrm).filter(BetOrm.event_id == data.event_id)
            result = await session.execute(query)
            bet_model = result.scalars().first()

            if not bet_model:
                raise ValueError(f"Bet with id {data.event_id} not found")

            bet_model.final = data.final

            update_query = update(BetOrm).where(BetOrm.event_id == data.event_id).values(final=data.final)
            await session.execute(update_query)
            await session.flush()
            await session.commit()

            return True
