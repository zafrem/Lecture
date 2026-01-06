**[🏠 Home](../../../README.md)** > **[AI](../../README.md)** > **[AI Agent](../README.md)** > **Education Assistant**

# Education Assistant Agent

This repository contains both the source code for the AI Agent and the educational materials used to teach how to build it.

## 📂 Structure

### [1. The Project (Source Code)](Project/)
The complete, working implementation of the Education Assistant.
- **Features**: Discord Bot, Email Integration, SQLite Database, Equity Monitor, **AI Tutoring**.
- **Tech Stack**: Python, discord.py, smtplib, sqlite3, **Ollama (Local LLM)**.

### [2. The Class (Tutorials)](Class/)
A step-by-step guide explaining the design and creation process of this agent.
- **Step 1**: [Concept & Architecture Design](Class/01_Concept_and_Design.md)
- **Step 2**: [Database & Memory](Class/02_Designing_Memory.md)
- **Step 3**: [Core Logic, Monitoring & Hybrid AI](Class/03_Building_the_Brain.md)
    - **Step 3b**: [Local LLMs & Ollama Guide](Class/03_b_Local_LLM_Guide.md)
    - **Step 3c**: [Cloud AI (Gemini/OpenAI) Guide](Class/03_c_Cloud_API_Guide.md)
- **Step 4**: [Interfaces (Discord/Email)](Class/04_Interfaces_and_Integration.md)
- **Step 5**: [Use Cases](Class/05_Use_Cases_and_Examples.md)
- **Step 6**: [Publishing to GitHub Pages](Class/06_Publishing_to_Github_Pages.md)

## 🎯 Goal
To promote educational equity by providing teachers with an AI Co-Pilot that handles logistics and ensures no student is neglected in large classes.
- **New**: Includes a local AI Tutor loop that proactively helps students struggling with concepts until they understand.