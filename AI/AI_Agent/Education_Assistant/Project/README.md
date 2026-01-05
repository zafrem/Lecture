# Education Assistant Agent

An AI-powered middleware designed to help teachers manage "one-to-many" classes effectively and equitably.

## 🌟 Key Features

### 1. Teacher Co-Pilot (Command Center)
- **Natural Language Interface**: Teachers can send commands like *"Schedule class on Friday at 2 PM"* or *"Add student Alice"*.
- **Task Management**: Automatically updates the database and schedule.

### 2. Equity Monitor (Student Guardian)
- **Automated Checks**: Runs daily scans to identify students falling behind or missing prerequisites.
- **Proactive Support**: Automatically distributes supplementary materials to "at-risk" students without waiting for teacher intervention.

### 3. Anonymous Feedback Bridge
- **Safe Space**: Students can send questions or concerns privately.
- **Anonymized Reporting**: The agent strips identifiers and aggregates messages for the teacher, encouraging honest feedback.

## 🛠️ Project Structure

- `main.py`: CLI simulation for testing the core logic without external dependencies.
- `agent_core.py`: The "Brain". Handles command parsing, monitoring logic, and database interactions.
- `discord_interface.py`: The "Front-End". A Discord Bot that connects teachers and students to the agent.
- `email_service.py`: The "Courier". Handles sending email notifications (Mock or SMTP).
- `database_manager.py`: The "Memory". SQLite database.
- `USE_CASES.md`: Detailed technical workflows and scenarios.

## 🚀 How to Run

### 1. Local Simulation (No Keys Required)
Run the CLI demo to see how the agent thinks and acts.
```bash
python3 main.py
```

### 2. Discord Bot (Requires Token)
To run the actual bot:
1.  Create a Bot on the [Discord Developer Portal](https://discord.com/developers/applications).
2.  Enable **Message Content Intent**.
3.  Get your **Token** and the **Channel ID** for the teacher's private channel.
4.  Run:
```bash
export DISCORD_TOKEN="your_token_here"
export TEACHER_CHANNEL_ID="1234567890"
python3 discord_interface.py
```

### 3. Email Configuration
To enable real emails (Gmail example):
```bash
export EMAIL_ADDRESS="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password" # Use App Password, not login password
```

## 🤖 Interaction Flow

### Teacher (via Discord Channel)
- **!agent Add student Alice (alice@gmail.com)** -> Agent adds Alice to DB.
- **!agent Schedule class on 2026-05-10 14:00 for History** -> Updates schedule.
- **!report** -> Shows anonymous feedback from students.

### Student (via Discord DM)
- **DM to Bot**: "I don't understand the last assignment."
- **Bot**: "Message received. The teacher will see this anonymously."
- **Agent**: Aggregates this into the `!report` for the teacher.

### Automated Equity Check
- The `daily_monitor_loop` runs every 24 hours.
- If a student is flagged as "needs_help", the Agent triggers `email_service` to send supplementary material.

## 📝 Example Commands

When running the interactive mode:
- `Add student John (john@example.com)`
- `Schedule class on 2026-02-15 10:00 for Advanced Math`
- `Assign task Read Chapter 5 by 2026-02-20`

## 🔮 Future Roadmap (Integration)
- **Discord Bot**: Connect `agent_core.py` to `discord.py` to handle real-time messages.
- **Email API**: Use Gmail API to send actual notifications.
- **LLM Integration**: Replace Regex parsing in `agent_core.py` with OpenAI/Gemini for robust natural language understanding.