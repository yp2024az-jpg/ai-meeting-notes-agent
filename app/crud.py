from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import models, schemas, auth
from typing import List, Optional
from datetime import datetime

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Workspace CRUD operations
def get_workspace(db: Session, workspace_id: int):
    return db.query(models.Workspace).filter(models.Workspace.id == workspace_id).first()

def get_workspaces_by_owner(db: Session, owner_id: int):
    return db.query(models.Workspace).filter(models.Workspace.owner_id == owner_id).all()

def get_user_workspaces(db: Session, user_id: int):
    return db.query(models.Workspace).join(models.WorkspaceMember).filter(
        and_(
            models.WorkspaceMember.user_id == user_id,
            models.WorkspaceMember.workspace_id == models.Workspace.id
        )
    ).all()

def create_workspace(db: Session, workspace: schemas.WorkspaceCreate, owner_id: int):
    db_workspace = models.Workspace(**workspace.dict(), owner_id=owner_id)
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)

    # Add owner as workspace member
    db_member = models.WorkspaceMember(
        workspace_id=db_workspace.id,
        user_id=owner_id,
        role="owner"
    )
    db.add(db_member)
    db.commit()

    return db_workspace

# Project CRUD operations
def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects_by_workspace(db: Session, workspace_id: int):
    return db.query(models.Project).filter(models.Project.workspace_id == workspace_id).all()

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# Meeting CRUD operations
def get_meeting(db: Session, meeting_id: int):
    return db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()

def get_meetings_by_project(db: Session, project_id: int):
    return db.query(models.Meeting).filter(models.Meeting.project_id == project_id).all()

def get_user_meetings(db: Session, user_id: int):
    return db.query(models.Meeting).filter(models.Meeting.created_by_id == user_id).all()

def create_meeting(db: Session, meeting: schemas.MeetingCreate, created_by_id: int):
    db_meeting = models.Meeting(**meeting.dict(), created_by_id=created_by_id)
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting

def update_meeting(db: Session, meeting_id: int, meeting_update: schemas.MeetingUpdate):
    db_meeting = db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()
    if db_meeting:
        update_data = meeting_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_meeting, field, value)
        db.commit()
        db.refresh(db_meeting)
    return db_meeting

# Meeting Note CRUD operations
def get_meeting_notes(db: Session, meeting_id: int):
    return db.query(models.MeetingNote).filter(models.MeetingNote.meeting_id == meeting_id).all()

def create_meeting_note(db: Session, note: schemas.MeetingNoteCreate, created_by_id: int):
    db_note = models.MeetingNote(**note.dict(), created_by_id=created_by_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# Task CRUD operations
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks_by_project(db: Session, project_id: int):
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()

def get_tasks_by_assigned_user(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.assigned_to_id == user_id).all()

def create_task(db: Session, task: schemas.TaskCreate, created_by_id: int):
    db_task = models.Task(**task.dict(), created_by_id=created_by_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_task, field, value)
        db.commit()
        db.refresh(db_task)
    return db_task