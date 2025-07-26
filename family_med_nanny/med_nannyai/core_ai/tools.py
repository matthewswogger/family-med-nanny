from typing import Any
from datetime import date
from pydantic_ai import RunContext, Tool

from .data_models import SessionDependencies
from med_nannyai.medication_journal import MedicationJournal, Medication


# understand which user's journal to use

async def add_a_medication(
        ctx: RunContext[SessionDependencies],
        name: str,
        frequency: str,
        start_date: date,
        end_date: date | None,
        number_of_refills: int | None,
        refills_expire_at: date | None,
        notes: str | None
    ) -> Medication | None:
    """
    Add a medication to a user's journal
    """
    medication = Medication(
        name=name,
        frequency=frequency,
        start_date=start_date,
        end_date=end_date,
        number_of_refills=number_of_refills,
        refills_expire_at=refills_expire_at,
        notes=notes
    )
    ctx.deps.journal.add_medication(ctx.deps.user_id, medication)
    return medication

async def get_a_medication(
        ctx: RunContext[SessionDependencies],
        name: str
    ) -> Medication | None:
    """
    Get a medication from a user's journal
    """
    return ctx.deps.journal.get_medication(ctx.deps.user_id, name)

async def modify_a_medication(
        ctx: RunContext[SessionDependencies],
        **kwargs: Any
    ) -> Medication | None:
    """
    Modify a medication in a user's journal
    """
    pass

async def get_all_medications(
        ctx: RunContext[SessionDependencies]
    ) -> MedicationJournal:
    """
    Get all medications in a user's journal
    """
    return ctx.deps.journal.get_journal(ctx.deps.user_id)

async def get_all_medication_names(
        ctx: RunContext[SessionDependencies]
    ) -> list[str]:
    """
    Get all medication names in a user's journal
    """
    return list(ctx.deps.journal.get_journal(ctx.deps.user_id).medications.keys())

tools = [
    Tool(add_a_medication, takes_ctx=True),
    Tool(get_a_medication, takes_ctx=True),
    # Tool(modify_a_medication, takes_ctx=True),
    Tool(get_all_medications, takes_ctx=True),
    Tool(get_all_medication_names, takes_ctx=True),
]
