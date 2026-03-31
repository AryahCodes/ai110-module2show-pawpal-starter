from datetime import datetime
from pawpal_system import Task, Pet


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
