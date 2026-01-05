import discord
from discord.ext import commands, tasks
import os
import agent_core
import email_service

# Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_BOT_TOKEN_HERE")
TEACHER_CHANNEL_ID = int(os.getenv("TEACHER_CHANNEL_ID", 123456789)) # Channel where teacher sends commands

# Intents (Required for reading message content)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
agent = agent_core.EducationAgent()

@bot.event
async def on_ready():
    print(f'🤖 Bot connected as {bot.user}')
    daily_monitor_loop.start()

@bot.event
async def on_message(message):
    # Ignore own messages
    if message.author == bot.user:
        return

    # 1. Student DM Handling (Anonymous Feedback)
    if isinstance(message.channel, discord.DMChannel):
        # We assume anyone DMing the bot is a student for this prototype
        # In production, we'd check their role in the server
        response = agent.process_student_message(message.author.id, message.content)
        await message.channel.send(response)
        
        # Notify teacher channel that feedback arrived
        channel = bot.get_channel(TEACHER_CHANNEL_ID)
        if channel:
            await channel.send("📩 New anonymous feedback received. Type `!report` to view.")
        return

    # Process commands
    await bot.process_commands(message)

# --- Teacher Commands ---

@bot.command(name="agent")
async def process_natural_language(ctx, *, user_input):
    """
    Teacher sends natural language command.
    Usage: !agent Add student Alice (alice@example.com)
    """
    if ctx.channel.id != TEACHER_CHANNEL_ID:
        return # Restrict to teacher channel

    response = agent.process_teacher_command(user_input)
    await ctx.send(response)

@bot.command(name="report")
async def show_report(ctx):
    """
    Show anonymous feedback report.
    """
    if ctx.channel.id != TEACHER_CHANNEL_ID:
        return

    lines = agent.generate_feedback_report()
    report_text = "\n".join(lines)
    await ctx.send(f"```\n{report_text}\n```")

@bot.command(name="email_all")
async def email_students(ctx, subject, *, body):
    """
    Send email to all students.
    Usage: !email_all "Homework 1" Please complete Chapter 1.
    """
    # This requires adding a 'get_all_emails' to agent/db
    # For now, we mock it
    await ctx.send(f"📧 Sending email '{subject}' to all students (Mock)...")
    email_service.send_email("all_students@class.com", subject, body)

# --- Background Tasks ---

@tasks.loop(hours=24)
async def daily_monitor_loop():
    """
    Runs the monitor agent daily and posts alerts to the teacher channel.
    """
    channel = bot.get_channel(TEACHER_CHANNEL_ID)
    if not channel:
        return

    logs = agent.run_daily_monitor()
    if logs:
        text = "\n".join(logs)
        await channel.send(f"**🕒 Daily Monitor Report**\n```\n{text}\n```")

if __name__ == "__main__":
    if DISCORD_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ Error: Please set DISCORD_TOKEN environment variable.")
    else:
        bot.run(DISCORD_TOKEN)
