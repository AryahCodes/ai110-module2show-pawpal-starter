from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    title: str
    category: str
    priority: str
    due_time: str
    duration: int
    recurring: bool
    recurrence_days: list = field(default_factory=list)
    completed: bool = False

    def mark_complete(self):
        pass

    def is_overdue(self):
        pass

    def generate_next_task(self):
        pass


@dataclass
class Appointment:
    title: str
    date_time: datetime
    vet_name: str
    notes: str

    def conflicts_with(self, task):
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)
    appointments: list = field(default_factory=list)

    def add_task(self, task):
        pass

    def add_appointment(self, appointment):
        pass

    def get_pending_tasks(self):
        pass

    def complete_task(self, task_name):
        pass


@dataclass
class Owner:
    name: str
    owner_id: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet):
        pass

    def remove_pet(self, pet_name):
        pass

    def get_pet(self, pet_name):
        pass


class PawPalSystem:
    def __init__(self):
        self.owners: dict = {}

    def add_owner(self, owner):
        pass

    def add_pet_to_owner(self, owner_id, pet):
        pass

    def schedule_task(self, owner_id, pet_name, task):
        pass

    def schedule_appointment(self, owner_id, pet_name, appointment):
        pass

    def get_daily_agenda(self, owner_id):
        pass

    def detect_conflicts(self, owner_id):
        pass
