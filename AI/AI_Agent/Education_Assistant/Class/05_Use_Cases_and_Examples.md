# Step 5: Use Cases & Real-World Examples

Understanding the code is one thing; understanding *how to apply it* is another. This document outlines specific scenarios where the Education Assistant Agent solves real classroom problems.

## 1. The "Equity Guardian" Scenario
**Problem:** In a class of 40, "Charlie" quietly fails the first two quizzes. The teacher is too busy grading papers to notice the trend immediately. Charlie falls further behind.

**Agent Solution:**
1.  **Trigger:** The system logs a grade below 60% for Charlie (or a manual tag `needs_help` is added).
2.  **Monitor Action:** During the daily scan, the Agent flags Charlie.
3.  **Automated Response:** The Agent retrieves "Supplementary Pack #1" (Basic Concepts Review) and emails it to Charlie automatically.
4.  **Result:** Charlie gets immediate support resources without waiting for the next parent-teacher conference.

## 2. The "Safe Space" Bridge
**Problem:** "Alice" is confused about the new homework but is too shy to ask in the public Discord channel because she thinks everyone else understands it.

**Agent Solution:**
1.  **Action:** Alice DMs the Bot: *"I don't understand how the 'Loop' works in the homework."*
2.  **Processing:** The Agent strips her User ID and name.
3.  **Reporting:** The Agent adds the message to the **Daily Report**.
4.  **Teacher View:** The teacher sees: *"[Anonymous]: I don't understand how the 'Loop' works..."*
5.  **Result:** The teacher realizes this is a common issue and reviews "Loops" in the next class, helping Alice and likely others, without Alice feeling embarrassed.

## 3. The "Logistics Manager"
**Problem:** The teacher gets sick and needs to move Tuesday's class to Thursday online. Usually, this involves emailing parents, posting on the LMS, and messaging the group chat—often forgetting one group.

**Agent Solution:**
1.  **Command:** Teacher types: `!agent Reschedule Tuesday class to Thursday 4PM Online`.
2.  **Execution:**
    *   Updates the database Schedule.
    *   Sends a generic "Urgent Update" email to the entire class mailing list.
    *   Posts an announcement in the Discord `#announcements` channel.
3.  **Result:** Consistent communication across all channels instantly.

## 4. The "Homework Nudge"
**Problem:** Students often forget deadlines until the night before.

**Agent Solution:**
1.  **Monitor Action:** The Agent scans the `Tasks` table every morning.
2.  **Logic:** Finds tasks due in exactly 3 days.
3.  **Execution:** Sends a friendly DM reminder to all students who haven't marked it as complete (future feature).
    *   *"Hi! Just a friendly reminder that 'Chapter 3 Essay' is due in 3 days. Do you need the reference sheet again?"*
4.  **Result:** Higher submission rates and less last-minute panic.

## 5. The "Absent Student" Catch-Up
**Problem:** "David" misses class due to illness. The teacher has to remember to email him the slides and the new assignment manually.

**Agent Solution:**
1.  **Trigger:** Teacher marks attendance: `!agent Mark David as absent`.
2.  **Action:** The Agent immediately retrieves the day's "Lecture Summary" and "Homework #4" from the database.
3.  **Execution:** Emails David: *"Sorry we missed you today! Here is what we covered and the homework due Tuesday."*
4.  **Result:** David stays in the loop without extra work for the teacher.

## 6. The "Project Group" Matchmaker
**Problem:** Forming groups is hard. Friends stick together, and skills aren't balanced.

**Agent Solution:**
1.  **Data:** The Agent knows student tags (e.g., `coder`, `designer`, `writer`).
2.  **Command:** `!agent Create balanced groups of 3`.
3.  **Logic:** The Agent mixes tags to ensure each group has at least one `coder` and one `writer`.
4.  **Output:** Publishes the list to Discord: *"Group A: Alice (Coder), Bob (Writer), Charlie (Designer)."*

## 7. The "Topic Trouble" Detector (Quiz Analyzer)
**Problem:** The teacher thinks everyone understood "Recursion," but 60% of the class failed that specific question on the quiz.

**Agent Solution:**
1.  **Input:** Teacher uploads quiz data (future feature).
2.  **Analysis:** The Agent notices a spike in wrong answers for "Question 5: Recursion".
3.  **Alert:** Agent suggests: *"It seems 60% of students struggled with Recursion. Should I schedule a 15-min review for next class?"*
4.  **Action:** Teacher agrees, and the schedule is updated.

## 8. The "Parent Update" Drafter
**Problem:** Parents want updates, but writing 30 personalized emails is time-consuming.

**Agent Solution:**
1.  **Command:** `!agent Draft weekly update for Emily`.
2.  **Process:** Agent pulls Emily's attendance, last 3 quiz scores, and missing tasks.
3.  **Output:** Generates a draft email for the teacher to review:
    > "Dear Parents, Emily has attended all classes this week. She excelled in History (90%) but has a missing assignment in Math due yesterday. Please remind her..."
4.  **Result:** Teacher edits and sends in seconds, not minutes.

## 9. Summary of Commands
Here is a quick reference of the natural language commands designed for this agent:

| Intent | Example Command |
| :--- | :--- |
| **Add Student** | `Add student John Doe (john@email.com)` |
| **Schedule** | `Schedule class on 2026-10-05 14:00 for Advanced Math` |
| **Homework** | `Assign task Read Chapter 4 by 2026-10-10` |
| **Attendance** | `Mark [Name] as absent` (New) |
| **Groups** | `Create balanced groups of [Number]` (New) |
| **Report** | `!report` (Discord specific) |
