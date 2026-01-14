from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, models, schemas
from app.database import get_db
from app.auth import get_current_active_user

router = APIRouter(prefix="/api", tags=["api"])

# Workspace routes
@router.post("/workspaces", response_model=schemas.Workspace)
async def create_workspace(
    workspace: schemas.WorkspaceCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new workspace"""
    return crud.create_workspace(db=db, workspace=workspace, owner_id=current_user.id)

@router.get("/workspaces", response_model=List[schemas.Workspace])
async def get_user_workspaces(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's workspaces"""
    return crud.get_user_workspaces(db=db, user_id=current_user.id)

@router.get("/workspaces/{workspace_id}", response_model=schemas.Workspace)
async def get_workspace(
    workspace_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get workspace by ID"""
    workspace = crud.get_workspace(db=db, workspace_id=workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

# Project routes
@router.post("/projects", response_model=schemas.Project)
async def create_project(
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new project"""
    # Verify user has access to workspace
    workspace = crud.get_workspace(db=db, workspace_id=project.workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    return crud.create_project(db=db, project=project)

@router.get("/workspaces/{workspace_id}/projects", response_model=List[schemas.Project])
async def get_workspace_projects(
    workspace_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get projects in a workspace"""
    return crud.get_projects_by_workspace(db=db, workspace_id=workspace_id)

# Meeting routes
@router.post("/meetings", response_model=schemas.Meeting)
async def create_meeting(
    meeting: schemas.MeetingCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new meeting"""
    # Verify user has access to project
    project = crud.get_project(db=db, project_id=meeting.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return crud.create_meeting(db=db, meeting=meeting, created_by_id=current_user.id)

@router.get("/projects/{project_id}/meetings", response_model=List[schemas.Meeting])
async def get_project_meetings(
    project_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get meetings in a project"""
    return crud.get_meetings_by_project(db=db, project_id=project_id)

@router.get("/meetings/{meeting_id}", response_model=schemas.Meeting)
async def get_meeting(
    meeting_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get meeting by ID"""
    meeting = crud.get_meeting(db=db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting

@router.put("/meetings/{meeting_id}", response_model=schemas.Meeting)
async def update_meeting(
    meeting_id: int,
    meeting_update: schemas.MeetingUpdate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update meeting"""
    meeting = crud.update_meeting(db=db, meeting_id=meeting_id, meeting_update=meeting_update)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting

# Meeting Notes routes
@router.get("/meetings/{meeting_id}/notes", response_model=List[schemas.MeetingNote])
async def get_meeting_notes(
    meeting_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get notes for a meeting"""
    return crud.get_meeting_notes(db=db, meeting_id=meeting_id)

@router.post("/meetings/{meeting_id}/notes", response_model=schemas.MeetingNote)
async def create_meeting_note(
    meeting_id: int,
    note: schemas.MeetingNoteCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a note for a meeting"""
    # Verify meeting exists
    meeting = crud.get_meeting(db=db, meeting_id=meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    return crud.create_meeting_note(db=db, note=note, created_by_id=current_user.id)

# Task routes
@router.post("/tasks", response_model=schemas.Task)
async def create_task(
    task: schemas.TaskCreate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new task"""
    return crud.create_task(db=db, task=task, created_by_id=current_user.id)

@router.get("/projects/{project_id}/tasks", response_model=List[schemas.Task])
async def get_project_tasks(
    project_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get tasks in a project"""
    return crud.get_tasks_by_project(db=db, project_id=project_id)

@router.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update task"""
    task = crud.update_task(db=db, task_id=task_id, task_update=task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task