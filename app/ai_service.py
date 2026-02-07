import os
import json
from typing import List, Dict, Any, Optional
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.groq_api_key = os.getenv("Groq_api_key", "")
        self.client = None
        if self.groq_api_key:
            try:
                self.client = Groq(api_key=self.groq_api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Groq client: {e}")

    async def generate_summary(self, transcript: str, meeting_type: str = "general") -> str:
        """Generate meeting summary using AI"""
        if not self.client:
            return "AI model not available. Please configure Groq API key."

        try:
            prompt = f"""Please provide a comprehensive summary of this {meeting_type} meeting transcript:

Transcript:
{transcript}

Please structure your summary to include:
1. Main topics discussed
2. Key decisions made
3. Important outcomes or next steps

Summary:"""

            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2048
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.exception("Error generating summary")
            return f"Error generating summary: {e}"

    async def extract_action_items(self, transcript: str, summary: Optional[str] = None) -> List[Dict[str, Any]]:
        """Extract action items from meeting transcript"""
        if not self.client:
            logger.error("Groq client not initialized")
            return []

        if not transcript or len(transcript.strip()) < 10:
            logger.warning("Transcript too short to extract action items")
            return []

        try:
            context = f"Summary: {summary}\n\n" if summary else ""
            prompt = f"""{context}Extract action items from this meeting transcript. Return ONLY valid JSON array, no markdown, no extra text.

Transcript:
{transcript}

JSON format:
[
  {{"title": "Task title", "description": "Details", "assignee": "Person", "due_date": "Date", "priority": "high/medium/low"}}
]"""

            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1024
            )
            content = response.choices[0].message.content.strip()

            # Clean JSON response
            content = content.replace("```json", "").replace("```", "").strip()
            
            if not content or content == "[]":
                logger.info("No action items found in transcript")
                return []

            action_items = json.loads(content)
            
            if not isinstance(action_items, list):
                logger.warning(f"Expected list, got {type(action_items)}")
                return []
                
            logger.info(f"Extracted {len(action_items)} action items")
            return action_items

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}. Content: {content}")
            return []
        except Exception as e:
            logger.exception("Error extracting action items")
            return []

    async def analyze_sentiment(self, transcript: str) -> Dict[str, Any]:
        """Analyze sentiment of the meeting"""
        if not self.client:
            return {"overall": "neutral", "confidence": 0}

        try:
            prompt = f"""Analyze the sentiment of this meeting transcript and provide:
1. Overall sentiment (positive/negative/neutral)
2. Confidence score (0-1)
3. Key positive aspects
4. Key concerns or negative aspects

Transcript:
{transcript}

Return as JSON with keys: overall, confidence, positive_aspects, concerns"""

            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2048
            )
            content = response.choices[0].message.content

            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                return {"overall": "neutral", "confidence": 0.5}

        except Exception as e:
            logger.exception("Error analyzing sentiment")
            return {"overall": "neutral", "confidence": 0}

    async def identify_topics(self, transcript: str) -> List[str]:
        """Identify main topics discussed in the meeting"""
        if not self.client:
            return []

        try:
            prompt = f"""Identify the main topics discussed in this meeting transcript.
Return a JSON array of topic strings.

Transcript:
{transcript}

Return only the JSON array of topics."""

            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2048
            )
            content = response.choices[0].message.content

            try:
                topics = json.loads(content)
                return topics if isinstance(topics, list) else []
            except json.JSONDecodeError:
                return []

        except Exception as e:
            logger.exception("Error identifying topics")
            return []

    async def generate_meeting_insights(self, transcript: str, summary: str = None) -> Dict[str, Any]:
        """Generate comprehensive meeting insights"""
        if not self.client:
            return {}

        try:
            context = f"Summary: {summary}\n\n" if summary else ""
            prompt = f"""{context}Provide comprehensive insights for this meeting transcript:

Transcript:
{transcript}

Return a JSON object with:
- key_decisions: array of key decisions made
- risks_identified: array of risks or concerns raised
- unanswered_questions: array of open questions
- recommendations: array of recommendations or suggestions
- follow_up_needed: boolean indicating if follow-up meeting is needed"""

            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2048
            )
            content = response.choices[0].message.content

            try:
                insights = json.loads(content)
                return insights
            except json.JSONDecodeError:
                return {}

        except Exception as e:
            logger.exception("Error generating insights")
            return {}

# Global AI service instance
ai_service = AIService()