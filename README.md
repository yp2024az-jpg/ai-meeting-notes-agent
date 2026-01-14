# 🤖 AI Meeting Notes Agent - ClickUp Style Platform

A comprehensive AI-powered meeting management platform inspired by ClickUp, featuring real-time transcription, AI summarization, task management, and collaborative workspaces.

## ✨ Features

### Core Features
- **Real-time Speech-to-Text Transcription**: Browser-based speech recognition with live transcription
- **AI-Powered Analysis**: Automatic meeting summaries, action item extraction, and insights
- **Multi-user Collaboration**: Real-time WebSocket-based collaboration during meetings
- **Project Management**: Organize meetings within projects and workspaces
- **Task Integration**: Convert meeting action items into assignable tasks
- **Advanced AI Features**:
  - Sentiment analysis
  - Topic detection
  - Action item extraction
  - Meeting insights and recommendations

### User Management
- **Authentication System**: JWT-based authentication with secure password hashing
- **Role-based Access Control**: Workspace owners, admins, and members
- **Multi-tenant Architecture**: Isolated workspaces for different teams/organizations

### Meeting Features
- **Meeting Types**: Support for different meeting formats (standups, retrospectives, client calls, etc.)
- **Participant Management**: Track meeting attendees and roles
- **Meeting Templates**: Pre-configured templates for common meeting types
- **Time Tracking**: Automatic meeting duration calculation
- **Meeting History**: Complete archive of past meetings with search

### Dashboard & Analytics
- **Comprehensive Dashboard**: Overview of meetings, tasks, and team productivity
- **Real-time Statistics**: Live updates on meeting status and completion
- **Team Insights**: Analytics on meeting effectiveness and participation
- **Export Capabilities**: Export transcripts, notes, and reports

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Google AI API key (for AI features)

### Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd ai-meeting-notes-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment setup**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Database setup**:
   ```bash
   # Create PostgreSQL database
   createdb meeting_notes

   # Run database migrations
   alembic upgrade head

   # Initialize with demo data
   python init_db.py
   ```

5. **Start the application**:
   ```bash
   python main.py
   ```

6. **Access the application**:
   - Open http://localhost:8000 in your browser
   - Login with demo credentials: `demo` / `demo123`

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/meeting_notes

# Authentication
SECRET_KEY=your-super-secret-key-change-this-in-production

# AI Integration
GOOGLE_API_KEY=your-google-api-key-here

# Application
DEBUG=True
```

### Database Configuration

The application uses PostgreSQL. Make sure to:
1. Install PostgreSQL
2. Create a database named `meeting_notes`
3. Update the `DATABASE_URL` in your `.env` file

## 📁 Project Structure

```
ai-meeting-notes-agent/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Database operations
│   ├── auth.py              # Authentication utilities
│   ├── ai_service.py        # AI integration service
│   ├── websocket_manager.py # WebSocket management
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication routes
│       ├── api.py           # REST API routes
│       └── websocket.py     # WebSocket routes
├── templates/
│   ├── login.html           # Login/register page
│   ├── dashboard.html       # Main dashboard
│   ├── meeting.html         # Meeting interface
│   └── index.html           # Legacy interface
├── static/                  # Static files (CSS, JS, images)
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── main.py                  # Application entry point
├── init_db.py               # Database initialization
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── alembic.ini              # Alembic configuration
└── README.md
```

## 🔑 API Documentation

Once the application is running, visit:
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📝 Key Differences from Original Version

This version transforms the basic AI Meeting Notes Agent into a comprehensive platform:

### Architecture Changes
- **Database**: Moved from in-memory storage to PostgreSQL with SQLAlchemy
- **Authentication**: Added JWT-based user authentication and authorization
- **Multi-tenancy**: Support for multiple workspaces and users
- **Real-time Collaboration**: WebSocket-based real-time updates

### New Features
- **User Management**: Registration, login, and user profiles
- **Workspace Management**: Create and manage isolated workspaces
- **Project Organization**: Group meetings within projects
- **Task Management**: Create and assign tasks from meeting action items
- **Advanced AI**: Sentiment analysis, topic detection, comprehensive insights
- **Dashboard**: Comprehensive overview with statistics and analytics

### UI/UX Improvements
- **Modern Dashboard**: ClickUp-inspired interface with tabs and cards
- **Meeting Interface**: Enhanced meeting view with sidebar for notes and insights
- **Responsive Design**: Mobile-friendly design
- **Real-time Updates**: Live updates during meetings

## 🔒 Security

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Secure token-based authentication
- **Input Validation**: Comprehensive input validation with Pydantic
- **CORS Configuration**: Properly configured CORS for security

## 🚀 Deployment

### Production Deployment

1. **Set DEBUG=False** in your environment
2. **Use a production WSGI server** (gunicorn, uvicorn with workers)
3. **Configure a reverse proxy** (nginx recommended)
4. **Set up SSL/TLS** certificates
5. **Configure proper database credentials**
6. **Set up monitoring and logging**

### Docker Deployment

```dockerfile
# Example Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN alembic upgrade head

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API documentation at `/docs`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Demo Credentials:**
- Username: `demo`
- Password: `demo123`

Start exploring the platform by logging in with these credentials!