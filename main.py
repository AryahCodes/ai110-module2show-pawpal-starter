from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, PawPalSystem

system = PawPalSystem()

owner = Owner(name="Jordan", owner_id="owner1")
system.add_owner(owner)

mochi = Pet(name="Mochi", species="dog", age=3)
whiskers = Pet(name="Whiskers", species="cat", age=5)
system.add_pet_to_owner("owner1", mochi)
system.add_pet_to_owner("owner1", whiskers)

now = datetime.now()

# Tasks added deliberately OUT OF ORDER (late before early, low before high)
system.schedule_task("owner1", "Mochi", Task(
    title="Evening Walk",
    category="exercise",
    priority="medium",
    due_time=now.replace(hour=17, minute=0, second=0),
    duration=30,
    recurring=True,
))

system.schedule_task("owner1", "Whiskers", Task(
    title="Litter Box Cleaning",
    category="grooming",
    priority="low",
    due_time=now.replace(hour=12, minute=0, second=0),
    duration=10,
    recurring=False,
))

system.schedule_task("owner1", "Mochi", Task(
    title="Medication",
    category="medication",
    priority="high",
    due_time=now.replace(hour=9, minute=0, second=0),
    duration=5,
    recurring=True,
))

system.schedule_task("owner1", "Whiskers", Task(
    title="Feeding",
    category="feeding",
    priority="medium",
    due_time=now.replace(hour=8, minute=0, second=0),
    duration=10,
    recurring=True,
))

system.schedule_task("owner1", "Mochi", Task(
    title="Morning Walk",
    category="exercise",
    priority="high",
    due_time=now.replace(hour=7, minute=0, second=0),
    duration=30,
    recurring=True,
))


def print_task_list(task_list):
    """Helper to print a list of (pet_name, task) tuples."""
    if not task_list:
        print("  (no tasks)")
        return
    for i, (pet_name, task) in enumerate(task_list, 1):
        time_str = task.due_time.strftime("%I:%M %p")
        status = "OVERDUE" if task.is_overdue() else "Pending"
        if task.completed:
            status = "Completed"
        print(f"  {i}. [{task.priority.upper()}] {task.title}")
        print(f"     Pet: {pet_name} | Time: {time_str} | Duration: {task.duration} min")
        print(f"     Category: {task.category} | Status: {status}")


# ---- SORTING DEMOS ----

print("=" * 55)
print(f"  Today's Schedule for {owner.name}")
print(f"  {now.strftime('%A, %B %d, %Y')}")
print("=" * 55)

print("\n--- Sorted by PRIORITY then Time ---")
agenda_priority = system.get_sorted_agenda("owner1", sort_by="priority")
print_task_list(agenda_priority)

print("\n--- Sorted by TIME only ---")
agenda_time = system.get_sorted_agenda("owner1", sort_by="time")
print_task_list(agenda_time)

print("\n--- Sorted by DURATION (shortest first) ---")
agenda_duration = system.get_sorted_agenda("owner1", sort_by="duration")
print_task_list(agenda_duration)

# ---- FILTERING DEMOS ----

print("\n" + "=" * 55)
print("  FILTERING RESULTS")
print("=" * 55)

print("\n--- Filter: only Mochi's tasks ---")
mochi_tasks = system.get_filtered_tasks("owner1", pet_name="Mochi")
print_task_list(mochi_tasks)

print("\n--- Filter: only pending tasks ---")
pending_tasks = system.get_filtered_tasks("owner1", status="pending")
print_task_list(pending_tasks)

print("\n--- Filter: only exercise tasks ---")
exercise_tasks = system.get_filtered_tasks("owner1", category="exercise")
print_task_list(exercise_tasks)

# ---- RECURRING TASK DEMO ----

print("\n" + "=" * 55)
print("  RECURRING TASK DEMO")
print("=" * 55)

print("\n--- Completing 'Morning Walk' (recurring) for Mochi ---")
completed_task = mochi.complete_task("Morning Walk")
if completed_task:
    print(f"  Completed: {completed_task.title}")
    print(f"  Was recurring: {'Yes' if completed_task.recurring else 'No'}")
    next_task = [t for t in mochi.get_pending_tasks() if t.title == "Morning Walk"]
    if next_task:
        print(f"  Next occurrence auto-scheduled for: {next_task[0].due_time.strftime('%A, %B %d at %I:%M %p')}")

print("\n--- Mochi's pending tasks after completion ---")
mochi_pending = [(mochi.name, t) for t in mochi.get_pending_tasks()]
print_task_list(mochi_pending)

# ---- CONFLICT DETECTION DEMO ----

print("\n" + "=" * 55)
print("  CONFLICT DETECTION DEMO")
print("=" * 55)

print("\n--- Adding two overlapping tasks for Mochi at 10:00 AM ---")
system.schedule_task("owner1", "Mochi", Task(
    title="Grooming Session",
    category="grooming",
    priority="medium",
    due_time=now.replace(hour=10, minute=0, second=0),
    duration=30,
    recurring=False,
))
system.schedule_task("owner1", "Mochi", Task(
    title="Training Class",
    category="exercise",
    priority="high",
    due_time=now.replace(hour=10, minute=0, second=0),
    duration=45,
    recurring=False,
))
print("  Added: Grooming Session  (10:00 AM, 30 min)")
print("  Added: Training Class    (10:00 AM, 45 min)")

task_conflicts = system.detect_task_conflicts("owner1")
if task_conflicts:
    print(f"\n  WARNING: {len(task_conflicts)} conflict(s) detected!")
    for pet_name, t1, t2 in task_conflicts:
        t1_end = t1.due_time + timedelta(minutes=t1.duration)
        t2_end = t2.due_time + timedelta(minutes=t2.duration)
        print(f"  - {pet_name}: '{t1.title}' ({t1.due_time.strftime('%I:%M %p')}-{t1_end.strftime('%I:%M %p')})"
              f" overlaps with '{t2.title}' ({t2.due_time.strftime('%I:%M %p')}-{t2_end.strftime('%I:%M %p')})")
else:
    print("\n  No conflicts detected.")

print("\n" + "=" * 55)
print(f"  Total tasks across all pets: {len(system.get_sorted_agenda('owner1'))}")
print("=" * 55)
