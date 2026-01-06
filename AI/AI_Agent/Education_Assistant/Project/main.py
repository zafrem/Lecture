from agent_core import EducationAgent
import time
import os

# Set fake API keys for logic flow demonstration (Triggering fallback if real ones aren't present)
if not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    print("ℹ️  No Cloud API Keys found. The Agent will attempt to use Local Ollama or fallback to Regex.")

def main():
    agent = EducationAgent()
    
    print("=== 🎓 Education Assistant Agent Started ===")
    print("Simulating Teacher Interaction via Discord/Email...\n")

    # Scenario 1: Initial Setup (Teacher commands)
    commands = [
        "Add student Alice (alice@example.com)",
        "Add student Bob (bob@example.com)",
        "Add student Charlie (charlie@example.com)", 
    ]
    
    for cmd in commands:
        response = agent.process_teacher_command(cmd)
        print(response)

    # Manually update a student to have "needs_help" tag for demo
    import database_manager
    conn = database_manager.get_connection()
    # Assume Charlie (ID 3) needs help
    conn.execute("UPDATE students SET tags = 'needs_help' WHERE name = 'Charlie'")
    conn.commit()
    conn.close()
    print("ℹ️  [System] Simulating low quiz score for Charlie (Tag: 'needs_help' added)")

    # Scenario 2: Scheduling
    print("\n--- Teacher sets the schedule ---")
    print(agent.process_teacher_command("Schedule class on 2026-01-10 14:00 for Python Basics"))

    # Scenario 3: The "Monitor" wakes up and triggers Tutoring
    print("\n--- 🕒 8:00 AM Daily Check ---")
    monitor_logs = agent.run_daily_monitor()
    for log in monitor_logs:
        print(log) 
        # In a real app, the "Question" log would be sent as a DM to the student.

    # Scenario 4: Tutoring Interaction (Charlie responds)
    print("\n--- 💬 Student Interaction Simulation (Tutoring) ---")
    print("Simulating Student 'Charlie' (ID 3) replying to the AI Tutor...")
    
    # Charlie replies incorrectly first
    response1 = agent.process_student_message(3, "I think Python is a type of snake?")
    print(f"Charlie: I think Python is a type of snake?\nAgent: {response1}\n")

    # Charlie replies correctly (Simulated)
    # Note: Without a real LLM, the fallback response is static "I am unable to evaluate..."
    # If the user has an API key set, this will actually work!
    response2 = agent.process_student_message(3, "It is a programming language.")
    print(f"Charlie: It is a programming language.\nAgent: {response2}")

    # Scenario 5: Anonymous Feedback (Alice, ID 1)
    print("\n--- 💬 Student Interaction Simulation (Feedback) ---")
    print(agent.process_student_message(1, "The class speed is good."))

    # Teacher checks report
    print("\n--- 📋 Teacher checks reports ---")
    report_lines = agent.generate_feedback_report()
    for line in report_lines:
        print(line)

    print("\n=== Demo Complete ===")
    
if __name__ == "__main__":
    main()