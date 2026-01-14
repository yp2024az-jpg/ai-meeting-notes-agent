import os
import json
from typing import List, Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "")
        self.model = None
        if self.google_api_key:
            try:
                self.model = ChatGoogleGenerativeAI(model='gemini-2.5-pro')
            except Exception as e:
                logger.warning(f"Failed to initialize AI model: {e}")

    async def generate_summary(self, transcript: str, meeting_type: str = "general") -> str:
        """Generate meeting summary using AI"""
        if not self.model:
            return "AI model not available. Please configure GOOGLE_API_KEY."

        try:
            prompt = f"""Please provide a comprehensive summary of this {meeting_type} meeting transcript:

Transcript:
{transcript}

Please structure your summary to include:
1. Main topics discussed
2. Key decisions made
3. Important outcomes or next steps

Summary:"""

            response = self.model.invoke(prompt)
            if hasattr(response, 'content'):
                return response.content
            elif isinstance(response, dict) and 'content' in response:
                return response['content']
            else:
                return str(response)
        except Exception as e:
            logger.exception("Error generating summary")
            return f"Error generating summary: {e}"

    async def extract_action_items(self, transcript: str, summary: Optional[str] = None) -> List[Dict[str, Any]]:
        """Extract action items from meeting transcript"""
        if not self.model:
            return []

        try:
            context = f"Summary: {summary}\n\n" if summary else ""
            prompt = f"""{context}Please analyze this meeting transcript and extract all action items, tasks, and follow-ups mentioned:

Transcript:
{transcript}

Please return a JSON array of action items with the following structure:
[
  {{
    "title": "Action item title",
    "description": "Detailed description",
    "assignee": "Person responsible (if mentioned)",
    "due_date": "Due date (if mentioned)",
    "priority": "high/medium/low"
  }}
]

Only return the JSON array, no additional text."""

            response = self.model.invoke(prompt)
            content = ""
            if hasattr(response, 'content'):
                content = response.content
            elif isinstance(response, dict) and 'content' in response:
                content = response['content']
            else:
                content = str(response)

            # Try to parse JSON
            try:
                # Clean the response to extract JSON
                content = content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()

                action_items = json.loads(content)
                return action_items if isinstance(action_items, list) else []
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse AI response as JSON: {content}")
                return []

        except Exception as e:
            logger.exception("Error extracting action items")
            return []

    async def analyze_sentiment(self, transcript: str) -> Dict[str, Any]:
        """Analyze sentiment of the meeting"""
        if not self.model:
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

            response = self.model.invoke(prompt)
            content = ""
            if hasattr(response, 'content'):
                content = response.content
            elif isinstance(response, dict) and 'content' in response:
                content = response['content']
            else:
                content = str(response)

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
        if not self.model:
            return []

        try:
            prompt = f"""Identify the main topics discussed in this meeting transcript.
Return a JSON array of topic strings.

Transcript:
{transcript}

Return only the JSON array of topics."""

            response = self.model.invoke(prompt)
            content = ""
            if hasattr(response, 'content'):
                content = response.content
            elif isinstance(response, dict) and 'content' in response:
                content = response['content']
            else:
                content = str(response)

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
        if not self.model:
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

            response = self.model.invoke(prompt)
            content = ""
            if hasattr(response, 'content'):
                content = response.content
            elif isinstance(response, dict) and 'content' in response:
                content = response['content']
            else:
                content = str(response)

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