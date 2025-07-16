#!/usr/bin/env python3
"""
Test script for the Medication Management SMS API
This allows you to test the message parsing and medication management logic
without setting up Twilio.
"""

import requests
import json
from datetime import datetime

# Test the API locally
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_medication_management():
    """Test medication management functionality"""
    print("💊 Testing medication management...")

    # Test phone number
    test_phone = "+1234567890"

    # Test adding medications
    print("1. Adding medications...")
    add_commands = [
        "ADD aspirin 81mg daily",
        "ADD metformin 500mg twice daily",
        "ADD blood pressure med 10mg morning"
    ]

    for command in add_commands:
        print(f"   Testing: {command}")
        # Simulate the webhook call
        response = requests.post(
            f"{BASE_URL}/webhook/sms",
            data={
                "Body": command,
                "From": test_phone,
                "To": "+0987654321"
            }
        )
        print(f"   Response: {response.text}")

    print()

    # Test taking medications
    print("2. Taking medications...")
    take_commands = [
        "TAKE aspirin",
        "I took my metformin",
        "Just took blood pressure med"
    ]

    for command in take_commands:
        print(f"   Testing: {command}")
        response = requests.post(
            f"{BASE_URL}/webhook/sms",
            data={
                "Body": command,
                "From": test_phone,
                "To": "+0987654321"
            }
        )
        print(f"   Response: {response.text}")

    print()

    # Test viewing information
    print("3. Viewing information...")
    view_commands = ["LIST", "TODAY", "HELP"]

    for command in view_commands:
        print(f"   Testing: {command}")
        response = requests.post(
            f"{BASE_URL}/webhook/sms",
            data={
                "Body": command,
                "From": test_phone,
                "To": "+0987654321"
            }
        )
        print(f"   Response: {response.text}")

    print()

def test_debug_endpoints():
    """Test the debug endpoints"""
    print("🔧 Testing debug endpoints...")

    test_phone = "+1234567890"

    # Test medications endpoint
    print("1. Testing medications endpoint...")
    response = requests.get(f"{BASE_URL}/medications/{test_phone}")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")

    print()

    # Test logs endpoint
    print("2. Testing logs endpoint...")
    response = requests.get(f"{BASE_URL}/logs/{test_phone}")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")

    print()

def simulate_conversation():
    """Simulate a real conversation with the medication system"""
    print("💬 Simulating a conversation...")
    print("=" * 50)

    test_phone = "+1234567890"

    conversation = [
        ("Hi there!", "Unknown command"),
        ("HELP", "Help message"),
        ("ADD aspirin 81mg daily", "Add medication"),
        ("ADD metformin 500mg twice daily", "Add medication"),
        ("LIST", "List medications"),
        ("TAKE aspirin", "Take medication"),
        ("I took my metformin", "Take medication"),
        ("TODAY", "Today's logs"),
        ("TAKE something not in my list", "Error handling"),
        ("HELP", "Help message again")
    ]

    for i, (message, description) in enumerate(conversation, 1):
        print(f"{i}. User: {message}")
        print(f"   ({description})")

        response = requests.post(
            f"{BASE_URL}/webhook/sms",
            data={
                "Body": message,
                "From": test_phone,
                "To": "+0987654321"
            }
        )

        # Extract the message from TwiML response
        response_text = response.text
        if "<Message>" in response_text and "</Message>" in response_text:
            start = response_text.find("<Message>") + 9
            end = response_text.find("</Message>")
            message_content = response_text[start:end]
        else:
            message_content = response_text

        print(f"   System: {message_content}")
        print()

def main():
    """Run all tests"""
    print("🚀 Starting Medication Management SMS API Tests")
    print("=" * 60)

    try:
        # Test health endpoint
        test_health()

        # Test medication management
        test_medication_management()

        # Test debug endpoints
        test_debug_endpoints()

        # Simulate conversation
        simulate_conversation()

        print("✅ All tests completed!")

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("   Make sure the server is running with: python app.py")
        print("   Or: uvicorn app:app --reload --host 0.0.0.0 --port 8000")

    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    main()
