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

system.schedule_task("owner1", "Mochi", Task(
    title="Morning Walk",
    category="exercise",
    priority="high",
    due_time=now.replace(hour=7, minute=0, second=0),
    duration=30,
    recurring=True,
))

system.schedule_task("owner1", "Mochi", Task(
    title="Medication",
    category="health",
    priority="high",
    due_time=now.replace(hour=9, minute=0, second=0),
    duration=5,
    recurring=True,
))

system.schedule_task("owner1", "Whiskers", Task(
    title="Feeding",
    category="nutrition",
    priority="medium",
    due_time=now.replace(hour=8, minute=0, second=0),
    duration=10,
    recurring=True,
))

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
    category="hygiene",
    priority="low",
    due_time=now.replace(hour=12, minute=0, second=0),
    duration=10,
    recurring=False,
))

agenda = system.get_daily_agenda("owner1")

print("=" * 50)
print(f"  Today's Schedule for {owner.name}")
print(f"  {now.strftime('%A, %B %d, %Y')}")
print("=" * 50)

for i, (pet_name, task) in enumerate(agenda, 1):
    time_str = task.due_time.strftime("%I:%M %p")
    status = "OVERDUE" if task.is_overdue() else "Pending"
    print(f"\n  {i}. [{task.priority.upper()}] {task.title}")
    print(f"     Pet: {pet_name} | Time: {time_str} | Duration: {task.duration} min")
    print(f"     Category: {task.category} | Status: {status}")

print("\n" + "=" * 50)
print(f"  Total tasks: {len(agenda)}")
print("=" * 50)
