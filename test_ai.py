#!/usr/bin/env python3
"""
Test script to check AI service functionality
"""

import os
from dotenv import load_dotenv
load_dotenv()

from app.ai_service import ai_service

async def test_ai_service():
    print("Testing AI Service...")

    # Check if client is initialized
    if ai_service.client is None:
        print("❌ Groq client not initialized. Check your Groq_api_key in .env file")
        print(f"Groq API key found: {'Yes' if os.getenv('Groq_api_key') else 'No'}")
        return

    print("✅ Groq client initialized successfully")

    # Test with a simple prompt
    try:
        print("Testing generate_summary...")
        summary = await ai_service.generate_summary("Hello world meeting")
        print(f"Summary result: {summary}")
        if summary and summary != "AI model not available. Please configure Groq API key.":
            print("✅ AI service working correctly")
        else:
            print("❌ AI service not working")
    except Exception as e:
        print(f"❌ Error testing AI service: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_ai_service())
