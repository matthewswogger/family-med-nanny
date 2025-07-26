from dataclasses import dataclass, field
from datetime import date, datetime, timedelta


@dataclass(frozen=True)
class MedNannyAIUserID:
    id: str
    name: str

@dataclass
class Medication:
    """
    A medication is a single medication that a user is taking.
    """
    name: str
    frequency: str
    start_date: date
    end_date: date | None = None
    number_of_refills: int | None = None
    refills_expire_at: date | None = None
    # taken_at_correct_time: bool | None = None
    notes: str | None = None
    added_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime | None = None

@dataclass
class MedicationJournal:
    """
    A medication journal is a collection of medications that a unique user is taking, or has taken.
    """
    medications: dict[str, Medication] | dict[None, None] = field(default_factory=dict)

    def add_medication(self, medication: Medication):
        if medication.name not in self.medications:
            self.medications[medication.name] = medication
        else:
            raise ValueError(f"Entry with name {medication.name!r} already exists in your journal")

    def get_medication(self, medication_name: str) -> Medication | None:
        return self.medications.get(medication_name)

    def delete_medication(self, medication_name: str) -> Medication | None:
        return self.medications.pop(medication_name, None)


@dataclass
class MedicationJournals:
    journals: dict[MedNannyAIUserID, MedicationJournal] | dict[None, None] = field(default_factory=dict)

    def add_journal(self, med_nanny_user_id: MedNannyAIUserID):
        """
        Add a new journal for a user if it doesn't exist.
        """
        if med_nanny_user_id not in self.journals:
            self.journals[med_nanny_user_id] = MedicationJournal()

    def get_journal(self, med_nanny_user_id: MedNannyAIUserID) -> MedicationJournal:
        """
        Get user journal.
        """
        if not self.journals.get(med_nanny_user_id):
            self.add_journal(med_nanny_user_id)
        return self.journals[med_nanny_user_id]

    def add_medication(self, med_nanny_user_id: MedNannyAIUserID, medication: Medication):
        """
        Add a medication to a user's journal.
        """
        self.get_journal(med_nanny_user_id).add_medication(medication)


    def get_medication(self, med_nanny_user_id: MedNannyAIUserID, medication_name: str) -> Medication | None:
        """
        Get a medication from a user's journal.
        """
        return self.get_journal(med_nanny_user_id).get_medication(medication_name)

    def delete_medication(self, med_nanny_user_id: MedNannyAIUserID, medication_name: str) -> Medication | None:
        """
        Delete a medication from a user's journal.
        """
        return self.get_journal(med_nanny_user_id).delete_medication(medication_name)

