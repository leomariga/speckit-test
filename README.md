# Markdown to PDF Converter

A minimalist web application for converting markdown content to print-ready PDF documents with Gmail OAuth authentication and usage-based plans.

## Features

✅ **Markdown to PDF Conversion** (User Story 1 - P1)
- Paste markdown text or upload .md files
- Client-side PDF generation with print-ready styling
- Support for headers, lists, code blocks, tables, and more
- Download generated PDFs instantly

✅ **Gmail OAuth Authentication** (User Story 2 - P2)
- Secure sign-in with Google/Gmail accounts
- Session management with httpOnly cookies
- User registration and login flows

✅ **Plan-Based Usage Limits** (User Story 3 - P3)
- Free plan: Up to 20 pages
- Premium plan: 20-500 pages
- Real-time usage tracking
- Account dashboard with conversion history

## Tech Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Fast build tool
- **Pinia** - State management
- **TypeScript** - Type safety
- **markdown-it** - Markdown parsing
- **html2pdf.js** - Client-side PDF generation

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - Document database
- **Motor** - Async MongoDB driver
- **uv** - Fast Python package manager
- **Google OAuth 2.0** - Authentication

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Google OAuth credentials (for authentication features)

### 1. Clone and Setup

```bash
git checkout 001-markdown-pdf-converter
```

### 2. Configure Environment

Create `.env` files (optional - app works with defaults):

**Backend** (`backend/.env`):
```env
MONGODB_URI=mongodb://mongodb:27017
MONGODB_DB=markdown_pdf
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FRONTEND_URL=http://localhost:3000
```

**Frontend** (`frontend/.env`):
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

### 3. Start Services

```bash
docker-compose up --build
```

Services will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MongoDB**: localhost:27017

### 4. Google OAuth Setup (Optional)

For authentication features to work:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable Google+ API
3. Create OAuth 2.0 credentials
4. Add redirect URI: `http://localhost:8000/api/v1/auth/google/callback`
5. Copy credentials to `.env` files

## Project Structure

```
backend/
├── src/app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   ├── api/v1/              # API endpoints
│   └── db/                  # Database models
├── tests/                   # Test files
└── pyproject.toml           # uv dependencies

frontend/
├── src/
│   ├── components/          # Vue components
│   ├── pages/               # Page components
│   ├── services/            # API clients
│   ├── stores/              # Pinia stores
│   └── router/              # Vue Router
├── tests/                   # Test files
└── package.json             # npm dependencies

docker-compose.yml           # Service orchestration
```

## API Endpoints

### Health
- `GET /api/v1/health` - Health check

### Authentication
- `GET /api/v1/auth/google` - Initiate OAuth
- `GET /api/v1/auth/google/callback` - OAuth callback
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout

### Conversions
- `POST /api/v1/conversions` - Track conversion
- `GET /api/v1/conversions/history` - Get history

### Users
- `GET /api/v1/users/account` - Get account info

## Development

### Backend Development

```bash
cd backend
uv init
uv add fastapi uvicorn motor
uv run uvicorn src.app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Run Tests

```bash
# Backend
cd backend
uv run pytest

# Frontend
cd frontend
npm test
```

## Constitution Compliance

This project follows the Web Application Constitution (v1.0.0):

✅ **Security & Authentication**: Gmail OAuth with httpOnly cookies  
✅ **API Design Standards**: RESTful API with versioning (`/api/v1/`)  
✅ **Testing Requirements**: Integration and contract tests ready  
✅ **Versioning**: Semantic versioning (MAJOR.MINOR.PATCH)  
✅ **Observability**: Request logging, error tracking, health endpoints  
✅ **Security**: Input validation, CSRF protection, rate limiting ready

## Implementation Status

- ✅ **Phase 1**: Setup (9 tasks) - Complete
- ✅ **Phase 2**: Foundational (13 tasks) - Complete
- ✅ **Phase 3**: User Story 1 - Convert Markdown to PDF (14 tasks) - Complete
- ✅ **Phase 4**: User Story 2 - Gmail OAuth (17 tasks) - Complete
- ✅ **Phase 5**: User Story 3 - Plan Limits (19 tasks) - Complete
- ✅ **Phase 6**: Polish & Cross-Cutting (18 tasks) - Complete

**Total**: 90/90 tasks complete (100%) ✨

## License

MIT

## Documentation

Full documentation available in `/specs/001-markdown-pdf-converter/`:
- `spec.md` - Feature specification
- `plan.md` - Implementation plan
- `research.md` - Technical research
- `data-model.md` - Data models
- `contracts/openapi.yaml` - API specification
- `quickstart.md` - Detailed setup guide
- `tasks.md` - Task breakdown

