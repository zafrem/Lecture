from agent_core import EducationAgent
import time

def main():
    agent = EducationAgent()
    
    print("=== 🎓 Education Assistant Agent Started ===")
    print("Simulating Teacher Interaction via Discord/Email...\n")

    # Scenario 1: Initial Setup (Teacher commands)
    commands = [
        "Add student Alice (alice@example.com)",
        "Add student Bob (bob@example.com)",
        "Add student Charlie (charlie@example.com)", 
        # Simulating a student with a 'needs_help' tag manually for now
        # (In real app, this might come from 'Analyze grade' command)
    ]
    
    for cmd in commands:
        response = agent.process_teacher_command(cmd)
        print(response)

    # Manually update a student to have "needs_help" tag for demo
    import database_manager
    conn = database_manager.get_connection()
    conn.execute("UPDATE students SET tags = 'needs_help' WHERE name = 'Charlie'")
    conn.commit()
    conn.close()
    print("ℹ️  [System] Simulating low quiz score for Charlie (Tag: 'needs_help' added)")

    # Scenario 2: Scheduling
    print("\n--- Teacher sets the schedule ---")
    print(agent.process_teacher_command("Schedule class on 2026-01-10 14:00 for Python Basics"))
    print(agent.process_teacher_command("Assign task Review Chapter 1 by 2026-01-09"))

    # Scenario 3: The "Monitor" wakes up (e.g., Cron job)
    print("\n--- 🕒 8:00 AM Daily Check ---")
    monitor_logs = agent.run_daily_monitor()
    for log in monitor_logs:
        print(log)

    # Scenario 4: Anonymous Student Feedback
    print("\n--- 💬 Student Interaction Simulation ---")
    print("Simulating Student 'Alice' sending a private message...")
    # Assuming Alice has ID 1 (based on order of insertion)
    print(agent.process_student_message(1, "The Python Basics class is moving a bit too fast for me."))
    
    print("Simulating Student 'Bob' sending a question...")
    print(agent.process_student_message(2, "Will the exam cover Chapter 2?"))

    # Teacher checks report
    print("\n--- 📋 Teacher checks reports ---")
    report_lines = agent.generate_feedback_report()
    for line in report_lines:
        print(line)

    print("\n=== Demo Complete ===")
    print("You can try entering commands below (or type 'exit'):")
    print("Examples:")
    print(" - Add student [Name]")
    print(" - Schedule class on YYYY-MM-DD HH:MM for [Topic]")
    
    while True:
        try:
            user_input = input("\nTeacher> ")
            if user_input.lower() in ['exit', 'quit']:
                break
            response = agent.process_teacher_command(user_input)
            print(response)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
