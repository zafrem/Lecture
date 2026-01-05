import database_manager
import datetime
import re

class EducationAgent:
    def __init__(self):
        database_manager.init_db()

    def process_teacher_command(self, user_input):
        """
        Simulates an LLM parsing natural language into structured actions.
        In a real app, this would call OpenAI/Gemini API.
        Here, we use Regex for demonstration.
        """
        print(f"\n[Agent] Processing command: '{user_input}'")
        
        # 1. Intent: Add Student
        # Pattern: "Add student Name (Contact)"
        match_student = re.search(r"add student\s+([a-zA-Z\s]+)(?:\((.*)\))?", user_input, re.IGNORECASE)
        if match_student:
            name = match_student.group(1).strip()
            contact = match_student.group(2) if match_student.group(2) else "No contact"
            database_manager.add_student(name, contact)
            return f"✅ Added student: {name}"

        # 2. Intent: Schedule Class
        # Pattern: "Schedule class on YYYY-MM-DD HH:MM for Topic"
        match_schedule = re.search(r"schedule class on\s+([\d\-\s:]+)\s+for\s+(.*)", user_input, re.IGNORECASE)
        if match_schedule:
            date_str = match_schedule.group(1).strip()
            topic = match_schedule.group(2).strip()
            try:
                # Naive date parsing
                event_time = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                database_manager.add_schedule(event_time, topic)
                return f"✅ Class scheduled: '{topic}' at {event_time}"
            except ValueError:
                return "❌ Error: Date format should be YYYY-MM-DD HH:MM"

        # 3. Intent: Assign Homework
        # Pattern: "Assign task Description by YYYY-MM-DD"
        match_task = re.search(r"assign task\s+(.+)\s+by\s+([\d\-]+)", user_input, re.IGNORECASE)
        if match_task:
            desc = match_task.group(1).strip()
            date_str = match_task.group(2).strip()
            try:
                due_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                database_manager.add_task(desc, due_date)
                return f"✅ Homework assigned: '{desc}' due {due_date.date()}"
            except ValueError:
                return "❌ Error: Date format should be YYYY-MM-DD"

        return "❓ I didn't understand that. Try 'Add student...', 'Schedule class...', or 'Assign task...'."

    def run_daily_monitor(self):
        """
        Simulates the background 'Monitor' agent that checks for issues.
        Returns a list of logs/actions to be sent via Discord/Email.
        """
        logs = []
        logs.append("[Monitor Agent] 🔍 Scanning for required actions...")
        
        # 1. Check upcoming classes (Notify students)
        schedules = database_manager.get_upcoming_schedule()
        if schedules:
            logs.append(f"  -> Found {len(schedules)} upcoming classes.")
            for s in schedules:
                # s: (id, time, desc, type)
                logs.append(f"     📢 Queued Notification: 'Reminder: {s[2]} is starting at {s[1]}!'")
        else:
            logs.append("  -> No upcoming classes found.")

        # 2. Check for students needing help (Simulation)
        students = database_manager.get_all_students()
        at_risk_count = 0
        for stu in students:
            # stu: (id, name, contact, tags)
            if stu[3] and "needs_help" in stu[3]: # Check tags
                logs.append(f"  -> 🚨 ALERT: Student {stu[1]} flagged for support.")
                logs.append(f"     🚀 Action: Sent 'Supplementary Pack #1' to {stu[2]}")
                at_risk_count += 1
        
        if at_risk_count == 0:
            logs.append("  -> All students appear to be on track.")
            
        return logs

    def process_student_message(self, student_id, message):
        """
        Handles incoming messages from students.
        Stores them in the database for later anonymized reporting.
        """
        # In a real bot, we might log this internally
        # print(f"\n[Agent] 📩 Received message from Student ID {student_id}")
        database_manager.add_feedback(student_id, message)
        return "Message received. The teacher will see this anonymously."

    def generate_feedback_report(self):
        """
        Aggregates unread feedback and presents it anonymously to the teacher.
        Returns a list of strings.
        """
        report_lines = []
        report_lines.append("[Feedback Agent] 📊 Anonymous Student Report")
        
        feedbacks = database_manager.get_unread_feedback()
        
        if not feedbacks:
            report_lines.append("  -> No new student feedback.")
            return report_lines

        report_lines.append(f"  -> Found {len(feedbacks)} new messages:")
        feedback_ids = []
        for fb in feedbacks:
            # fb: (id, student_id, message, timestamp)
            report_lines.append(f"     📝 Anonymous: \"{fb[2]}\" (Time: {fb[3]})")
            feedback_ids.append(fb[0])
        
        # Mark as read
        database_manager.mark_feedback_read(feedback_ids)
        report_lines.append("  -> All messages marked as read.")
        return report_lines
