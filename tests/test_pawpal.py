from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, PawPalSystem


def test_task_completion():
    task = Task(
        title="Morning Walk",
        category="exercise",
        priority="high",
        due_time=datetime(2026, 3, 31, 7, 0),
        duration=30,
        recurring=False,
    )
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_task_addition():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.tasks) == 0

    task = Task(
        title="Feeding",
        category="nutrition",
        priority="medium",
        due_time=datetime(2026, 3, 31, 8, 0),
        duration=10,
        recurring=False,
    )
    pet.add_task(task)
    assert len(pet.tasks) == 1


# --------------- Sorting Correctness ---------------

def _build_system_with_tasks(tasks):
    """Helper: create an Owner+Pet inside a PawPalSystem and add the given tasks."""
    system = PawPalSystem()
    owner = Owner(name="Jordan", owner_id="o1")
    pet = Pet(name="Mochi", species="dog", age=3)
    for t in tasks:
        pet.add_task(t)
    owner.add_pet(pet)
    system.add_owner(owner)
    return system


def test_sort_by_priority():
    tasks = [
        Task("Grooming", "grooming", "low", datetime(2026, 4, 1, 9, 0), 20, False),
        Task("Medication", "medication", "high", datetime(2026, 4, 1, 10, 0), 5, False),
        Task("Walk", "exercise", "medium", datetime(2026, 4, 1, 8, 0), 30, False),
    ]
    system = _build_system_with_tasks(tasks)
    agenda = system.get_sorted_agenda("o1", sort_by="priority")
    titles = [t.title for _, t in agenda]
    assert titles == ["Medication", "Walk", "Grooming"]


def test_sort_by_priority_tiebreak_by_time():
    tasks = [
        Task("Late Walk", "exercise", "high", datetime(2026, 4, 1, 11, 0), 30, False),
        Task("Early Meds", "medication", "high", datetime(2026, 4, 1, 7, 0), 5, False),
    ]
    system = _build_system_with_tasks(tasks)
    agenda = system.get_sorted_agenda("o1", sort_by="priority")
    titles = [t.title for _, t in agenda]
    assert titles == ["Early Meds", "Late Walk"]


def test_sort_by_time():
    tasks = [
        Task("Grooming", "grooming", "low", datetime(2026, 4, 1, 12, 0), 20, False),
        Task("Medication", "medication", "high", datetime(2026, 4, 1, 7, 0), 5, False),
        Task("Walk", "exercise", "medium", datetime(2026, 4, 1, 9, 0), 30, False),
    ]
    system = _build_system_with_tasks(tasks)
    agenda = system.get_sorted_agenda("o1", sort_by="time")
    titles = [t.title for _, t in agenda]
    assert titles == ["Medication", "Walk", "Grooming"]


def test_sort_by_duration():
    tasks = [
        Task("Walk", "exercise", "high", datetime(2026, 4, 1, 8, 0), 30, False),
        Task("Medication", "medication", "high", datetime(2026, 4, 1, 9, 0), 5, False),
        Task("Grooming", "grooming", "low", datetime(2026, 4, 1, 10, 0), 20, False),
    ]
    system = _build_system_with_tasks(tasks)
    agenda = system.get_sorted_agenda("o1", sort_by="duration")
    titles = [t.title for _, t in agenda]
    assert titles == ["Medication", "Grooming", "Walk"]


# --------------- Recurrence Logic ---------------

def test_recurring_task_creates_next_day():
    pet = Pet(name="Mochi", species="dog", age=3)
    original_due = datetime(2026, 4, 1, 8, 0)
    task = Task("Feeding", "feeding", "high", original_due, 10, recurring=True)
    pet.add_task(task)

    pet.complete_task("Feeding")

    assert task.completed is True
    assert len(pet.tasks) == 2
    next_task = pet.tasks[1]
    assert next_task.title == "Feeding"
    assert next_task.completed is False
    assert next_task.due_time == original_due + timedelta(days=1)
    assert next_task.recurring is True


def test_non_recurring_task_no_next():
    pet = Pet(name="Mochi", species="dog", age=3)
    task = Task("Vet Visit Prep", "other", "medium", datetime(2026, 4, 1, 14, 0), 15, recurring=False)
    pet.add_task(task)

    pet.complete_task("Vet Visit Prep")

    assert task.completed is True
    assert len(pet.tasks) == 1


# --------------- Conflict Detection ---------------

def test_overlapping_tasks_detected():
    tasks = [
        Task("Walk", "exercise", "high", datetime(2026, 4, 1, 9, 0), 30, False),
        Task("Grooming", "grooming", "medium", datetime(2026, 4, 1, 9, 15), 30, False),
    ]
    system = _build_system_with_tasks(tasks)
    conflicts = system.detect_task_conflicts("o1")
    assert len(conflicts) == 1
    _, t1, t2 = conflicts[0]
    conflict_titles = {t1.title, t2.title}
    assert conflict_titles == {"Walk", "Grooming"}


def test_non_overlapping_tasks_no_conflict():
    tasks = [
        Task("Walk", "exercise", "high", datetime(2026, 4, 1, 9, 0), 30, False),
        Task("Grooming", "grooming", "medium", datetime(2026, 4, 1, 10, 0), 30, False),
    ]
    system = _build_system_with_tasks(tasks)
    conflicts = system.detect_task_conflicts("o1")
    assert len(conflicts) == 0
