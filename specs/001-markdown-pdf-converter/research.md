# Research: Markdown to PDF Converter

**Created**: 2025-01-27  
**Purpose**: Resolve technical unknowns and establish best practices for implementation

## Client-Side PDF Generation from Markdown

### Decision: Hybrid Approach - Client-Side Primary with Backend Fallback

**Rationale**: Client-side PDF generation is feasible using modern JavaScript libraries, but has limitations for print-quality output. A hybrid approach provides the best user experience while ensuring quality.

**Primary Approach**: Client-side generation using:
- `markdown-it` or `marked` for markdown parsing to HTML
- `html2pdf.js` or `jsPDF` + `html2canvas` for HTML to PDF conversion
- CSS print media queries for print-ready styling

**Backend Fallback**: FastAPI endpoint for server-side PDF generation when:
- Client-side generation fails or times out
- Print quality requirements exceed browser capabilities
- Large documents (>100 pages) that may cause browser performance issues

**Alternatives Considered**:
1. **Pure Backend Generation**: Rejected because it increases server load and doesn't leverage user's browser resources. However, this remains as fallback option.
2. **Pure Client-Side**: Rejected because browser PDF generation may not match print quality expectations for all markdown formats (especially complex tables, code blocks with syntax highlighting).
3. **Third-Party Service**: Rejected due to cost, dependency, and data privacy concerns.

**Implementation Strategy**:
- Attempt client-side generation first (faster, reduces server load)
- If client-side fails or quality is insufficient, fallback to backend endpoint
- Track conversion method in database for analytics

**Libraries Evaluated**:
- `html2pdf.js`: Good for simple HTML to PDF, supports print media queries
- `jsPDF` + `html2canvas`: More control, but may have quality issues with complex layouts
- `puppeteer` (backend only): Excellent quality, but requires Node.js backend
- `weasyprint` (backend only): Python-based, excellent print quality

**Recommendation**: Start with `html2pdf.js` for client-side, implement FastAPI endpoint with `weasyprint` or `reportlab` as fallback.

## FastAPI with uv Package Management

### Decision: Use uv for FastAPI Project

**Rationale**: uv provides fast, reliable Python package management with lockfile support, similar to npm/pnpm for Node.js. It's production-ready and recommended for modern Python projects.

**Setup**:
- Initialize project with `uv init`
- Add dependencies with `uv add fastapi uvicorn motor python-multipart`
- Use `uv.lock` for reproducible builds
- Docker image will use uv for dependency installation

**Alternatives Considered**:
1. **pip + requirements.txt**: Rejected because slower and less reliable dependency resolution
2. **poetry**: Considered but uv is faster and has better Docker integration
3. **pipenv**: Rejected due to performance and maintenance concerns

## MongoDB with Docker

### Decision: Use Official MongoDB Docker Image

**Rationale**: Official MongoDB image provides stable, production-ready database with minimal configuration. Docker Compose simplifies local development and production deployment.

**Configuration**:
- Use `mongo:7.0` (latest stable)
- Persistent volume for data (`mongodb_data`)
- Environment variables for authentication (optional for development)
- Connection via Motor async driver in FastAPI

**Alternatives Considered**:
1. **MongoDB Atlas (cloud)**: Considered for production, but Docker provides better local development experience
2. **PostgreSQL**: Rejected because spec doesn't require relational features, MongoDB's document model fits user/conversion data better

## Vue 3 Frontend Architecture

### Decision: Vue 3 with Composition API, Pinia, Vue Router

**Rationale**: Vue 3 Composition API provides better TypeScript support and code organization. Pinia is the recommended state management solution. Vue Router handles navigation.

**Key Libraries**:
- `vue@^3.4` - Core framework
- `pinia@^2.1` - State management
- `vue-router@^4.2` - Routing
- `axios` or `fetch` - API client
- `markdown-it` - Markdown parsing
- `html2pdf.js` - PDF generation

**Build Tool**: Vite (recommended for Vue 3, fast HMR)

**Alternatives Considered**:
1. **React**: Rejected because user specified Vue 3
2. **Vue 2**: Rejected because Vue 3 has better performance and TypeScript support
3. **Nuxt**: Considered but overkill for this simple SPA

## Gmail OAuth Integration

### Decision: Google OAuth 2.0 with FastAPI backend

**Rationale**: Gmail OAuth provides secure, user-friendly authentication without password management. FastAPI backend handles OAuth flow securely, stores tokens in httpOnly cookies.

**Implementation**:
- Use `google-auth` and `google-auth-oauthlib` Python libraries
- OAuth flow: redirect to Google → callback to backend → set httpOnly cookie → redirect to frontend
- Frontend checks authentication status via API endpoint
- Token refresh handled automatically by backend

**Security Considerations**:
- OAuth tokens stored in httpOnly cookies (not accessible to JavaScript)
- CSRF protection for OAuth callback
- Token expiration and refresh handling
- Scope: `openid email profile` (minimal required)

**Alternatives Considered**:
1. **Frontend-only OAuth**: Rejected because tokens would be exposed to JavaScript (security risk)
2. **JWT tokens**: Considered but OAuth tokens in httpOnly cookies provide better security
3. **Email/password**: Rejected because user specified Gmail login

## Plan Limit Enforcement

### Decision: Server-Side Enforcement with Client-Side UI Feedback

**Rationale**: Plan limits must be enforced server-side to prevent bypassing. Client-side provides immediate feedback for better UX.

**Implementation**:
- Backend calculates page count before allowing conversion
- Frontend shows remaining pages and prevents conversion if limit reached
- API returns 403 Forbidden if limit exceeded
- Page count calculated from markdown content (estimate) or actual PDF pages (accurate)

**Page Counting Strategy**:
- Estimate: Count markdown lines / average lines per page (less accurate)
- Accurate: Generate PDF first, count pages (more accurate, but requires generation)
- **Decision**: Use PDF page count for accuracy (required for plan compliance per SC-004)

**Alternatives Considered**:
1. **Client-side only enforcement**: Rejected because easily bypassed
2. **Line-based estimation**: Rejected because inaccurate, violates SC-004 (100% compliance requirement)
3. **Post-conversion counting**: Considered but allows conversion before checking (violates requirement)

## Print-Ready PDF Styling

### Decision: CSS Print Media Queries with Custom Stylesheet

**Rationale**: Print media queries allow styling specifically for PDF output, matching browser print preview behavior.

**Implementation**:
- Markdown → HTML conversion with custom CSS classes
- Print stylesheet with `@media print` rules
- Page breaks, margins, headers/footers via CSS
- Code block syntax highlighting preserved in PDF

**Styling Requirements**:
- Headers: Clear hierarchy (h1-h6)
- Lists: Proper indentation and spacing
- Code blocks: Monospace font, background color, syntax highlighting
- Tables: Borders, proper alignment
- Page breaks: Avoid breaking code blocks, tables across pages

**Alternatives Considered**:
1. **Default browser styles**: Rejected because doesn't match "print-ready" requirement
2. **PDF-specific library options**: Considered but CSS print media is more maintainable
3. **Template-based approach**: Considered but CSS is more flexible for markdown variations

