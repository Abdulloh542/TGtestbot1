from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.models import Ticket, TicketMessage


async def create_ticket(session, user_id: int, message: str):
    ticket = Ticket(user_id=user_id)
    session.add(ticket)
    await session.flush()
    session.add(
        TicketMessage(ticket_id=ticket.id, sender_role="USER", message=message)
    )
    await session.commit()
    return ticket


async def add_ticket_message(session, ticket_id: int, sender_role: str, message: str):
    result = await session.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalars().first()
    if not ticket:
        return None
    session.add(
        TicketMessage(ticket_id=ticket.id, sender_role=sender_role, message=message)
    )
    await session.commit()
    return ticket


async def get_ticket(session, ticket_id: int):
    result = await session.execute(
        select(Ticket)
        .where(Ticket.id == ticket_id)
        .options(selectinload(Ticket.messages))
    )
    return result.scalars().first()
