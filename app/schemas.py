from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Workspace schemas
class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkspaceCreate(WorkspaceBase):
    pass

class Workspace(WorkspaceBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = "#667eea"

class ProjectCreate(ProjectBase):
    workspace_id: int

class Project(ProjectBase):
    id: int
    workspace_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Meeting schemas
class MeetingBase(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: int
    start_time: Optional[datetime] = None
    meeting_type: Optional[str] = "general"
    participants: Optional[List[int]] = []
    tags: Optional[List[str]] = []

class MeetingCreate(MeetingBase):
    pass

class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    end_time: Optional[datetime] = None
    transcript: Optional[str] = None
    summary: Optional[str] = None
    action_items: Optional[List[Dict[str, Any]]] = None

class Meeting(MeetingBase):
    id: int
    created_by_id: int
    end_time: Optional[datetime]
    duration: Optional[float]
    status: str
    transcript: Optional[str]
    summary: Optional[str]
    action_items: Optional[List[Dict[str, Any]]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Meeting Note schemas
class MeetingNoteBase(BaseModel):
    content: str
    note_type: Optional[str] = "transcript"
    speaker: Optional[str] = None

class MeetingNoteCreate(MeetingNoteBase):
    meeting_id: int

class MeetingNote(MeetingNoteBase):
    id: int
    meeting_id: int
    timestamp: datetime
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to_id: Optional[int] = None
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = []

class TaskCreate(TaskBase):
    project_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None

class Task(TaskBase):
    id: int
    project_id: int
    meeting_id: Optional[int]
    created_by_id: int
    status: str
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# WebSocket schemas
class WebSocketMessage(BaseModel):
    type: str
    data: Dict[str, Any]

class TranscriptMessage(BaseModel):
    text: str
    timestamp: Optional[str] = None
    speaker: Optional[str] = "Speaker"

class SummaryRequest(BaseModel):
    meeting_id: int

# AI Enhancement schemas
class AISummaryRequest(BaseModel):
    transcript: str
    meeting_type: Optional[str] = "general"

class AIActionItemsRequest(BaseModel):
    transcript: str
    summary: Optional[str] = None

class AIResponse(BaseModel):
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None