from pydantic_ai import RunContext

from .data_models import SessionDependencies


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

# family_users = [MedNannyAIUserID(id=id, name=name) for id, name in family_names_map.items()]

async def initialization_instructions(ctx: RunContext[SessionDependencies]) -> str:
    [f'Name: {user.name} ID: {user.id}' for user in ctx.deps.family_users]
    return (
        f"{medication_assistant_general_instructions}"
        f"\nThe current date is: {ctx.deps.todays_date!r}"
        f"\nThe most recent message was sent by: Name: {ctx.deps.user_id.name!r}, ID: {ctx.deps.user_id.id!r}"
        # f"\nThe user's name is: {ctx.deps.user_id.name!r}"
        # f"\nThe user's id is: {ctx.deps.user_id.id!r}"
    )
