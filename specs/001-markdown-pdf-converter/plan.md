# Implementation Plan: Markdown to PDF Converter

**Branch**: `001-markdown-pdf-converter` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-markdown-pdf-converter/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

A minimalist web application enabling users to convert markdown content to print-ready PDF documents. The application provides user authentication via Gmail OAuth, plan-based usage limits (free: <20 pages, premium: 20-500 pages), and a straightforward conversion interface supporting both text input and file upload. Technical approach: Vue 3 frontend with client-side PDF generation capability, FastAPI backend with uv package management, MongoDB for data persistence, all containerized with Docker.

## Technical Context

**Language/Version**: Python 3.11+ (backend), JavaScript/TypeScript (frontend)  
**Primary Dependencies**: FastAPI, Vue 3, MongoDB, uv (Python package manager), Docker  
**Storage**: MongoDB (Docker container) for user accounts, conversion history, plan tracking  
**Testing**: pytest (backend), Vitest/Jest (frontend), contract tests for API endpoints  
**Target Platform**: Web browsers (modern browsers with ES6+ support), Linux containers (Docker)  
**Project Type**: web (frontend + backend architecture)  
**Performance Goals**: 
- PDF conversion completes in under 30 seconds for documents up to 50 pages (SC-001)
- System handles 100 concurrent conversion requests without degradation (SC-006)
- 95% conversion success rate (SC-002)
**Constraints**: 
- Client-side PDF generation is feasible using html2pdf.js with backend fallback for quality/complexity
- Print-ready PDF formatting requirements (headers, lists, code blocks, tables) via CSS print media queries
- Plan limit enforcement must be accurate (100% compliance per SC-004) - requires PDF page count, not estimation
**Scale/Scope**: 
- Initial target: 1000 users
- Free plan users: <20 pages per account
- Premium plan users: 20-500 pages per account
- 3 main pages: conversion interface, registration/login, account dashboard

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Security & Authentication (NON-NEGOTIABLE)
✅ **PASS**: Gmail OAuth authentication will be implemented for all user-facing endpoints. Sensitive operations (plan limit checks, conversion tracking) require authenticated users. HTTPS will be enforced in production. User inputs (markdown text/files) will be validated and sanitized. OAuth tokens will be stored securely (httpOnly cookies). Session management with proper expiration will be implemented.

### II. API Design Standards
✅ **PASS**: RESTful API design with consistent naming conventions (nouns for resources, HTTP verbs for actions). Standard HTTP status codes will be used. Structured error responses with appropriate status codes. API versioning will be implemented in URL path (`/api/v1/`). Request/response payloads will be validated using Pydantic models (FastAPI) and TypeScript interfaces (Vue 3).

### III. Testing Requirements
✅ **PASS**: Integration tests will cover critical user journeys (conversion flow, authentication flow, plan limit enforcement). API contract tests will validate request/response schemas. Authentication and authorization flows will have dedicated test coverage. Tests will be independently runnable with isolated test data (MongoDB test database, mocked OAuth).

### IV. Versioning & Breaking Changes
✅ **PASS**: API versioning will follow semantic versioning (MAJOR.MINOR.PATCH). Breaking changes will require MAJOR version increment. API versions will be specified in URL path (`/api/v1/`). Deprecated endpoints will be marked with migration guidance. Backward compatibility will be maintained within the same MAJOR version.

### V. Observability
✅ **PASS**: All API requests will be logged with request ID, timestamp, user context, and response status. Errors will be logged with sufficient context (stack traces, request parameters, user ID). Application health endpoints will be exposed (`/health`, `/api/v1/health`). Critical business operations (conversions, plan limit checks) will emit structured events for analytics.

### Security Requirements
✅ **PASS**: User data (email, plan type, page counts) will be encrypted at rest in MongoDB. Database access will use parameterized queries (Motor async driver). XSS protection via Content Security Policy and input sanitization. CSRF protection for state-changing operations. Rate limiting for authentication endpoints and conversion API.

### Development Workflow
✅ **PASS**: Feature specification documented in `spec.md`. Implementation plan documented in `plan.md`. Code reviews will verify constitution compliance. Breaking API changes will be documented with migration guides. Deployment will include rollback procedures (Docker container rollback).

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration management
│   │   ├── models/                 # Pydantic models
│   │   │   ├── user.py
│   │   │   ├── conversion.py
│   │   │   └── plan.py
│   │   ├── services/               # Business logic
│   │   │   ├── auth_service.py     # Gmail OAuth handling
│   │   │   ├── conversion_service.py # Conversion tracking
│   │   │   └── plan_service.py     # Plan limit enforcement
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py         # Authentication endpoints
│   │   │       ├── conversions.py  # Conversion endpoints
│   │   │       └── users.py        # User account endpoints
│   │   └── db/
│   │       └── mongodb.py           # MongoDB connection and models
│   ├── pyproject.toml              # uv project configuration
│   └── Dockerfile
├── tests/
│   ├── contract/                   # API contract tests
│   ├── integration/                # Integration tests
│   └── unit/                       # Unit tests
└── docker-compose.yml              # Local development setup

frontend/
├── src/
│   ├── main.ts                     # Vue 3 application entry
│   ├── App.vue                     # Root component
│   ├── components/                 # Reusable Vue components
│   │   ├── MarkdownEditor.vue
│   │   ├── PdfViewer.vue
│   │   └── FileUpload.vue
│   ├── pages/                      # Page components
│   │   ├── ConvertPage.vue         # Main conversion interface
│   │   ├── LoginPage.vue           # Gmail OAuth login
│   │   ├── RegisterPage.vue        # User registration
│   │   └── AccountPage.vue         # Account dashboard
│   ├── services/                   # API clients and utilities
│   │   ├── api.ts                  # API client
│   │   ├── auth.ts                 # Authentication service
│   │   └── pdf.ts                  # PDF generation service (client-side)
│   ├── stores/                     # State management (Pinia)
│   │   ├── auth.ts
│   │   └── conversion.ts
│   └── router/                      # Vue Router configuration
│       └── index.ts
├── package.json
├── vite.config.ts
├── Dockerfile
└── tests/
    ├── unit/                       # Component unit tests
    └── integration/                # E2E tests

docker-compose.yml                  # Production orchestration
```

**Structure Decision**: Web application structure with separate frontend (Vue 3) and backend (FastAPI) directories. This separation enables independent development, deployment, and scaling. MongoDB runs in a Docker container. The frontend includes client-side PDF generation capability to reduce backend load, with backend primarily handling authentication, plan enforcement, and conversion tracking.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
