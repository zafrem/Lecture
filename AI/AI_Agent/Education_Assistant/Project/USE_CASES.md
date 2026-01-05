# Project Use Cases & Workflows

This document details the technical workflows for the primary use cases of the Education Assistant Agent. It is intended for developers and teachers understanding the system logic.

## 1. Teacher Workflows

### A. Managing the Schedule
**Goal:** Add a new class session and ensure the system is aware of it for future reminders.
- **Input (Discord/CLI):** `Schedule class on 2026-05-20 10:00 for Physics Lab`
- **System Process:**
    1.  `process_teacher_command` parses Date (`2026-05-20 10:00`) and Topic (`Physics Lab`).
    2.  `database_manager.add_schedule` inserts row into `schedules` table.
    3.  Returns success confirmation string.
- **Outcome:** Database updated. Daily Monitor will pick this up 24 hours before the event.

### B. Onboarding a Student
**Goal:** Add a new student to the tracking system.
- **Input:** `Add student Sarah Connor (sarah@skynet.edu)`
- **System Process:**
    1.  Parses Name (`Sarah Connor`) and Contact (`sarah@skynet.edu`).
    2.  `database_manager.add_student` inserts row.
- **Outcome:** Student is now active in the system and eligible for automated monitoring.

### C. Monitoring Feedback
**Goal:** Review anonymous concerns from the class.
- **Input (Discord):** `!report`
- **System Process:**
    1.  `agent.generate_feedback_report()` queries `feedback` table for `is_read = 0`.
    2.  Formats list of messages (stripping User IDs).
    3.  Updates `is_read = 1` for retrieved messages.
- **Outcome:** Teacher sees a digest of concerns without bias.

## 2. System Automation Workflows

### A. The "Equity Check" (Daily Monitor)
**Goal:** Proactively support struggling students.
- **Trigger:** Time-based loop (e.g., `tasks.loop(hours=24)` or Cron).
- **Process:**
    1.  Query `students` table for tag `needs_help`.
    2.  **IF** found:
        *   Log Alert: "Student X flagged."
        *   Trigger `email_service` (Mock or Real) to send specific resource.
    3.  Query `schedules` for events in `[Now, Now + 7 Days]`.
    4.  **IF** found:
        *   Log Notification: "Reminder for Class Y."
- **Outcome:** Automated support and reminders without teacher manual input.

### B. Anonymous Feedback Loop
**Goal:** Student sends a safe message.
- **Input:** Student DMs the Discord Bot.
- **Process:**
    1.  `discord_interface` detects DM channel.
    2.  Calls `agent.process_student_message(user_id, content)`.
    3.  `database_manager.add_feedback` saves message with `student_id` (for record) but `is_read=0`.
    4.  Bot replies to Student: "Teacher will see this anonymously."
    5.  Bot alerts Teacher Channel: "New feedback received."
- **Outcome:** Message stored safely. Student identity protected in the final report.

### C. Absence Management (Catch-Up System)
**Goal:** Send materials to absent students.
- **Input:** `Mark [Student Name] as absent`
- **System Process:**
    1.  Identify `student_id`.
    2.  Get current date's `schedule` entry (Topic/Materials).
    3.  Trigger `email_service`:
        *   **Subject**: "Missed Class Materials: [Topic]"
        *   **Body**: "Here are the notes..."
    4.  Log absence in `attendance` table (to be created).
- **Outcome:** Student receives resources immediately.

### D. Group Formation Algorithm
**Goal:** Create diverse groups based on tags.
- **Input:** `Create groups of 3`
- **System Process:**
    1.  Query all students with their `tags`.
    2.  **Algorithm**:
        *   Separate students into buckets (e.g., Technical, Creative, Analyst).
        *   Round-robin selection: Pick 1 from each bucket until group is full.
        *   Handle remainders (randomly assign).
    3.  Format Output: "Group 1: [Name, Name, Name]..."
- **Outcome:** Balanced teams without teacher bias.

### E. Progress Report Generation
**Goal:** Draft a status update for a specific student.
- **Input:** `Draft update for [Student Name]`
- **System Process:**
    1.  Query `grades` (Mock), `attendance`, and `tasks` (Status: pending).
    2.  **LLM/Template Construction**:
        *   "Attendance: [X]%"
        *   "Missing Tasks: [List]"
        *   "Recent Issues: [Feedback/Flags]"
    3.  Return text block to Discord for teacher review.
- **Outcome:** A ready-to-send draft for parents/admin.

## 3. Integration Examples

### Discord Command Map
| Command | Parameter | Description |
| :--- | :--- | :--- |
| `!agent` | `[Natural Language]` | Main interface for scheduling/adding. |
| `!report` | None | Fetches unread anonymous feedback. |
| `!email_all` | `"[Subject]" [Body]` | Sends mass email to all students. |
| `!groups` | `[Size]` | Generates student groups. |

### Database Schema Reference
- **Students**: `id, name, contact, tags`
- **Schedules**: `id, event_time, description, event_type`
- **Tasks**: `id, description, due_date, status`
- **Feedback**: `id, student_id, message, timestamp, is_read`
- **Attendance** (Proposed): `id, student_id, date, status`
