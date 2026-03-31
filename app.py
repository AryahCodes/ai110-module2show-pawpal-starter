import streamlit as st
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, PawPalSystem

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant — manage pets, tasks, and daily schedules.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", owner_id="owner1")

if "system" not in st.session_state:
    st.session_state.system = PawPalSystem()
    st.session_state.system.add_owner(st.session_state.owner)

owner = st.session_state.owner
system = st.session_state.system

st.divider()

st.subheader("Add a Pet")
col_pet1, col_pet2, col_pet3 = st.columns(3)
with col_pet1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_pet2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col_pet3:
    age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add pet"):
    if owner.get_pet(pet_name):
        st.warning(f"A pet named **{pet_name}** already exists.")
    else:
        new_pet = Pet(name=pet_name, species=species, age=age)
        owner.add_pet(new_pet)
        st.success(f"Added **{pet_name}** the {species}!")

if owner.pets:
    st.write("Your pets:")
    pet_data = [{"Name": p.name, "Species": p.species, "Age": p.age} for p in owner.pets]
    st.table(pet_data)
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")

if not owner.pets:
    st.info("Add a pet first before scheduling tasks.")
else:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Select pet", pet_names)
    selected_pet = owner.get_pet(selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    category = st.selectbox("Category", ["exercise", "feeding", "grooming", "medication", "other"])
    recurring = st.checkbox("Recurring daily")

    if st.button("Add task"):
        new_task = Task(
            title=task_title,
            category=category,
            priority=priority,
            due_time=datetime.now() + timedelta(hours=1),
            duration=int(duration),
            recurring=recurring,
        )
        selected_pet.add_task(new_task)
        st.success(f"Added task **{task_title}** for {selected_pet_name}!")

    pending = selected_pet.get_pending_tasks()
    if pending:
        st.write(f"Pending tasks for **{selected_pet_name}**:")
        task_rows = [
            {
                "Title": t.title,
                "Category": t.category,
                "Priority": t.priority,
                "Duration (min)": t.duration,
                "Due": t.due_time.strftime("%I:%M %p"),
                "Recurring": "Yes" if t.recurring else "No",
            }
            for t in pending
        ]
        st.table(task_rows)
    else:
        st.info(f"No pending tasks for {selected_pet_name}.")

st.divider()

# --- Complete Task ---
st.subheader("Complete a Task")

all_pending = []
for p in owner.pets:
    for t in p.get_pending_tasks():
        all_pending.append((p.name, t))

if all_pending:
    task_labels = [f"{pn}: {t.title}" for pn, t in all_pending]
    selected_label = st.selectbox("Select a task to complete", task_labels, key="complete_select")
    idx = task_labels.index(selected_label)
    target_pet_name, target_task = all_pending[idx]

    if st.button("Mark complete"):
        target_pet = owner.get_pet(target_pet_name)
        completed = target_pet.complete_task(target_task.title)
        if completed:
            msg = f"Completed **{completed.title}** for {target_pet_name}!"
            if completed.recurring:
                msg += " Next occurrence has been auto-scheduled."
            st.success(msg)
        else:
            st.error("Could not complete the task.")
else:
    st.info("No pending tasks to complete.")

st.divider()

# --- Daily Agenda with Sort & Filter ---
st.subheader("Daily Agenda")
st.caption("Generate a prioritized schedule across all your pets.")

# --- Always-visible: overdue alerts and conflict warnings ---
all_tasks_flat = []
for p in owner.pets:
    for t in p.tasks:
        all_tasks_flat.append((p.name, t))

overdue_tasks = [(pn, t) for pn, t in all_tasks_flat if t.is_overdue()]
pending_count = sum(1 for _, t in all_tasks_flat if not t.completed and not t.is_overdue())
overdue_count = len(overdue_tasks)
completed_count = sum(1 for _, t in all_tasks_flat if t.completed)

if overdue_tasks:
    for pn, t in overdue_tasks:
        st.error(
            f"**Overdue** — {pn}'s task *{t.title}* was due at "
            f"{t.due_time.strftime('%I:%M %p')} ({t.category}, {t.priority} priority)"
        )

appt_conflicts = system.detect_conflicts(owner.owner_id)
if appt_conflicts:
    with st.expander("⚠️ Appointment–Task Conflicts", expanded=True):
        for pn, appt, task in appt_conflicts:
            st.warning(
                f"**{pn}**: Appointment *{appt.title}* at "
                f"{appt.date_time.strftime('%I:%M %p')} conflicts with task "
                f"*{task.title}* (due {task.due_time.strftime('%I:%M %p')}, "
                f"{task.duration} min)"
            )

task_conflicts = system.detect_task_conflicts(owner.owner_id)
if task_conflicts:
    with st.expander("⚠️ Task Time-Overlap Conflicts", expanded=True):
        for pn, t1, t2 in task_conflicts:
            st.warning(
                f"**{pn}**: *{t1.title}* "
                f"({t1.due_time.strftime('%I:%M %p')}–"
                f"{(t1.due_time + timedelta(minutes=t1.duration)).strftime('%I:%M %p')}) "
                f"overlaps with *{t2.title}* "
                f"({t2.due_time.strftime('%I:%M %p')}–"
                f"{(t2.due_time + timedelta(minutes=t2.duration)).strftime('%I:%M %p')})"
            )

# --- Summary metrics ---
if all_tasks_flat:
    m1, m2, m3 = st.columns(3)
    m1.metric("Pending", pending_count)
    m2.metric("Overdue", overdue_count)
    m3.metric("Completed", completed_count)

# --- Sort & filter controls ---
sort_labels = {
    "Priority then Time": "priority",
    "Time only": "time",
    "Shortest first": "duration",
}
sort_choice = st.radio("Sort by", list(sort_labels.keys()), horizontal=True)

filter_col1, filter_col2, filter_col3 = st.columns(3)
with filter_col1:
    pet_filter_options = ["All"] + [p.name for p in owner.pets]
    pet_filter = st.selectbox("Filter by pet", pet_filter_options, key="filter_pet")
with filter_col2:
    status_filter = st.selectbox(
        "Filter by status", ["All", "pending", "completed", "overdue"], key="filter_status"
    )
with filter_col3:
    category_filter = st.selectbox(
        "Filter by category",
        ["All", "exercise", "feeding", "grooming", "medication", "other"],
        key="filter_category",
    )

if st.button("Generate schedule"):
    pf = None if pet_filter == "All" else pet_filter
    sf = None if status_filter == "All" else status_filter
    cf = None if category_filter == "All" else category_filter

    if pf or sf or cf:
        agenda = system.get_filtered_tasks(owner.owner_id, pet_name=pf, status=sf, category=cf)
    else:
        agenda = system.get_sorted_agenda(owner.owner_id, sort_by=sort_labels[sort_choice])

    if pf or sf or cf:
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sort_key = sort_labels[sort_choice]
        if sort_key == "time":
            agenda.sort(key=lambda x: x[1].due_time)
        elif sort_key == "duration":
            agenda.sort(key=lambda x: x[1].duration)
        else:
            agenda.sort(key=lambda x: (priority_order.get(x[1].priority, 3), x[1].due_time))

    if not agenda:
        st.info("No tasks match your criteria. Add pets and tasks first.")
    else:
        st.success(f"Showing {len(agenda)} task(s) sorted by **{sort_choice}**:")
        agenda_rows = [
            {
                "Pet": pn,
                "Task": task.title,
                "Category": task.category,
                "Priority": task.priority.capitalize(),
                "Due": task.due_time.strftime("%I:%M %p"),
                "Duration (min)": task.duration,
                "Status": "✅ Completed" if task.completed else (
                    "🔴 Overdue" if task.is_overdue() else "🟡 Pending"
                ),
            }
            for pn, task in agenda
        ]
        st.table(agenda_rows)
