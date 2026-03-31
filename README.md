# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ includes an algorithmic layer that makes the scheduler more intelligent:

- **Flexible sorting** — View your daily agenda sorted by priority (high first), by time (earliest first), or by duration (shortest first for a quick-win approach).
- **Filtering** — Narrow down tasks by pet name, completion status (pending, completed, overdue), or category (exercise, feeding, grooming, medication, other).
- **Recurring task automation** — When a recurring task is marked complete, the next occurrence is automatically scheduled for the following day.
- **Conflict detection** — The system detects overlapping time windows between tasks for the same pet and displays warnings instead of silently double-booking.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The tests in `tests/test_pawpal.py` cover three core scheduling behaviors:

- **Sorting correctness** — Verifies that the daily agenda is returned in the right order for all three sort modes (priority, time, and duration), including tie-breaking within the same priority level.
- **Recurrence logic** — Confirms that completing a recurring task auto-creates the next day's occurrence, and that non-recurring tasks do not generate follow-ups.
- **Conflict detection** — Checks that overlapping task time windows are flagged as conflicts, and that non-overlapping tasks produce no false positives.

**Confidence Level:** 4/5 stars — the tests cover the most important algorithmic behaviors and all pass consistently.
