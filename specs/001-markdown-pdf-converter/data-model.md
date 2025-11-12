# Data Model: Markdown to PDF Converter

**Created**: 2025-01-27  
**Purpose**: Define data entities, relationships, validation rules, and state transitions

## Entities

### User

**Purpose**: Represents an authenticated user account with plan information and usage tracking.

**Attributes**:
- `_id` (ObjectId): Unique identifier, MongoDB primary key
- `email` (string, required, unique): User's email address from Gmail OAuth
- `plan_type` (string, enum: ["free", "premium"], default: "free"): Subscription tier
- `total_pages_converted` (integer, default: 0, min: 0): Cumulative pages converted across all conversions
- `account_created_at` (datetime, required): Account creation timestamp
- `last_login_at` (datetime, optional): Most recent login timestamp
- `oauth_provider` (string, default: "google"): Authentication provider (extensible for future providers)
- `oauth_user_id` (string, required, unique): OAuth provider's user identifier

**Validation Rules**:
- Email must be valid email format
- `total_pages_converted` cannot be negative
- `plan_type` must be one of: "free", "premium"
- `account_created_at` must be a valid datetime
- `last_login_at` must be >= `account_created_at` if present

**State Transitions**:
- **New User Creation**: `plan_type` = "free", `total_pages_converted` = 0, `account_created_at` = now
- **Plan Upgrade**: `plan_type` changes from "free" to "premium" (future: may reset or adjust page count)
- **Login**: `last_login_at` updated to current timestamp
- **Conversion**: `total_pages_converted` incremented by conversion page count

**Indexes**:
- `email` (unique index)
- `oauth_user_id` (unique index)
- `plan_type` (index for plan-based queries)

### Conversion

**Purpose**: Represents a single markdown to PDF conversion operation with tracking information.

**Attributes**:
- `_id` (ObjectId): Unique identifier, MongoDB primary key
- `user_id` (ObjectId, required, indexed): Reference to User who performed conversion
- `input_type` (string, enum: ["text", "file"], required): Input method
- `input_content` (string, optional): Markdown text content (if `input_type` = "text")
- `input_file_name` (string, optional): Original filename (if `input_type` = "file")
- `input_file_size` (integer, optional, min: 0): File size in bytes (if `input_type` = "file")
- `page_count` (integer, required, min: 1): Number of pages in generated PDF
- `conversion_method` (string, enum: ["client", "server"], required): Method used for PDF generation
- `status` (string, enum: ["success", "failed"], required): Conversion result
- `error_message` (string, optional): Error details if `status` = "failed"
- `converted_at` (datetime, required): Conversion timestamp
- `pdf_file_reference` (string, optional): Reference to stored PDF file (if stored server-side)

**Validation Rules**:
- `user_id` must reference existing User
- `input_type` must be "text" or "file"
- If `input_type` = "text", `input_content` is required
- If `input_type` = "file", `input_file_name` is required
- `page_count` must be >= 1
- `status` must be "success" or "failed"
- If `status` = "failed", `error_message` should be provided
- `converted_at` must be a valid datetime

**State Transitions**:
- **Conversion Initiated**: Record created with `status` = "pending" (ephemeral, not stored)
- **Conversion Success**: `status` = "success", `page_count` set, `converted_at` = now
- **Conversion Failure**: `status` = "failed", `error_message` set, `converted_at` = now
- **User Page Count Update**: After successful conversion, User's `total_pages_converted` incremented

**Indexes**:
- `user_id` (index for user's conversion history queries)
- `converted_at` (index for time-based queries)
- `status` (index for filtering successful/failed conversions)

### Plan

**Purpose**: Defines subscription tier limits and features (reference data, not user-specific).

**Attributes**:
- `plan_type` (string, enum: ["free", "premium"], required, unique): Plan identifier
- `min_page_limit` (integer, required, min: 0): Minimum page limit (inclusive)
- `max_page_limit` (integer, required, min: 1): Maximum page limit (exclusive for free, inclusive for premium)
- `features` (array of strings, default: []): List of enabled features
- `description` (string, optional): Human-readable plan description

**Validation Rules**:
- `plan_type` must be "free" or "premium"
- `max_page_limit` must be > `min_page_limit`
- For "free": `min_page_limit` = 0, `max_page_limit` = 20 (exclusive, so <20)
- For "premium": `min_page_limit` = 20, `max_page_limit` = 500 (inclusive, so 20-500)

**Reference Data** (stored in database, but typically hardcoded in application):
- **Free Plan**: `min_page_limit` = 0, `max_page_limit` = 20, `features` = ["basic_conversion"]
- **Premium Plan**: `min_page_limit` = 20, `max_page_limit` = 500, `features` = ["basic_conversion", "large_documents", "priority_support"]

**State Transitions**: None (reference data, immutable)

**Indexes**:
- `plan_type` (unique index)

## Relationships

### User → Conversion (One-to-Many)
- One User can have many Conversions
- `Conversion.user_id` references `User._id`
- Cascade: If User is deleted, Conversions may be retained for analytics (soft delete) or deleted (hard delete) - decision pending

### User → Plan (Many-to-One)
- Many Users belong to one Plan type
- `User.plan_type` references `Plan.plan_type` (string reference, not foreign key)
- Plan limits enforced via `User.plan_type` and `User.total_pages_converted`

## Business Rules

### Plan Limit Enforcement

**Rule**: User cannot convert if `total_pages_converted + estimated_page_count >= plan_max_limit`

**Implementation**:
1. Before conversion: Check `User.total_pages_converted + estimated_page_count < Plan.max_page_limit`
2. After conversion: Update `User.total_pages_converted += Conversion.page_count`
3. If limit exceeded: Return 403 Forbidden, do not increment page count

**Edge Cases**:
- If conversion fails after page count increment: Rollback `User.total_pages_converted` (transaction required)
- If page count calculation is inaccurate: Use actual PDF page count, not estimation
- Plan upgrade mid-month: Decision pending (reset count vs. prorated adjustment)

### Page Count Calculation

**Rule**: Page count must be accurate (from actual PDF), not estimated.

**Implementation**:
- Generate PDF first (client or server)
- Count pages in generated PDF
- Use this count for plan limit check and user tracking
- Store in `Conversion.page_count`

## Data Validation Summary

### User Validation
- Email format validation
- Plan type enum validation
- Non-negative page count
- Valid datetime fields

### Conversion Validation
- User reference exists
- Input type matches provided fields
- Page count >= 1
- Status enum validation
- Error message required if failed

### Plan Validation
- Plan type enum validation
- Limit range validation (max > min)
- Feature list validation

## Database Schema (MongoDB)

### Collections

**users**:
```javascript
{
  _id: ObjectId,
  email: String (unique),
  plan_type: String ("free" | "premium"),
  total_pages_converted: Number (default: 0),
  account_created_at: Date,
  last_login_at: Date (optional),
  oauth_provider: String (default: "google"),
  oauth_user_id: String (unique)
}
```

**conversions**:
```javascript
{
  _id: ObjectId,
  user_id: ObjectId (indexed),
  input_type: String ("text" | "file"),
  input_content: String (optional),
  input_file_name: String (optional),
  input_file_size: Number (optional),
  page_count: Number (min: 1),
  conversion_method: String ("client" | "server"),
  status: String ("success" | "failed"),
  error_message: String (optional),
  converted_at: Date,
  pdf_file_reference: String (optional)
}
```

**plans** (reference data):
```javascript
{
  plan_type: String (unique, "free" | "premium"),
  min_page_limit: Number,
  max_page_limit: Number,
  features: [String],
  description: String (optional)
}
```

