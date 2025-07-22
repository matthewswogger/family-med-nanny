import asyncio
from dotenv import load_dotenv

load_dotenv()


##############################################
# Requires the installation of the following:
#   pip install clai
if __name__ == '__main__':
    from med_nannyai import (
        # MedNannyAI,
        agent,
        SessionDependencies,
        SlackUserIdentification,
        MedicationJournal
    )
    async def main():
        deps = SessionDependencies(
            user_info=SlackUserIdentification(user_id=123, user_name='John Doe'),
            medication_journal=MedicationJournal()
        )
        await agent.to_cli(deps=deps)

    asyncio.run(main())
