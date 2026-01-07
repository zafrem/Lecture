**[🏠 Home](../../../../README.md)** > **[AI](../../../README.md)** > **[AI Agent](../../README.md)** > **[Education Assistant](../README.md)** > **[Class](README.md)** > **Step 4**

# Step 4: Connecting to the World (Interfaces)

A brain in a jar is useless. Our agent needs to talk to people where they are: **Discord** and **Email**.

## 1. The Discord Bot (The "Face")
Discord is the main interface because it supports:
-   **Commands**: `!agent Add student...` (Public/Teacher channel).
-   **Privacy**: Students can DM the bot, and the bot keeps secrets (Anonymous Feedback).

### Event-Driven Programming
Discord bots work on "Events":
-   `on_ready()`: When the bot starts.
-   `on_message(msg)`: When someone types something.

**The Workflow:**
1.  User types `!agent ...`
2.  `discord_interface.py` catches it.
3.  It passes the text to `agent_core.py`.
4.  `agent_core` returns a string.
5.  `discord_interface` sends it back to the channel.

## 2. The Email Service (The "Courier")
Sometimes you need to send a formal file or a long guide. Discord might not be best for that.
We create a separate module `email_service.py` so the Agent can say:
> "Send 'Math_Guide.pdf' to Alice."

And the service handles the SMTP (Simple Mail Transfer Protocol) details.

## 3. Putting it All Together (`main.py`)
To test without setting up Discord servers every time, we use `main.py`.
It **simulates** the world:
1.  It pretends to be a teacher typing commands.
2.  It pretends to be the clock moving forward (triggering the Monitor).
3.  It pretends to be a student sending a DM.

## 4. Educational Goal
By building this, you learn:
-   **API Integration**: Using `discord.py` and `smtplib`.
-   **Modularity**: Separating "Logic" (Agent) from "Input/Output" (Discord/CLI).
-   **Simulation**: How to test complex systems locally.
