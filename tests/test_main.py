"""
Tests for AI Meeting Notes Agent
"""

import pytest 
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app, MeetingNotesManager
import json

def test_meeting_notes_manager():
    """Test the MeetingNotesManager class"""
    manager = MeetingNotesManager()

    # Test initial state
    assert manager.notes == []
    assert manager.current_meeting is None
    assert manager.start_time is None

    # Test starting meeting
    manager.start_meeting("Test Meeting")
    assert manager.current_meeting == "Test Meeting"
    assert manager.start_time is not None

    # Test adding notes
    manager.add_note("10:00:00", "Speaker 1", "Hello world")
    assert len(manager.notes) == 1
    assert manager.notes[0]["text"] == "Hello world"
    assert manager.notes[0]["speaker"] == "Speaker 1"
    assert manager.notes[0]["type"] == "transcript"

    # Test adding summary
    manager.add_summary("This is a summary")
    assert len(manager.notes) == 2
    assert manager.notes[1]["text"] == "This is a summary"
    assert manager.notes[1]["type"] == "summary"

    # Test getting notes
    notes = manager.get_notes()
    assert len(notes) == 2
    assert notes[0]["text"] == "Hello world"
    assert notes[1]["text"] == "This is a summary"

def test_app_creation():
    """Test that the FastAPI app is created correctly"""
    assert app.title == "AI Meeting Notes Agent"
    assert app.version == "1.0.0"

    # Check that routes exist
    routes = [route.path for route in app.routes]
    assert "/" in routes
    assert "/api/notes" in routes
    assert "/ws/transcript" in routes

def test_environment_variables():
    """Test that environment variables are loaded"""
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    assert api_key is not None
    assert len(api_key) > 0

def test_google_ai_initialization():
    """Test that Google AI is initialized"""
    import langchain_google_genai as ChatGoogleGenerativeAI
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    # Re-initialize to test
    model=ChatGoogleGenerativeAI(model='gemini-2.5-pro')
    assert model is not None

# Integration tests would go here when server is running
# - Test HTTP endpoints with requests library
# - Test WebSocket connections
# - Test full transcription workflow