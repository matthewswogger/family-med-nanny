from dataclasses import dataclass
from datetime import date

from med_nannyai.medication_journal import (
    MedNannyAIUserID,
    MedicationJournals
)


@dataclass
class SessionDependencies:
    journal: MedicationJournals
    user_id: MedNannyAIUserID
    family_users: list[MedNannyAIUserID]
    todays_date: date = date.today()
