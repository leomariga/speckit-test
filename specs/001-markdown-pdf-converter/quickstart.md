# Quickstart Guide: Markdown to PDF Converter

**Created**: 2025-01-27  
**Purpose**: Get the application running locally for development

## Prerequisites

- Docker and Docker Compose installed
- Node.js 18+ (for local frontend development, optional)
- Python 3.11+ (for local backend development, optional)
- uv package manager installed (`pip install uv`)

## Quick Start with Docker

### 1. Clone and Navigate

```bash
cd /path/to/project
git checkout 001-markdown-pdf-converter
```

### 2. Start Services

```bash
docker-compose up --build
```

This starts:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **MongoDB**: localhost:27017
- **API Docs**: http://localhost:8000/docs (Swagger UI)

### 3. Access the Application

Open http://localhost:3000 in your browser.

## Local Development Setup

### Backend Setup

```bash
cd backend
uv init
uv add fastapi uvicorn motor python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv
uv sync
```

Create `.env` file:
```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=markdown_pdf
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
SECRET_KEY=your-secret-key-for-sessions
```

Run backend:
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
```

Create `.env` file:
```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_GOOGLE_CLIENT_ID=your-google-client-id
```

Run frontend:
```bash
npm run dev
```

### MongoDB Setup (if not using Docker)

```bash
docker run -d --name mongodb -p 27017:27017 mongo:7.0
```

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/api/v1/auth/google/callback`
5. Copy Client ID and Client Secret to `.env` files

## First Use

1. **Register/Login**: Click "Sign in with Gmail" on the login page
2. **Convert Markdown**: 
   - Paste markdown text or upload a `.md` file
   - Click "Convert to PDF"
   - Download the generated PDF
3. **Check Account**: View your usage and plan limits on the account page

## Testing the API

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

### Convert Markdown (requires authentication)

```bash
# First, authenticate via browser (OAuth flow)
# Then use session cookie:

curl -X POST http://localhost:8000/api/v1/conversions \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your-session-cookie" \
  -d '{
    "input_type": "text",
    "markdown_text": "# Hello World\n\nThis is a test."
  }' \
  --output output.pdf
```

## Project Structure

```
backend/
├── src/app/          # FastAPI application
├── tests/            # Test files
└── pyproject.toml    # uv dependencies

frontend/
├── src/              # Vue 3 application
├── tests/            # Test files
└── package.json      # npm dependencies
```

## Common Tasks

### Run Tests

**Backend**:
```bash
cd backend
uv run pytest
```

**Frontend**:
```bash
cd frontend
npm test
```

### View API Documentation

Open http://localhost:8000/docs for interactive Swagger UI.

### Reset Database

```bash
docker-compose down -v
docker-compose up
```

### View Logs

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Troubleshooting

### MongoDB Connection Error

- Ensure MongoDB is running: `docker ps | grep mongo`
- Check `MONGODB_URI` in `.env` file
- Verify network connectivity between services

### OAuth Redirect Error

- Check redirect URI matches Google Cloud Console settings
- Ensure `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are correct
- Verify callback URL is accessible

### PDF Generation Fails

- Check browser console for client-side errors
- Verify backend logs for server-side errors
- Ensure markdown content is valid
- Try smaller document first

### Port Already in Use

- Change ports in `docker-compose.yml`
- Or stop conflicting services: `docker-compose down`

## Next Steps

- Read [spec.md](./spec.md) for feature requirements
- Review [data-model.md](./data-model.md) for data structure
- Check [contracts/openapi.yaml](./contracts/openapi.yaml) for API details
- See [research.md](./research.md) for technical decisions

