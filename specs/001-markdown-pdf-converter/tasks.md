# Tasks: Markdown to PDF Converter

**Input**: Design documents from `/specs/001-markdown-pdf-converter/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT included as they were not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths follow the structure defined in plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure (backend/src/app/, backend/tests/)
- [x] T002 Create frontend directory structure (frontend/src/, frontend/tests/)
- [x] T003 [P] Initialize backend Python project with uv in backend/pyproject.toml
- [x] T004 [P] Initialize frontend Vue 3 project with Vite in frontend/
- [x] T005 [P] Create backend Dockerfile in backend/Dockerfile
- [x] T006 [P] Create frontend Dockerfile in frontend/Dockerfile
- [x] T007 Create docker-compose.yml at repository root for orchestration
- [x] T008 [P] Configure backend linting (ruff) in backend/pyproject.toml
- [x] T009 [P] Configure frontend linting (ESLint) in frontend/.eslintrc.js

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T010 Setup MongoDB connection in backend/src/app/db/mongodb.py
- [x] T011 [P] Create backend configuration management in backend/src/app/config.py
- [x] T012 [P] Create frontend configuration in frontend/src/config.ts
- [x] T013 [P] Setup FastAPI application structure in backend/src/app/main.py
- [x] T014 [P] Setup Vue 3 application entry in frontend/src/main.ts
- [x] T015 [P] Create Vue Router configuration in frontend/src/router/index.ts
- [x] T016 [P] Setup Pinia stores structure in frontend/src/stores/
- [x] T017 [P] Create API versioning middleware in backend/src/app/api/v1/__init__.py
- [x] T018 [P] Implement error handling middleware in backend/src/app/middleware/error_handler.py
- [x] T019 [P] Setup request logging middleware in backend/src/app/middleware/logging.py
- [x] T020 [P] Create health check endpoint in backend/src/app/api/v1/health.py
- [x] T021 [P] Create base API client in frontend/src/services/api.ts
- [x] T022 Setup CORS configuration in backend/src/app/main.py for frontend access

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Convert Markdown to PDF (Priority: P1) 🎯 MVP

**Goal**: Enable users to convert markdown content (text or file) to print-ready PDF documents with client-side generation.

**Independent Test**: A user can paste markdown text or upload a file, click convert, and download the resulting PDF. The PDF contains the expected content formatted appropriately for printing.

### Implementation for User Story 1

- [x] T023 [P] [US1] Install markdown parsing library (markdown-it) in frontend/package.json
- [x] T024 [P] [US1] Install PDF generation library (html2pdf.js) in frontend/package.json
- [x] T025 [P] [US1] Create MarkdownEditor component in frontend/src/components/MarkdownEditor.vue
- [x] T026 [P] [US1] Create FileUpload component in frontend/src/components/FileUpload.vue
- [x] T027 [P] [US1] Create PdfViewer component in frontend/src/components/PdfViewer.vue
- [x] T028 [US1] Create PDF generation service in frontend/src/services/pdf.ts with markdown-to-PDF conversion logic
- [x] T029 [US1] Create print-ready CSS stylesheet in frontend/src/styles/print.css with @media print rules
- [x] T030 [US1] Create ConvertPage component in frontend/src/pages/ConvertPage.vue with text input and file upload
- [x] T031 [US1] Integrate MarkdownEditor, FileUpload, and PDF generation in ConvertPage.vue
- [x] T032 [US1] Add PDF download functionality in ConvertPage.vue
- [x] T033 [US1] Add error handling for invalid markdown and conversion failures in frontend/src/services/pdf.ts
- [x] T034 [US1] Add progress indicator for long conversions in ConvertPage.vue
- [x] T035 [US1] Create Conversion Pydantic model in backend/src/app/models/conversion.py (for future tracking)
- [x] T036 [US1] Add route for ConvertPage in frontend/src/router/index.ts

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can convert markdown to PDF without authentication.

---

## Phase 4: User Story 2 - User Registration and Gmail Login (Priority: P2)

**Goal**: Enable users to create accounts and sign in using Gmail OAuth authentication.

**Independent Test**: A new user can click register, authenticate with Gmail, and successfully access their account dashboard. An existing user can log in with Gmail and access their account.

### Implementation for User Story 2

- [x] T037 [P] [US2] Install Google OAuth libraries in backend (google-auth, google-auth-oauthlib) via uv
- [x] T038 [P] [US2] Create User MongoDB model in backend/src/app/db/models/user.py
- [x] T039 [P] [US2] Create User Pydantic model in backend/src/app/models/user.py
- [x] T040 [US2] Create auth service in backend/src/app/services/auth_service.py with Gmail OAuth flow
- [x] T041 [US2] Implement OAuth initiation endpoint in backend/src/app/api/v1/auth.py (GET /auth/google)
- [x] T042 [US2] Implement OAuth callback endpoint in backend/src/app/api/v1/auth.py (GET /auth/google/callback)
- [x] T043 [US2] Implement session management with httpOnly cookies in backend/src/app/services/auth_service.py
- [x] T044 [US2] Create get current user endpoint in backend/src/app/api/v1/auth.py (GET /auth/me)
- [x] T045 [US2] Create logout endpoint in backend/src/app/api/v1/auth.py (POST /auth/logout)
- [x] T046 [P] [US2] Create authentication service in frontend/src/services/auth.ts
- [x] T047 [P] [US2] Create auth store in frontend/src/stores/auth.ts with Pinia
- [x] T048 [P] [US2] Create LoginPage component in frontend/src/pages/LoginPage.vue with Gmail OAuth button
- [x] T049 [P] [US2] Create RegisterPage component in frontend/src/pages/RegisterPage.vue with Gmail OAuth button
- [x] T050 [US2] Add authentication route guards in frontend/src/router/index.ts
- [x] T051 [US2] Integrate auth service with API client in frontend/src/services/api.ts
- [x] T052 [US2] Add session refresh logic in frontend/src/services/auth.ts
- [x] T053 [US2] Add error handling for OAuth failures in frontend/src/pages/LoginPage.vue and RegisterPage.vue

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can authenticate and then convert markdown to PDF.

---

## Phase 5: User Story 3 - Plan Limits and Enforcement (Priority: P3)

**Goal**: Enforce usage limits based on user plan type (free: <20 pages, premium: 20-500 pages) and track page counts.

**Independent Test**: A free plan user attempting to convert a document that would exceed 20 pages gets blocked with an appropriate message. A premium user successfully converts documents within their 20-500 page limit.

### Implementation for User Story 3

- [x] T054 [P] [US3] Create Plan MongoDB model in backend/src/app/db/models/plan.py
- [x] T055 [P] [US3] Create Plan Pydantic model in backend/src/app/models/plan.py
- [x] T056 [US3] Initialize plan reference data (free/premium) in MongoDB via migration script
- [x] T057 [US3] Create plan service in backend/src/app/services/plan_service.py with limit checking logic
- [x] T058 [US3] Create conversion service in backend/src/app/services/conversion_service.py for tracking conversions
- [x] T059 [US3] Add page count calculation logic in backend/src/app/services/conversion_service.py (from PDF)
- [x] T060 [US3] Implement plan limit check before conversion in backend/src/app/services/plan_service.py
- [x] T061 [US3] Create conversion tracking endpoint in backend/src/app/api/v1/conversions.py (POST /conversions) with plan limit enforcement
- [x] T062 [US3] Create conversion history endpoint in backend/src/app/api/v1/conversions.py (GET /conversions/history)
- [x] T063 [US3] Create user account endpoint in backend/src/app/api/v1/users.py (GET /users/account) with plan and usage info
- [x] T064 [US3] Update User model to track total_pages_converted in backend/src/app/db/models/user.py
- [x] T065 [US3] Add transaction handling for conversion + page count update in backend/src/app/services/conversion_service.py
- [x] T066 [P] [US3] Create conversion store in frontend/src/stores/conversion.ts with Pinia
- [x] T067 [P] [US3] Create AccountPage component in frontend/src/pages/AccountPage.vue
- [x] T068 [US3] Display plan type and usage information in AccountPage.vue
- [x] T069 [US3] Add plan limit checking in frontend before conversion attempt in ConvertPage.vue
- [x] T070 [US3] Display plan limit exceeded message in ConvertPage.vue when limit reached
- [x] T071 [US3] Integrate conversion tracking API calls in frontend/src/services/api.ts
- [x] T072 [US3] Add route for AccountPage in frontend/src/router/index.ts

**Checkpoint**: All user stories should now be independently functional. Users can authenticate, convert markdown to PDF, and have their usage tracked with plan limits enforced.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T073 [P] Add rate limiting middleware in backend/src/app/middleware/rate_limit.py
- [x] T074 [P] Add CSRF protection middleware in backend/src/app/middleware/csrf.py
- [x] T075 [P] Add input validation and sanitization in backend/src/app/middleware/validation.py
- [x] T076 [P] Add Content Security Policy headers in backend/src/app/middleware/security.py
- [x] T077 [P] Add structured logging for conversions in backend/src/app/services/conversion_service.py
- [x] T078 [P] Add structured logging for authentication events in backend/src/app/services/auth_service.py
- [x] T079 [P] Add error boundary component in frontend/src/components/ErrorBoundary.vue
- [x] T080 [P] Add loading states and spinners across all frontend pages
- [x] T081 [P] Add toast notifications for success/error messages in frontend/src/components/Toast.vue
- [x] T082 [P] Add responsive design improvements across all frontend pages
- [x] T083 [P] Add backend fallback PDF generation endpoint in backend/src/app/api/v1/conversions.py (for quality/complexity cases)
- [x] T084 [P] Add PDF generation service in backend/src/app/services/pdf_service.py using weasyprint or reportlab
- [x] T085 Add environment variable validation on startup in backend/src/app/config.py
- [x] T086 Add frontend environment variable validation in frontend/src/config.ts
- [x] T087 Update quickstart.md validation - verify all setup steps work
- [x] T088 [P] Add API documentation improvements (OpenAPI schema enhancements)
- [x] T089 [P] Add code cleanup and refactoring pass
- [x] T090 [P] Add performance optimization (lazy loading, code splitting in frontend)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories. Can work without authentication initially.
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1. Authentication is required for US3.
- **User Story 3 (P3)**: Depends on Foundational (Phase 2) AND User Story 2 (P2) - Requires authentication to track user-specific page counts.

### Within Each User Story

- Models before services
- Services before endpoints/UI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, User Stories 1 and 2 can start in parallel
- User Story 3 must wait for User Story 2 (authentication) to complete
- All tasks within a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members (except US3 depends on US2)

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Create MarkdownEditor component in frontend/src/components/MarkdownEditor.vue"
Task: "Create FileUpload component in frontend/src/components/FileUpload.vue"
Task: "Create PdfViewer component in frontend/src/components/PdfViewer.vue"
Task: "Install markdown parsing library (markdown-it) in frontend/package.json"
Task: "Install PDF generation library (html2pdf.js) in frontend/package.json"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently - users can convert markdown to PDF without authentication
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! - conversion works)
3. Add User Story 2 → Test independently → Deploy/Demo (authentication added)
4. Add User Story 3 → Test independently → Deploy/Demo (plan limits enforced)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (conversion)
   - Developer B: User Story 2 (authentication) - can start in parallel
3. Once User Story 2 is complete:
   - Developer C: User Story 3 (plan limits) - depends on US2
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- User Story 1 can work without authentication (guest mode)
- User Story 2 enables authentication for all features
- User Story 3 requires authentication to track per-user usage
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

