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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
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
