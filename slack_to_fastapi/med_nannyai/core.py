from datetime import date#, datetime
from dataclasses import dataclass
from pydantic import Field
from pydantic_ai import Agent, RunContext, ImageUrl
import logfire

from .medication_journal import MedicationJournal, MedicationJournalEntry
from .prescription_extraction import read_label_medication_bottle


logfire.configure()
logfire.instrument_pydantic_ai()
logfire.instrument_httpx(capture_all=True)


class MedNannyAI:
    def __init__(self):
        pass

    def craft_message(self, event, context):
        pass

    def send_message(self, message, channel_id):
        pass

########################################################################
# Data Models
########################################################################

@dataclass
class SlackUserIdentification:
    user_id: int = Field(description="The user's id")
    user_name: str = Field(description="The user's name")

@dataclass
class SessionDependencies:
    medication_journal: MedicationJournal
    user_info: SlackUserIdentification = Field(
        description='The user\'s information'
    )
    todays_date: date = date.today()


########################################################################
# Agent
########################################################################

agent = Agent(
    model='openai:gpt-4.1-mini',
    # model='openai:gpt-4o',
    deps_type=SessionDependencies,
    output_type=str,
)

########################################################################
# Instructions
########################################################################

medication_assistant_general_instructions = """\
You're an assistant to help a family manage their medications.
This means that at least one of the family members has a very complex medication regimen.
This also usually means that the other family members are acting as
caregivers for the person with the complex medication regimen.
While all family members may take some medications, you will mostly be handling the medications
for the person with the complex medication regimen.
Questions/messages you will most likely handle are:
- Have I taken my morning medications yet today?
- How many more days until I need to get a refill for medication `medication name`?
- Do I have any refills left for `medication name` or do I need to call it in?
- What's the dosage for `medication name` again?
- Just took my morning meds, give me a reminder when it's time to take my evening meds.
- Give me a reminder on Thursday to call in my medication.
"""

@agent.instructions
async def initialization_instructions(ctx: RunContext[SessionDependencies]) -> str:
    return (
        f"{medication_assistant_general_instructions}"
        f"\nThe current date is {ctx.deps.todays_date!r}"
        f"\nThe user's name is {ctx.deps.user_info.user_name!r}"
        f"\nThe user's id is {ctx.deps.user_info.user_id!r}"
    )

########################################################################
# Tools
########################################################################

@agent.tool
async def medication_journal_add_entry(
        ctx: RunContext[SessionDependencies],
        medication_name: str,
        medication_frequency: str,
        medication_start_date: date,
        medication_end_date: date | None,
        medication_notes: str | None
    ) -> MedicationJournalEntry | None:
    """
    Add a medication journal entry to the user's medication journal
    """
    entry = MedicationJournalEntry(
        medication_name=medication_name,
        medication_frequency=medication_frequency,
        medication_start_date=medication_start_date,
        medication_end_date=medication_end_date,
        medication_notes=medication_notes
    )
    ctx.deps.medication_journal.add_entry(ctx.deps.user_info.user_id, entry)
    return entry


@agent.tool
async def medication_journal_get_entry(
        ctx: RunContext[SessionDependencies],
        index: int
    ) -> MedicationJournalEntry | None:
    """
    Get a specific medication journal entry by index for the current user
    """
    return ctx.deps.medication_journal.get_entry(ctx.deps.user_info.user_id, index)


@agent.tool
async def medication_journal_get_all_entries(
        ctx: RunContext[SessionDependencies]
    ) -> list[MedicationJournalEntry]:
    """
    Get all medication journal entries for the current user
    """
    return ctx.deps.medication_journal.get_entries(ctx.deps.user_info.user_id)


@agent.tool_plain
async def image_read_label_medication_bottle() -> ImageUrl:
    """
    Read the label on a medication bottle and return the text
    """
    return await read_label_medication_bottle()


########################################################################
# For use in CLI
########################################################################

async def main():
    deps = SessionDependencies(
        user_info=SlackUserIdentification(user_id=123, user_name='John Doe'),
        medication_journal=MedicationJournal()
    )
    await agent.to_cli(deps=deps)
