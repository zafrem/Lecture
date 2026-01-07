**[🏠 Home](../../../../README.md)** > **[AI](../../../README.md)** > **[AI Agent](../../README.md)** > **[Education Assistant](../README.md)** > **[Class](README.md)** > **Step 1**

# Step 1: Concept & Design

## 1. The Problem: The "One-to-Many" Dilemma
In a typical classroom, one teacher manages 20-30 students. It is physically impossible to:
- Remind every student individually about their missing homework.
- Notice immediately when a specific student's grade drops slightly.
- Listen to the private concerns of every shy student.

## 2. The Solution: The AI Co-Pilot
We don't want to replace the teacher. We want to give the teacher a "Secretary" or "Co-Pilot" that handles the repetitive logistics and monitoring.

### The Role of the Agent
1.  **The Secretary (Teacher-facing)**: Takes quick commands ("Schedule class", "Remind everyone").
2.  **The Guardian (Student-facing)**: Watches over student progress and sends help when needed.
3.  **The Bridge**: Allows students to speak anonymously to the teacher.

## 3. Architecture Design
Before writing code, we must design the system components.

```mermaid
graph TD
    Teacher -- "Natural Language" --> AgentCore
    Student -- "DM/Feedback" --> AgentCore
    
    subgraph "The Agent"
        AgentCore[Logic Core (Brain)]
        Database[(SQLite Memory)]
        Monitor[Daily Monitor Loop]
    end
    
    AgentCore -- "Read/Write" --> Database
    Monitor -- "Check Status" --> Database
    
    Monitor -- "Send Email" --> EmailService
    AgentCore -- "Reply" --> DiscordBot
```

### Key Components
-   **Memory (Database)**: Where do we store the list of students and the schedule?
-   **Brain (Agent Core)**: How do we understand "Add student Alice"?
-   **Mouth (Interfaces)**: How does the agent talk? (Discord, Email, CLI).

## 4. Design Decisions
-   **Why Python?**: Easy to write, huge ecosystem for AI and APIs.
-   **Why SQLite?**: Simple file-based database, perfect for learning and prototypes.
-   **Why Discord?**: Teachers and students are already there. It supports real-time chat and private DMs.
