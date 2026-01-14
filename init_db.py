#!/usr/bin/env python3
"""
Database initialization script
Creates demo user and sample data for the AI Meeting Notes Agent
"""

import os
import sys
from sqlalchemy.orm import Session

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.database import SessionLocal, engine
from app import models, schemas, auth, crud
from datetime import datetime

def init_db():
    """Initialize the database with demo data"""

    # Create tables
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Create demo user
        demo_user = crud.get_user_by_username(db, username="demo")
        if not demo_user:
            demo_user_data = {
                "email": "demo@example.com",
                "username": "demo",
                "full_name": "Demo User",
                "password": "123"
            }
            demo_user = crud.create_user(db, schemas.UserCreate(**demo_user_data))
            print("Created demo user")

        # Create demo workspace
        demo_workspace = crud.get_workspaces_by_owner(db, demo_user.id)
        if not demo_workspace:
            workspace_data = {
                "name": "Demo Workspace",
                "description": "A demo workspace for testing the AI Meeting Notes Agent"
            }
            demo_workspace = crud.create_workspace(db, schemas.WorkspaceCreate(**workspace_data), demo_user.id)
            print("Created demo workspace")

        # Create demo project
        demo_projects = crud.get_projects_by_workspace(db, demo_workspace.id)
        if not demo_projects:
            project_data = {
                "name": "Demo Project",
                "description": "A demo project for testing meetings and tasks",
                "workspace_id": demo_workspace.id,
                "color": "#667eea"
            }
            demo_project = crud.create_project(db, schemas.ProjectCreate(**project_data))
            print("Created demo project")

            # Create demo meeting
            meeting_data = {
                "title": "Welcome Meeting",
                "description": "Introduction to the AI Meeting Notes Agent platform",
                "project_id": demo_project.id,
                "meeting_type": "general",
                "status": "completed",
                "transcript": "Welcome to the AI Meeting Notes Agent! This is a demo meeting to showcase the platform's capabilities.",
                "summary": "This was an introductory meeting demonstrating the AI Meeting Notes Agent platform features.",
                "action_items": [
                    {
                        "title": "Explore dashboard features",
                        "description": "Take time to explore all the dashboard features",
                        "assignee": "demo",
                        "priority": "medium"
                    }
                ]
            }
            demo_meeting = crud.create_meeting(db, schemas.MeetingCreate(**meeting_data), demo_user.id)
            print("Created demo meeting")

            # Create demo task
            task_data = {
                "title": "Complete platform onboarding",
                "description": "Explore all features of the AI Meeting Notes Agent platform",
                "project_id": demo_project.id,
                "assigned_to_id": demo_user.id,
                "priority": "medium",
                "status": "todo"
            }
            demo_task = crud.create_task(db, schemas.TaskCreate(**task_data), demo_user.id)
            print("Created demo task")

        print("Database initialization completed successfully!")
        print("\nDemo Credentials:")
        print("Username: demo")
        print("Password: demo123")
        print("\nYou can now start the application with: python main.py")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()