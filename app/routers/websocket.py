from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..websocket_manager import meeting_manager
from .. import crud, models, auth
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws/meeting/{meeting_id}")
async def meeting_websocket(
    websocket: WebSocket,
    meeting_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time meeting collaboration"""

    # Authenticate user from token
    try:
        current_user = auth.get_current_user(token=token, db=db)
        if not current_user or not current_user.is_active:
            await websocket.close(code=1008)  # Policy violation
            return
    except Exception as e:
        logger.warning(f"WebSocket authentication failed: {e}")
        await websocket.close(code=1008)
        return

    # Verify user has access to meeting
    meeting = crud.get_meeting(db=db, meeting_id=meeting_id)
    if not meeting:
        await websocket.close(code=1003)  # Unsupported data
        return

    # Check if user is participant or meeting creator
    has_access = (
        meeting.created_by_id == current_user.id or
        current_user.id in (meeting.participants or [])
    )
    if not has_access:
        await websocket.close(code=1008)
        return

    # Connect to meeting
    await meeting_manager.connection_manager.connect(websocket, meeting_id)

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()

            message_type = data.get("type")

            if message_type == "start_meeting":
                # Start meeting session
                await meeting_manager.start_meeting(meeting_id, data.get("data", {}))

            elif message_type == "transcript":
                # Add transcript to meeting
                transcript_data = {
                    "text": data.get("text", ""),
                    "speaker": data.get("speaker", current_user.username),
                    "timestamp": data.get("timestamp"),
                    "user_id": current_user.id
                }
                await meeting_manager.add_transcript(meeting_id, transcript_data)

            elif message_type == "generate_summary":
                # Generate AI summary
                summary = await meeting_manager.generate_summary(meeting_id)
                await meeting_manager.connection_manager.send_personal_message(
                    websocket,
                    {
                        "type": "summary_generated",
                        "data": {"summary": summary}
                    }
                )

            elif message_type == "extract_action_items":
                # Extract action items
                action_items = await meeting_manager.extract_action_items(meeting_id)
                await meeting_manager.connection_manager.send_personal_message(
                    websocket,
                    {
                        "type": "action_items_extracted",
                        "data": {"action_items": action_items}
                    }
                )

            elif message_type == "end_meeting":
                # End meeting
                await meeting_manager.end_meeting(meeting_id)

            elif message_type == "ping":
                # Keep-alive ping
                await meeting_manager.connection_manager.send_personal_message(
                    websocket,
                    {"type": "pong"}
                )

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for meeting {meeting_id}")
    except Exception as e:
        logger.exception(f"WebSocket error for meeting {meeting_id}: {e}")
    finally:
        meeting_manager.connection_manager.disconnect(websocket)