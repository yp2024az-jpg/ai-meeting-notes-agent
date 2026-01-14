from typing import Dict, List, Set
import json
import logging
from fastapi import WebSocket
from app import models, schemas
from app.ai_service import ai_service

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # meeting_id -> set of websockets
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # websocket -> meeting_id
        self.connection_meetings: Dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket, meeting_id: int):
        """Connect a websocket to a meeting"""
        await websocket.accept()
        if meeting_id not in self.active_connections:
            self.active_connections[meeting_id] = set()
        self.active_connections[meeting_id].add(websocket)
        self.connection_meetings[websocket] = meeting_id
        logger.info(f"WebSocket connected to meeting {meeting_id}")

    def disconnect(self, websocket: WebSocket):
        """Disconnect a websocket"""
        meeting_id = self.connection_meetings.get(websocket)
        if meeting_id and meeting_id in self.active_connections:
            self.active_connections[meeting_id].discard(websocket)
            if not self.active_connections[meeting_id]:
                del self.active_connections[meeting_id]
        if websocket in self.connection_meetings:
            del self.connection_meetings[websocket]
        logger.info(f"WebSocket disconnected from meeting {meeting_id}")

    async def broadcast_to_meeting(self, meeting_id: int, message: Dict):
        """Broadcast message to all connections in a meeting"""
        if meeting_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[meeting_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.warning(f"Failed to send message to connection: {e}")
                    disconnected.add(connection)

            # Clean up disconnected connections
            for conn in disconnected:
                self.disconnect(conn)

    async def send_personal_message(self, websocket: WebSocket, message: Dict):
        """Send message to a specific websocket"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.warning(f"Failed to send personal message: {e}")
            self.disconnect(websocket)

class MeetingManager:
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        # meeting_id -> meeting data
        self.active_meetings: Dict[int, Dict] = {}

    async def start_meeting(self, meeting_id: int, meeting_data: Dict):
        """Start a meeting session"""
        self.active_meetings[meeting_id] = {
            "data": meeting_data,
            "transcript": [],
            "participants": set(),
            "start_time": meeting_data.get("start_time")
        }

        await self.connection_manager.broadcast_to_meeting(
            meeting_id,
            {
                "type": "meeting_started",
                "meeting_id": meeting_id,
                "data": meeting_data
            }
        )

    async def add_transcript(self, meeting_id: int, transcript_data: Dict):
        """Add transcript to meeting"""
        if meeting_id not in self.active_meetings:
            return

        meeting = self.active_meetings[meeting_id]
        meeting["transcript"].append(transcript_data)

        # Broadcast to all participants
        await self.connection_manager.broadcast_to_meeting(
            meeting_id,
            {
                "type": "transcript",
                "data": transcript_data
            }
        )

    async def generate_summary(self, meeting_id: int) -> str:
        """Generate AI summary for meeting"""
        if meeting_id not in self.active_meetings:
            return "Meeting not found"

        meeting = self.active_meetings[meeting_id]
        transcript_text = "\n".join([t.get("text", "") for t in meeting["transcript"]])

        if not transcript_text:
            return "No transcript available for summarization."

        summary = await ai_service.generate_summary(transcript_text)

        # Broadcast summary to participants
        await self.connection_manager.broadcast_to_meeting(
            meeting_id,
            {
                "type": "summary",
                "data": {
                    "summary": summary,
                    "meeting_id": meeting_id
                }
            }
        )

        return summary

    async def extract_action_items(self, meeting_id: int) -> List[Dict]:
        """Extract action items from meeting"""
        if meeting_id not in self.active_meetings:
            return []

        meeting = self.active_meetings[meeting_id]
        transcript_text = "\n".join([t.get("text", "") for t in meeting["transcript"]])

        if not transcript_text:
            return []

        action_items = await ai_service.extract_action_items(transcript_text)

        # Broadcast action items to participants
        await self.connection_manager.broadcast_to_meeting(
            meeting_id,
            {
                "type": "action_items",
                "data": {
                    "action_items": action_items,
                    "meeting_id": meeting_id
                }
            }
        )

        return action_items

    async def end_meeting(self, meeting_id: int):
        """End a meeting session"""
        if meeting_id in self.active_meetings:
            meeting_data = self.active_meetings[meeting_id]

            # Generate final summary and insights
            transcript_text = "\n".join([t.get("text", "") for t in meeting_data["transcript"]])

            if transcript_text:
                # Generate comprehensive insights
                insights = await ai_service.generate_meeting_insights(transcript_text)

                await self.connection_manager.broadcast_to_meeting(
                    meeting_id,
                    {
                        "type": "meeting_ended",
                        "data": {
                            "meeting_id": meeting_id,
                            "insights": insights,
                            "final_summary": await ai_service.generate_summary(transcript_text)
                        }
                    }
                )

            del self.active_meetings[meeting_id]

# Global instances
connection_manager = ConnectionManager()
meeting_manager = MeetingManager(connection_manager)