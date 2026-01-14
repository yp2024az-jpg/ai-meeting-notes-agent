from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    workspaces = relationship("Workspace", back_populates="owner")
    workspace_memberships = relationship("WorkspaceMember", back_populates="user")

class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="workspaces")
    members = relationship("WorkspaceMember", back_populates="workspace")
    projects = relationship("Project", back_populates="workspace")

class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, default="member")  # owner, admin, member
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    workspace = relationship("Workspace", back_populates="members")
    user = relationship("User", back_populates="workspace_memberships")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    color = Column(String, default="#667eea")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    workspace = relationship("Workspace", back_populates="projects")
    meetings = relationship("Meeting", back_populates="project")

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    duration = Column(Float)  # in minutes
    status = Column(String, default="scheduled")  # scheduled, in_progress, completed, cancelled
    meeting_type = Column(String, default="general")  # general, standup, retrospective, client_call, etc.
    transcript = Column(Text)
    summary = Column(Text)
    action_items = Column(JSON)  # Store as JSON array
    participants = Column(JSON)  # Store as JSON array of user IDs
    tags = Column(JSON)  # Store as JSON array
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="meetings")
    created_by = relationship("User")
    notes = relationship("MeetingNote", back_populates="meeting")

class MeetingNote(Base):
    __tablename__ = "meeting_notes"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    speaker = Column(String)
    content = Column(Text, nullable=False)
    note_type = Column(String, default="transcript")  # transcript, summary, action_item, decision
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    meeting = relationship("Meeting", back_populates="notes")
    created_by = relationship("User")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"))
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=True)  # If created from meeting
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="todo")  # todo, in_progress, done, cancelled
    priority = Column(String, default="medium")  # low, medium, high, urgent
    due_date = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    tags = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    project = relationship("Project")
    meeting = relationship("Meeting")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    created_by = relationship("User", foreign_keys=[created_by_id])

class MeetingTemplate(Base):
    __tablename__ = "meeting_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    template_type = Column(String, nullable=False)  # standup, retrospective, planning, etc.
    agenda_items = Column(JSON)  # Pre-defined agenda items
    duration_minutes = Column(Integer, default=60)
    participant_roles = Column(JSON)  # Expected roles/participants
    created_by_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    workspace = relationship("Workspace")
    created_by = relationship("User")