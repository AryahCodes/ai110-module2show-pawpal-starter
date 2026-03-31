# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My system is designed around helping a pet owner manage daily care efficiently. The core actions the system supports are:
Add and manage pets  
Create and manage care tasks (feeding, walking, medication, etc.)  
Generate and view a prioritized daily schedule  

- What classes did you include, and what responsibilities did you assign to each?
Owner: manages user information and their pets  
Pet: stores pet details and associated tasks/appointments  
Task: represents care activities with attributes like priority, duration, and due time  
Appointment: represents scheduled events like vet visits  
PawPalSystem: coordinates scheduling, task management, and conflict detection  

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, my design changed during implementation based on reviewing my class structure.
One key change was updating how time is handled. Initially, I treated task due times as strings, but I realized this would cause issues when comparing times for overdue checks and conflict detection. I changed this to use datetime objects instead, which made comparisons more reliable and allowed scheduling logic to work correctly.
Another change was improving how recurring tasks are handled. Initially, tasks could generate a new task, but there was no clear place where the new task would be added back to the pet’s task list. I adjusted the design so that this logic is handled when completing a task, ensuring recurring tasks are properly scheduled.
These changes made the system more consistent and better aligned with the scheduling logic.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
My scheduler considers three constraints: priority (high, medium, low), due time, and task duration. By default, it sorts tasks by priority first and then by due time within each priority level, so high-priority tasks always appear before medium or low ones. It also supports sorting purely by time or by shortest duration first for a "quick-win" approach. For conflict detection, it considers task duration to calculate time windows and checks whether any two tasks overlap.
- How did you decide which constraints mattered most?
I decided priority should rank highest because in pet care, some tasks like medication are non-negotiable and must come first regardless of timing. Due time is the secondary constraint because once you know what's most important, you need to know what to do next chronologically. Duration is a tertiary option for when an owner wants to knock out quick tasks first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
My conflict detection only checks for time-window overlaps (whether two tasks' start-to-end ranges intersect). It does not check whether the owner realistically has enough buffer time between tasks -- for example, a task ending at 10:30 AM and another starting at 10:30 AM are not flagged as conflicting, even though there's zero travel or transition time between them.
- Why is that tradeoff reasonable for this scenario?
This is reasonable for a personal pet care app because most tasks happen at home, so transition time is minimal. Checking for exact overlap catches the real scheduling errors (double-booking) without being overly strict and flagging every back-to-back pair as a conflict, which would create too many false warnings for a simple daily planner.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I use design brainstorming and refactoring.
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
