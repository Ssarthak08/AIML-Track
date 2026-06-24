# 🚀 FastAPI Learning Project: BookVault API

> **Goal:** Build a full-featured Book Management REST API while deeply learning FastAPI, Pydantic, and industry-grade patterns.  
> **Duration:** 2 weeks · ~2 hrs/day  
> **Stack:** FastAPI · Pydantic v2 · SQLite + SQLAlchemy · Alembic · JWT Auth · pytest  

---

## 📌 What You'll Build

A **BookVault API** — a backend for managing books, authors, reviews, and user accounts.  
No frontend. Pure API, documented, tested, and structured the way a real backend engineer would ship it.

---

## 🗓️ Week 1 — Core FastAPI + Pydantic Mastery

---

### Day 1 — Project Skeleton & FastAPI Internals

**Goal:** Understand how FastAPI actually works before writing business logic.

**Topics Covered:**
- `FastAPI()` app lifecycle — what happens at startup/shutdown
- ASGI vs WSGI — why FastAPI uses Uvicorn/ASGI
- `APIRouter` — how FastAPI modularizes routes
- Request/response cycle internals
- Python type hints as the source of truth in FastAPI

**What to build:**
```
bookvault/
├── main.py               # App factory, router registration, lifespan
├── routers/
│   └── health.py         # GET /health, GET /health/detailed
├── core/
│   └── config.py         # Settings with pydantic-settings
└── requirements.txt
```

**Key concepts to research:**
- `@asynccontextmanager` lifespan pattern (replaces deprecated `on_event`)
- `app.include_router()` with prefix and tags
- `pydantic-settings` — `BaseSettings`, `.env` loading, type coercion

**Things to notice:** FastAPI builds an OpenAPI schema automatically from your type hints. Visit `/docs` and `/redoc` — understand *why* they look the way they do.

---

### Day 2 — Pydantic v2 Deep Dive (Models & Validation)

**Goal:** Understand Pydantic from first principles — this is the backbone of FastAPI.

**Topics Covered:**
- `BaseModel` internals — `model_fields`, `model_config`
- Field validators: `@field_validator`, `@model_validator`
- `Field(...)` — `default`, `default_factory`, `alias`, `title`, `description`, `ge`, `le`, `min_length`, `pattern`
- `model_config = ConfigDict(...)` — `str_strip_whitespace`, `str_to_lower`, `validate_assignment`, `populate_by_name`
- `computed_field` — derive fields from existing data
- `model_dump()` vs `model_dump(mode='json')` — serialization differences
- `model_validate()` — constructing models from dicts/ORM objects

**What to build:**
```
schemas/
├── book.py          # BookBase, BookCreate, BookUpdate, BookResponse, BookList
└── author.py        # AuthorBase, AuthorCreate, AuthorResponse
```

**Example schema to implement (start here, extend it):**
```python
class BookCreate(BaseModel):
    title: str
    isbn: str
    published_year: int
    price: Decimal
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        # ISBN-13 is 13 digits. Validate it.
        ...
    
    @field_validator('published_year')
    @classmethod
    def year_must_be_realistic(cls, v: int) -> int:
        # Books weren't printed before ~1450
        ...
```

**Key question to answer while coding:** What's the difference between `@field_validator(mode='before')` and `mode='after'`? When would you use each?

---

### Day 3 — Path/Query/Body Parameters + Response Models

**Goal:** Master how FastAPI extracts data from requests and shapes responses.

**Topics Covered:**
- Path parameters — `Path(...)` with validation (`ge`, `le`, `pattern`)
- Query parameters — `Query(...)`, optional vs required, list params
- Request body — `Body(...)`, `embed=True`
- `Annotated[type, Field(...)]` — the modern way to annotate
- Response models — `response_model`, `response_model_exclude_unset`, `response_model_include`
- `JSONResponse`, `Response` — when you need to bypass response_model
- Status codes — `status.HTTP_201_CREATED`, `status.HTTP_204_NO_CONTENT`

**What to build:**
```
routers/
├── books.py     # Full CRUD: POST /books, GET /books, GET /books/{id}, PATCH /books/{id}, DELETE /books/{id}
└── authors.py   # POST /authors, GET /authors/{id}, GET /authors/{id}/books
```

**Patterns to implement:**
```python
# Filtering + pagination in GET /books
@router.get("/books", response_model=list[BookResponse])
async def list_books(
    title: str | None = Query(None, min_length=1, max_length=100),
    year_from: int | None = Query(None, ge=1450),
    year_to: int | None = Query(None, le=2025),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    ...
```

**Things to notice:** What happens if you set `response_model=BookResponse` but return a dict? What if the dict has extra keys?

---

### Day 4 — Database Layer (SQLAlchemy + Async)

**Goal:** Wire FastAPI to a real database without blocking the event loop.

**Topics Covered:**
- SQLAlchemy 2.0 style — `DeclarativeBase`, `Mapped`, `mapped_column`
- `AsyncEngine`, `AsyncSession`, `async_sessionmaker`
- Dependency injection with `Depends` — the FastAPI pattern for DB sessions
- `get_db()` generator pattern — yield-based cleanup
- Basic CRUD with async SQLAlchemy: `session.execute(select(...))`, `session.add()`, `session.commit()`
- `selectinload` vs `joinedload` — N+1 problem and how to fix it

**What to build:**
```
models/
├── base.py       # DeclarativeBase, TimestampMixin (created_at, updated_at)
├── book.py       # Book model with relationship to Author
└── author.py     # Author model

database.py       # Engine, sessionmaker, get_db dependency
```

**Key pattern — session as a dependency:**
```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# In router:
@router.get("/books/{book_id}")
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    ...
```

**Key question:** Why is `Depends(get_db)` better than creating a session inside the route function directly?

---

### Day 5 — Repository Pattern + Service Layer

**Goal:** Learn how to separate concerns properly — the way real codebases are structured.

**Topics Covered:**
- Repository pattern — abstract data access behind a class
- Service layer — business logic lives here, not in routes
- Why this structure matters: testability, replaceability
- Type aliases and generic repositories

**What to build:**
```
repositories/
├── base.py          # Generic BaseRepository[ModelType]
├── book.py          # BookRepository: get, get_multi, create, update, delete
└── author.py        # AuthorRepository

services/
├── book.py          # BookService — orchestrates repo + business rules
└── author.py        # AuthorService
```

**What the structure looks like:**
```
Route → Service → Repository → Database
          ↑ business logic    ↑ data access only
```

The route should do almost nothing except parse input and call a service method. The service handles rules (e.g., "can't delete an author with books"). The repository handles SQL.

**Key question:** What makes this testable? (Hint: think about what you'd mock in a unit test.)

---

### Day 6 — Error Handling + Custom Exceptions

**Goal:** Make the API return clean, consistent errors that clients can rely on.

**Topics Covered:**
- `HTTPException` — when and how to raise it
- `RequestValidationError` — what FastAPI raises on Pydantic failures
- Custom exception classes
- `@app.exception_handler(ExceptionType)` — global handlers
- Structured error response schemas
- 404 vs 422 vs 500 — when each is appropriate

**What to build:**
```
core/
├── exceptions.py       # BookNotFoundError, DuplicateISBNError, etc.
└── exception_handlers.py  # Global handlers registered in main.py

schemas/
└── errors.py           # ErrorResponse, ValidationErrorResponse
```

**Error schema to standardize on:**
```python
class ErrorDetail(BaseModel):
    field: str | None = None
    message: str
    
class ErrorResponse(BaseModel):
    status_code: int
    error: str
    details: list[ErrorDetail] = []
    request_id: str | None = None
```

**What to implement:** Override FastAPI's default 422 validation error handler to return *your* error schema, not FastAPI's default one.

---

### Day 7 — Database Migrations (Alembic) + Review Entity

**Goal:** Learn proper migration workflows and add the reviews feature.

**Topics Covered:**
- Why migrations exist — the problem with `create_all()`
- Alembic setup with async SQLAlchemy
- `alembic revision --autogenerate` — how it compares model vs DB
- `alembic upgrade head` / `alembic downgrade -1`
- Migration best practices — never edit old migrations

**What to build:**
```
alembic/
├── env.py              # Async-compatible env
└── versions/
    ├── 001_create_authors.py
    ├── 002_create_books.py
    └── 003_create_reviews.py

models/
└── review.py           # Review model (book_id FK, rating 1-5, body text)

routers/
└── reviews.py          # POST /books/{id}/reviews, GET /books/{id}/reviews
```

**Practice the full migration workflow:**
1. Create model → generate migration → inspect the generated SQL → run it → verify schema.

---

## 🗓️ Week 2 — Auth, Testing, and Production Patterns

---

### Day 8 — Authentication: JWT + OAuth2 Password Flow

**Goal:** Implement real authentication the FastAPI way.

**Topics Covered:**
- Password hashing with `passlib` (bcrypt) — never store plaintext
- `OAuth2PasswordBearer` — FastAPI's built-in scheme
- `OAuth2PasswordRequestForm` — the standard login form body
- JWT tokens — structure (header.payload.signature), encoding with `python-jose`
- `Depends` chain — `get_current_user` depends on `oauth2_scheme` depends on request
- Token expiry, refresh token concepts (implement access token only)

**What to build:**
```
models/
└── user.py             # User model: id, email, hashed_password, is_active

routers/
├── auth.py             # POST /auth/register, POST /auth/login (returns JWT)
└── users.py            # GET /users/me

core/
└── security.py         # hash_password, verify_password, create_access_token, decode_token

dependencies/
└── auth.py             # get_current_user, require_active_user
```

**The dependency chain to understand:**
```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    # decode JWT → get user_id → fetch from DB → return User
    ...

# Then in routes:
@router.get("/users/me")
async def me(current_user: User = Depends(get_current_user)):
    return current_user
```

**Key question:** Why does FastAPI show a lock icon on `/docs` for protected routes once you add `Depends(oauth2_scheme)`?

---

### Day 9 — Advanced Dependency Injection

**Goal:** Master `Depends` — FastAPI's superpower.

**Topics Covered:**
- Dependency injection vs manual wiring
- Dependencies with `yield` — setup + teardown (same as get_db)
- Nested dependencies — FastAPI builds a DAG and resolves it
- `Depends` on class instances — `__call__` pattern
- `BackgroundTasks` — fire-and-forget after response
- Caching: `use_cache=True` (default) vs `use_cache=False`

**What to build:**
```python
# Class-based dependency (pagination)
class PaginationParams:
    def __init__(
        self,
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
    ):
        self.limit = limit
        self.offset = offset

# Reuse across all list endpoints
@router.get("/books")
async def list_books(pagination: PaginationParams = Depends()):
    ...
    
@router.get("/authors")
async def list_authors(pagination: PaginationParams = Depends()):
    ...
```

**Also implement:**
- `BackgroundTasks`: after a user posts a review, send a mock email notification in the background (just print/log it for now)
- A `require_admin` dependency that extends `get_current_user`

---

### Day 10 — Middleware + Request Lifecycle

**Goal:** Understand the full request/response pipeline.

**Topics Covered:**
- Starlette middleware — FastAPI is built on Starlette
- `BaseHTTPMiddleware` — wrapping every request
- `@app.middleware("http")` decorator style
- CORS — `CORSMiddleware` and why it matters for frontends
- Request ID injection — trace every request
- Timing middleware — measure response time
- Trusted host middleware

**What to build:**
```
middleware/
├── request_id.py     # Inject X-Request-ID header on every request
├── timing.py         # Inject X-Process-Time header on every response
└── logging.py        # Log method, path, status_code, duration on every request
```

**Middleware to implement:**
```python
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        # Store on request.state so routes can access it
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
```

**Key question:** What's the order of middleware execution? What's the difference between middleware and a dependency?

---

### Day 11 — Testing with pytest + HTTPX

**Goal:** Learn to write tests that actually give you confidence.

**Topics Covered:**
- `pytest` basics — fixtures, parametrize, conftest.py
- `httpx.AsyncClient` with `ASGITransport` — testing FastAPI without a real server
- Test database setup — separate SQLite DB per test run
- `pytest-asyncio` — running async test functions
- Dependency overrides — `app.dependency_overrides[get_db] = get_test_db`
- Testing auth routes — getting a token, using it in subsequent requests
- Factory pattern for test data

**What to build:**
```
tests/
├── conftest.py         # App fixture, test DB, async client, auth helpers
├── test_books.py       # CRUD tests for books
├── test_auth.py        # Register, login, token usage
└── test_reviews.py     # Review creation, validation
```

**The test setup that everything else builds on:**
```python
# conftest.py
@pytest.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
        
@pytest.fixture
async def auth_headers(client):
    # register → login → return {"Authorization": "Bearer <token>"}
    ...
```

**Tests to write:**
- Creating a book with missing required fields → assert 422
- Creating a duplicate ISBN → assert 409
- Getting a non-existent book → assert 404
- Protected route without token → assert 401
- Protected route with token → assert 200

---

### Day 12 — Advanced Pydantic Patterns

**Goal:** Go deeper on Pydantic — the parts most tutorials skip.

**Topics Covered:**
- `model_validator(mode='before')` vs `mode='after')` — cross-field validation
- Discriminated unions — `Annotated[Union[...], Field(discriminator='type')]`
- Custom types — subclass `str` or use `Annotated` with `AfterValidator`
- `model_rebuild()` — forward references in circular schemas
- Partial updates — handling `PATCH` semantics with `Optional` fields
- `model_dump(exclude_unset=True)` — only update what was sent

**What to build:**

Proper PATCH (partial update) for books:
```python
class BookUpdate(BaseModel):
    title: str | None = None
    price: Decimal | None = None
    published_year: int | None = None
    
    # This validator runs after individual field validators
    @model_validator(mode='after')
    def at_least_one_field(self) -> 'BookUpdate':
        if not any([self.title, self.price, self.published_year]):
            raise ValueError('At least one field must be provided')
        return self
```

A custom ISBN type:
```python
def validate_isbn13(v: str) -> str:
    # real ISBN-13 check digit validation
    ...
    
ISBN13 = Annotated[str, AfterValidator(validate_isbn13)]

class BookCreate(BaseModel):
    isbn: ISBN13   # reusable anywhere
```

---

### Day 13 — Background Tasks, Events & Advanced Patterns

**Goal:** Cover the remaining FastAPI features worth knowing before production.

**Topics Covered:**
- `startup` / `shutdown` lifespan events — connection pooling, cache warmup
- `BackgroundTasks` deep dive — limitations (no retry, no persistence)
- File uploads — `UploadFile`, `File(...)`
- Streaming responses — `StreamingResponse` for large payloads
- `WebSocket` basics — a minimal chat endpoint to understand the concept
- Custom OpenAPI — adding security schemes, custom docs metadata
- `APIRouter` dependencies — apply auth to all routes in a router at once

**What to build:**

Book cover upload:
```python
@router.post("/books/{book_id}/cover")
async def upload_cover(
    book_id: int,
    cover: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # validate file type, save, update book record
    ...
```

Apply auth to entire router:
```python
router = APIRouter(
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(get_current_user)],  # ALL routes require auth
)
```

---

### Day 14 — Polish: Logging, Config, Final Cleanup

**Goal:** Make the project look like something you'd actually put on a resume.

**Topics Covered:**
- Structured logging with `structlog` or `logging.config.dictConfig`
- 12-factor config — all config via environment, never hardcoded
- `pydantic-settings` with multiple env files (`.env`, `.env.test`)
- OpenAPI customization — title, version, contact, license
- Proper README
- `pyproject.toml` — modern Python project packaging

**What to build:**
```
core/
├── config.py      # Complete settings model using pydantic-settings
└── logging.py     # Structured logging setup

.env               # Local development settings
.env.example       # Template committed to git (no secrets)
pyproject.toml     # Project metadata, dependencies, tool config
README.md          # Setup instructions, endpoint summary
```

**Final config to implement:**
```python
class Settings(BaseSettings):
    app_name: str = "BookVault API"
    debug: bool = False
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 30
    allowed_origins: list[str] = ["http://localhost:3000"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
```

---

## 📂 Final Project Structure

```
bookvault/
├── alembic/
│   ├── env.py
│   └── versions/
├── core/
│   ├── config.py
│   ├── exceptions.py
│   ├── exception_handlers.py
│   ├── logging.py
│   └── security.py
├── dependencies/
│   └── auth.py
├── middleware/
│   ├── request_id.py
│   └── timing.py
├── models/
│   ├── base.py
│   ├── author.py
│   ├── book.py
│   ├── review.py
│   └── user.py
├── repositories/
│   ├── base.py
│   ├── author.py
│   └── book.py
├── routers/
│   ├── auth.py
│   ├── authors.py
│   ├── books.py
│   ├── health.py
│   ├── reviews.py
│   └── users.py
├── schemas/
│   ├── author.py
│   ├── book.py
│   ├── errors.py
│   ├── review.py
│   └── user.py
├── services/
│   ├── author.py
│   └── book.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_books.py
│   └── test_reviews.py
├── database.py
├── main.py
├── .env.example
├── alembic.ini
├── pyproject.toml
└── README.md
```

---

## 🔑 Key Concepts Summary

| Day | Core Concept | FastAPI Feature |
|-----|-------------|-----------------|
| 1 | App structure, ASGI | `FastAPI()`, `APIRouter`, `include_router` |
| 2 | Validation, serialization | `BaseModel`, `Field`, `field_validator`, `model_validator` |
| 3 | Request parsing, response shaping | `Path`, `Query`, `Body`, `response_model` |
| 4 | Async DB access | `AsyncSession`, `Depends(get_db)` |
| 5 | Separation of concerns | Repository + Service pattern |
| 6 | Error contracts | `HTTPException`, `exception_handler` |
| 7 | Schema evolution | Alembic migrations |
| 8 | Auth | `OAuth2PasswordBearer`, JWT, `Depends` chain |
| 9 | DI mastery | Class-based deps, `BackgroundTasks`, `use_cache` |
| 10 | Request pipeline | Middleware, CORS, request state |
| 11 | Testing | `httpx`, `pytest-asyncio`, dependency overrides |
| 12 | Pydantic advanced | Discriminated unions, custom types, PATCH semantics |
| 13 | Production patterns | Lifespan, file uploads, router-level auth |
| 14 | Production readiness | Structured logging, `pydantic-settings` |

---

## 📦 Dependencies

```toml
[project]
name = "bookvault"
requires-python = ">=3.11"
dependencies = [
    "fastapi[standard]>=0.115",
    "sqlalchemy[asyncio]>=2.0",
    "aiosqlite",
    "alembic",
    "pydantic[email]>=2.0",
    "pydantic-settings",
    "python-jose[cryptography]",
    "passlib[bcrypt]",
    "python-multipart",
]

[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-asyncio",
    "httpx",
]
```

---

## 🧠 Things to Look Up on Your Own (Don't Skip These)

These aren't implemented in the project but are essential FastAPI/Pydantic knowledge:

- `orjson` — faster JSON serialization, drop-in replacement
- `fastapi-cache2` — Redis-backed response caching
- `rate limiting` — `slowapi` library
- `Pydantic v2 performance` — why v2 is 5-50x faster than v1 (Rust core)
- `anyio` vs `asyncio` — what FastAPI uses internally
- `WebSockets` — full-duplex connections (briefly touched Day 13)
- `Server-Sent Events` (SSE) — for streaming AI responses
- `OpenTelemetry` — distributed tracing (you're already using this in InsightBase)

---

## ✅ Definition of Done

By end of Day 14, you should be able to:

- [ ] Explain what happens between `uvicorn main:app` and the first request being handled
- [ ] Write a Pydantic model with custom validators and explain when each validator mode runs
- [ ] Implement a new feature end-to-end: model → migration → schema → repository → service → route → test
- [ ] Debug a 422 validation error by reading the error body
- [ ] Chain 3+ dependencies together and explain how FastAPI resolves them
- [ ] Write a middleware and explain when it runs relative to route dependencies
- [ ] Override a dependency in tests without changing production code
