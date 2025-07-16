# For each medication, we will have a journal entry.

# The journal entry will have the following fields:
# - medication_name
# - medication_dosage
# - medication_frequency
# - medication_start_date
# - medication_end_date
# - medication_notes
# - medication_refills_left
# - medication_refills_needed
# - if_medication_was_taken_at_correct_time

# each family member will have an individual journal where journal entries are tracked.

from dataclasses import dataclass
from pydantic import Field
from datetime import date


@dataclass
class MedicationJournalEntry:
    medication_name: str = Field(description='The name of the medication')
    medication_frequency: str = Field(description='The frequency of the medication')
    medication_start_date: date = Field(description='The start date of the medication')
    medication_end_date: date | None = Field(default=None, description='The end date of the medication')
    medication_notes: str | None = Field(default=None, description='Any notes about the medication')


class MedicationJournal:
    entries: dict[int, list[MedicationJournalEntry]] = {}

    @classmethod
    def add_entry(cls, user_id: int, entry: MedicationJournalEntry):
        if user_id not in cls.entries:
            cls.entries[user_id] = []
        cls.entries[user_id].append(entry)

    @classmethod
    def get_entry(cls, user_id: int, index: int) -> MedicationJournalEntry | None:
        if user_id not in cls.entries or index >= len(cls.entries[user_id]):
            return None
        return cls.entries[user_id][index]

    @classmethod
    def get_entries(cls, user_id: int) -> list[MedicationJournalEntry]:
        if user_id not in cls.entries:
            return []
        return cls.entries[user_id]
