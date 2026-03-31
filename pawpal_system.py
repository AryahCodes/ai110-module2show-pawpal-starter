from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Task:
    title: str
    category: str
    priority: str
    due_time: datetime
    duration: int
    recurring: bool
    recurrence_days: list = field(default_factory=list)
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_overdue(self):
        """Return True if the task is past due and not completed."""
        return not self.completed and self.due_time < datetime.now()

    def generate_next_task(self):
        """Create and return the next occurrence of a recurring task."""
        if not self.recurring:
            return None
        next_due = self.due_time + timedelta(days=1)
        return Task(
            title=self.title,
            category=self.category,
            priority=self.priority,
            due_time=next_due,
            duration=self.duration,
            recurring=self.recurring,
            recurrence_days=self.recurrence_days,
            completed=False,
        )


@dataclass
class Appointment:
    title: str
    date_time: datetime
    vet_name: str
    notes: str

    def conflicts_with(self, task):
        """Return True if this appointment overlaps with the task's time window."""
        task_end = task.due_time + timedelta(minutes=task.duration)
        return self.date_time < task_end and self.date_time >= task.due_time


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)
    appointments: list = field(default_factory=list)

    def add_task(self, task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def add_appointment(self, appointment):
        """Add an appointment to this pet's appointment list."""
        self.appointments.append(appointment)

    def get_pending_tasks(self):
        """Return all tasks that have not been completed."""
        return [task for task in self.tasks if not task.completed]

    def complete_task(self, task_name):
        """Complete a task by name and schedule the next one if recurring."""
        for task in self.tasks:
            if task.title == task_name and not task.completed:
                task.mark_complete()
                next_task = task.generate_next_task()
                if next_task:
                    self.tasks.append(next_task)
                return task
        return None


@dataclass
class Owner:
    name: str
    owner_id: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name):
        """Remove a pet by name from this owner's pet list."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_pet(self, pet_name):
        """Return the pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None


class PawPalSystem:
    def __init__(self):
        self.owners: dict = {}

    def add_owner(self, owner):
        """Register an owner in the system."""
        self.owners[owner.owner_id] = owner

    def add_pet_to_owner(self, owner_id, pet):
        """Add a pet to the specified owner."""
        owner = self.owners.get(owner_id)
        if owner:
            owner.add_pet(pet)

    def schedule_task(self, owner_id, pet_name, task):
        """Schedule a task for a specific pet belonging to an owner."""
        owner = self.owners.get(owner_id)
        if owner:
            pet = owner.get_pet(pet_name)
            if pet:
                pet.add_task(task)

    def schedule_appointment(self, owner_id, pet_name, appointment):
        """Schedule an appointment for a specific pet belonging to an owner."""
        owner = self.owners.get(owner_id)
        if owner:
            pet = owner.get_pet(pet_name)
            if pet:
                pet.add_appointment(appointment)

    def get_daily_agenda(self, owner_id):
        """Return all pending tasks for an owner, sorted by priority then time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        owner = self.owners.get(owner_id)
        if not owner:
            return []
        all_tasks = []
        for pet in owner.pets:
            for task in pet.get_pending_tasks():
                all_tasks.append((pet.name, task))
        all_tasks.sort(key=lambda x: (priority_order.get(x[1].priority, 3), x[1].due_time))
        return all_tasks

    def detect_conflicts(self, owner_id):
        """Find appointments that overlap with pending tasks for an owner."""
        owner = self.owners.get(owner_id)
        if not owner:
            return []
        conflicts = []
        for pet in owner.pets:
            for appointment in pet.appointments:
                for task in pet.get_pending_tasks():
                    if appointment.conflicts_with(task):
                        conflicts.append((pet.name, appointment, task))
        return conflicts
