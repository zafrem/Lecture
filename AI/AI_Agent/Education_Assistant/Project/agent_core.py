import database_manager
import datetime
import re
import os
import json
import urllib.request
import urllib.error

# Try importing LLM libraries
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

class EducationAgent:
    def __init__(self):
        database_manager.init_db()
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.ollama_model = "llama3" # Fallback to user's requested model if needed

        if self.gemini_key and HAS_GEMINI:
            genai.configure(api_key=self.gemini_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        
        if self.openai_key and HAS_OPENAI:
            self.openai_client = openai.OpenAI(api_key=self.openai_key)

    def process_teacher_command(self, user_input):
        """
        Processes the teacher's command. 
        Prioritizes LLM (Gemini -> OpenAI -> Ollama) for natural language understanding.
        Falls back to Regex if no keys are found or LLM fails.
        """
        print(f"\n[Agent] Processing command: '{user_input}'")

        # 1. Try Gemini
        if self.gemini_key and HAS_GEMINI:
            try:
                print("[Agent] 🧠 Attempting to use Gemini...")
                response = self._query_gemini(user_input)
                result = self._execute_llm_action(response)
                if result: return result
            except Exception as e:
                print(f"[Agent] ⚠️ Gemini Error: {e}")

        # 2. Try OpenAI
        if self.openai_key and HAS_OPENAI:
            try:
                print("[Agent] 🧠 Attempting to use OpenAI...")
                response = self._query_openai(user_input)
                result = self._execute_llm_action(response)
                if result: return result
            except Exception as e:
                print(f"[Agent] ⚠️ OpenAI Error: {e}")

        # 3. Try Ollama (Local)
        try:
            print(f"[Agent] 🦙 Attempting to use Local Ollama ({self.ollama_model})...")
            response = self._query_ollama(user_input)
            result = self._execute_llm_action(response)
            if result: return result
        except Exception as e:
            print(f"[Agent] ⚠️ Ollama Error: {e}")

        # 4. Fallback to Regex
        print("[Agent] ⚙️ Falling back to Regex pattern matching...")
        return self._process_with_regex(user_input)

    def _get_system_prompt(self):
        return """
        You are an education assistant database interface. 
        Analyze the user's command and extract structured data in JSON format.
        Do not output markdown code blocks, just the raw JSON string.
        
        Supported Actions:
        1. Add Student
           - Keywords: "add student", "enroll", "register"
           - Required Output: {"intent": "add_student", "name": "String", "contact": "String (optional)"}
        
        2. Schedule Class
           - Keywords: "schedule", "class", "meet"
           - Required Output: {"intent": "schedule_class", "datetime": "YYYY-MM-DD HH:MM", "topic": "String"}
           - Note: Convert relative times (like "tomorrow at 2pm") to concrete dates assuming today is 2026-01-06.
        
        3. Assign Task
           - Keywords: "assign", "homework", "task"
           - Required Output: {"intent": "assign_task", "description": "String", "due_date": "YYYY-MM-DD"}
        
        If the intent is unclear, return {"intent": "unknown"}.
        """

    def _query_gemini(self, user_input):
        prompt = f"{self._get_system_prompt()}\nUser Input: {user_input}"
        response = self.gemini_model.generate_content(prompt)
        # Cleanup potential markdown formatting
        text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)

    def _query_openai(self, user_input):
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": user_input}
            ],
            temperature=0
        )
        text = response.choices[0].message.content.replace('```json', '').replace('```', '').strip()
        return json.loads(text)

    def _query_ollama(self, user_input):
        """
        Queries the local Ollama instance running on port 11434.
        """
        url = "http://localhost:11434/api/generate"
        prompt = f"{self._get_system_prompt()}\nUser Input: {user_input}\nResponse (JSON only):"
        
        data = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
            "format": "json" # Force JSON mode if model supports it
        }
        
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=2) as response:
            result = json.loads(response.read().decode('utf-8'))
            text = result.get('response', '').strip()
            # Simple cleanup just in case
            text = text.replace('```json', '').replace('```', '').strip()
            return json.loads(text)

    def _execute_llm_action(self, data):
        """
        Executes the database action based on the parsed JSON from LLM.
        """
        intent = data.get("intent")
        
        if intent == "add_student":
            name = data.get("name")
            contact = data.get("contact", "No contact")
            database_manager.add_student(name, contact)
            return f"✅ [AI] Added student: {name}"

        elif intent == "schedule_class":
            date_str = data.get("datetime")
            topic = data.get("topic")
            try:
                event_time = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                database_manager.add_schedule(event_time, topic)
                return f"✅ [AI] Class scheduled: '{topic}' at {event_time}"
            except ValueError:
                return f"❌ [AI] Error parsing date: {date_str}. Format required: YYYY-MM-DD HH:MM"

        elif intent == "assign_task":
            desc = data.get("description")
            date_str = data.get("due_date")
            try:
                due_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                database_manager.add_task(desc, due_date)
                return f"✅ [AI] Homework assigned: '{desc}' due {due_date.date()}"
            except ValueError:
                return f"❌ [AI] Error parsing date: {date_str}. Format required: YYYY-MM-DD"
        
        return None # Return None to trigger fallback if intent is unknown/null

    def _process_with_regex(self, user_input):
        """
        Original Regex logic for fallback.
        """
        # 1. Intent: Add Student
        match_student = re.search(r"add student\s+([a-zA-Z\s]+)(?:\((.*)\))?", user_input, re.IGNORECASE)
        if match_student:
            name = match_student.group(1).strip()
            contact = match_student.group(2) if match_student.group(2) else "No contact"
            database_manager.add_student(name, contact)
            return f"✅ Added student: {name}"

        # 2. Intent: Schedule Class
        match_schedule = re.search(r"schedule class on\s+([\d\-\s:]+)\s+for\s+(.*)", user_input, re.IGNORECASE)
        if match_schedule:
            date_str = match_schedule.group(1).strip()
            topic = match_schedule.group(2).strip()
            try:
                event_time = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                database_manager.add_schedule(event_time, topic)
                return f"✅ Class scheduled: '{topic}' at {event_time}"
            except ValueError:
                return "❌ Error: Date format should be YYYY-MM-DD HH:MM"

        # 3. Intent: Assign Homework
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
                
                # NEW LOGIC: Instead of sending a static "Pack", we initiate a tutoring session
                tutoring_topic = "General Review" # Ideally this would come from the tag, e.g. "needs_math_help" -> "Math"
                
                # Check if session already exists
                if not database_manager.get_active_tutoring_session(stu[0]):
                    # Start a new AI tutoring session
                    welcome_msg = self._generate_tutoring_question(tutoring_topic, is_start=True)
                    database_manager.start_tutoring_session(stu[0], tutoring_topic, welcome_msg)
                    logs.append(f"     🚀 Action: Initiated AI Tutoring Session for {stu[2]}")
                    logs.append(f"        Question: '{welcome_msg}'")
                else:
                    logs.append(f"     ℹ️  Student is already in an active tutoring session.")

                at_risk_count += 1
        
        if at_risk_count == 0:
            logs.append("  -> All students appear to be on track.")
            
        return logs

    def process_student_message(self, student_id, message):
        """
        Handles incoming messages from students.
        Checks if they are in a tutoring session. If so, engages the AI tutor.
        Otherwise, treats it as anonymous feedback.
        """
        # 1. Check for Active Tutoring Session
        session = database_manager.get_active_tutoring_session(student_id)
        if session:
            topic, context = session
            # Pass to AI Tutor Logic
            response = self._handle_tutoring_response(student_id, topic, context, message)
            return response

        # 2. Default: Anonymous Feedback
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

    def get_student_emails(self):
        """
        Retrieves all student emails for broadcasting.
        """
        return database_manager.get_all_emails()

    # --- AI Tutoring Logic ---

    def _handle_tutoring_response(self, student_id, topic, previous_context, student_message):
        """
        Evaluates the student's answer and determines the next step.
        """
        # Construct Prompt for LLM
        prompt = f"""
        You are a kind and patient AI Tutor teaching '{topic}'.
        
        Context (Last Question/State): {previous_context}
        Student Answer: {student_message}
        
        Task:
        1. Evaluate if the student's answer is correct or meaningful.
        2. If CORRECT/MEANINGFUL: Congratulate them warmly and end the session. Output prefix: [PASS]
        3. If INCORRECT/CONFUSED: Explain the concept simply, provide a hint, and ask a new related question. Output prefix: [FAIL]
        
        Keep your response short and encouraging (under 50 words).
        """
        
        response_text = ""
        # 1. Gemini
        if self.gemini_key and HAS_GEMINI:
            try:
                response = self.gemini_model.generate_content(prompt)
                response_text = response.text
            except: pass
        
        # 2. OpenAI
        if not response_text and self.openai_key and HAS_OPENAI:
            try:
                resp = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = resp.choices[0].message.content
            except: pass

        # 3. Ollama
        if not response_text:
            try:
                url = "http://localhost:11434/api/generate"
                data = {
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False
                }
                req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=2) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    response_text = result.get('response', '')
            except: pass
            
        if not response_text:
             # Fallback if no AI
            return "I am unable to evaluate your answer right now. Please check back later."

        # Parse AI Response
        if "[PASS]" in response_text:
            final_msg = response_text.replace("[PASS]", "").strip()
            database_manager.end_tutoring_session(student_id)
            # Optional: Remove 'needs_help' tag if we had logic for it
            return f"🎉 {final_msg}"
        else:
            next_msg = response_text.replace("[FAIL]", "").strip()
            database_manager.update_tutoring_context(student_id, next_msg)
            return next_msg

    def _generate_tutoring_question(self, topic, is_start=False):
        """
        Generates a question to start the session.
        """
        prompt = f"Generate a simple, engaging question to test a student's understanding of '{topic}'. Keep it short."
        
        # 1. Gemini
        if self.gemini_key and HAS_GEMINI:
            try:
                return self.gemini_model.generate_content(prompt).text.strip()
            except: pass
            
        # 2. OpenAI
        if self.openai_key and HAS_OPENAI:
            try:
                resp = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                return resp.choices[0].message.content.strip()
            except: pass

        # 3. Ollama
        try:
            url = "http://localhost:11434/api/generate"
            data = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False
            }
            req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=2) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('response', '').strip()
        except: pass

        return f"Please tell me what you know about {topic}?"