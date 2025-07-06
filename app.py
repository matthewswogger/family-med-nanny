from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import re
from typing import Optional
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Medication Management SMS API", version="1.0.0")

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# In-memory storage (replace with database in production)
medications = {}
medication_logs = []
users = {}

class MedicationManager:
    def __init__(self):
        self.medications = {}
        self.logs = []
        self.users = {}
    
    def add_medication(self, phone_number: str, name: str, dosage: str, frequency: str):
        """Add a new medication for a user"""
        if phone_number not in self.medications:
            self.medications[phone_number] = []
        
        medication = {
            "name": name.lower(),
            "dosage": dosage,
            "frequency": frequency,
            "added_date": datetime.now()
        }
        
        self.medications[phone_number].append(medication)
        return f"Added {name} ({dosage}) - {frequency}"
    
    def log_medication_taken(self, phone_number: str, medication_name: str):
        """Log that a medication was taken"""
        if phone_number not in self.medications:
            return "No medications found. Use ADD to add medications first."
        
        med_name = medication_name.lower()
        user_meds = self.medications[phone_number]
        
        # Find the medication
        medication = None
        for med in user_meds:
            if med_name in med["name"] or med["name"] in med_name:
                medication = med
                break
        
        if not medication:
            return f"Medication '{medication_name}' not found. Your medications: {', '.join([m['name'] for m in user_meds])}"
        
        # Log the dose
        log_entry = {
            "phone_number": phone_number,
            "medication": medication["name"],
            "dosage": medication["dosage"],
            "taken_at": datetime.now()
        }
        
        self.logs.append(log_entry)
        return f"✅ Logged: {medication['name'].title()} ({medication['dosage']}) taken at {datetime.now().strftime('%I:%M %p')}"
    
    def list_medications(self, phone_number: str):
        """List all medications for a user"""
        if phone_number not in self.medications or not self.medications[phone_number]:
            return "No medications found. Use ADD to add medications first."
        
        meds = self.medications[phone_number]
        response = "📋 Your Medications:\n"
        for i, med in enumerate(meds, 1):
            response += f"{i}. {med['name'].title()} - {med['dosage']} ({med['frequency']})\n"
        return response
    
    def list_today_logs(self, phone_number: str):
        """List today's medication logs"""
        today = datetime.now().date()
        today_logs = [log for log in self.logs 
                     if log["phone_number"] == phone_number 
                     and log["taken_at"].date() == today]
        
        if not today_logs:
            return "No medications taken today yet."
        
        response = "📅 Today's Medications:\n"
        for log in today_logs:
            time_str = log["taken_at"].strftime("%I:%M %p")
            response += f"✅ {log['medication'].title()} ({log['dosage']}) at {time_str}\n"
        return response
    
    def help_message(self):
        """Return help message with available commands"""
        return """💊 Medication Management Commands:

ADD [medication] [dosage] [frequency]
Example: ADD aspirin 81mg daily

TAKE [medication]
Example: TAKE aspirin

LIST - Show all your medications
TODAY - Show today's taken medications
HELP - Show this help message

Examples:
- "ADD metformin 500mg twice daily"
- "TAKE blood pressure med"
- "I took my insulin"
- "Just took aspirin" """

# Initialize medication manager
med_manager = MedicationManager()

def parse_message(message: str) -> dict:
    """Parse incoming SMS message and extract intent"""
    message = message.strip().upper()
    
    # Handle natural language
    if any(word in message for word in ["TOOK", "TAKEN", "JUST TOOK", "TOOK MY"]):
        # Extract medication name from natural language
        words = message.split()
        medication_words = []
        for word in words:
            if word not in ["I", "TOOK", "MY", "JUST", "THE", "A", "AN"]:
                medication_words.append(word)
        return {
            "action": "TAKE",
            "medication": " ".join(medication_words).lower()
        }
    
    # Handle structured commands
    if message.startswith("ADD "):
        parts = message[4:].split()
        if len(parts) >= 3:
            dosage = parts[-2]
            frequency = parts[-1]
            medication = " ".join(parts[:-2])
            return {
                "action": "ADD",
                "medication": medication.lower(),
                "dosage": dosage,
                "frequency": frequency
            }
    
    elif message.startswith("TAKE "):
        medication = message[5:].lower()
        return {
            "action": "TAKE",
            "medication": medication
        }
    
    elif message == "LIST":
        return {"action": "LIST"}
    
    elif message == "TODAY":
        return {"action": "TODAY"}
    
    elif message == "HELP":
        return {"action": "HELP"}
    
    # Default: try to extract medication name for taking
    return {
        "action": "TAKE",
        "medication": message.lower()
    }

@app.post("/webhook/sms")
async def handle_sms_webhook(
    request: Request,
    Body: str = Form(...),
    From: str = Form(...),
    To: str = Form(...)
):
    """Handle incoming SMS messages from Twilio"""
    try:
        logger.info(f"Received SMS from {From}: {Body}")
        
        # Parse the message
        parsed = parse_message(Body)
        
        # Process the action
        if parsed["action"] == "ADD":
            response = med_manager.add_medication(
                From, 
                parsed["medication"], 
                parsed["dosage"], 
                parsed["frequency"]
            )
        elif parsed["action"] == "TAKE":
            response = med_manager.log_medication_taken(
                From, 
                parsed["medication"]
            )
        elif parsed["action"] == "LIST":
            response = med_manager.list_medications(From)
        elif parsed["action"] == "TODAY":
            response = med_manager.list_today_logs(From)
        elif parsed["action"] == "HELP":
            response = med_manager.help_message()
        else:
            response = "I didn't understand that. Send HELP for available commands."
        
        # Create TwiML response
        twiml = MessagingResponse()
        twiml.message(response)
        
        logger.info(f"Sending response to {From}: {response}")
        
        return PlainTextResponse(str(twiml), media_type="text/xml")
        
    except Exception as e:
        logger.error(f"Error processing SMS: {e}")
        twiml = MessagingResponse()
        twiml.message("Sorry, there was an error processing your message. Please try again.")
        return PlainTextResponse(str(twiml), media_type="text/xml")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Medication Management SMS API is running", "status": "healthy"}

@app.get("/medications/{phone_number}")
async def get_medications(phone_number: str):
    """Get medications for a phone number (for debugging)"""
    if phone_number not in med_manager.medications:
        return {"medications": []}
    return {"medications": med_manager.medications[phone_number]}

@app.get("/logs/{phone_number}")
async def get_logs(phone_number: str):
    """Get medication logs for a phone number (for debugging)"""
    user_logs = [log for log in med_manager.logs if log["phone_number"] == phone_number]
    return {"logs": user_logs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 