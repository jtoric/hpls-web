# HPLS Powerlifting Website

## Project Overview
Croatian Powerlifting Federation (HPLS) website — a FastAPI + Vue 3 rebuild of the existing WordPress site. Backend serves as a headless CMS with JWT auth; frontend is a Vue SPA with TailwindCSS.

## Architecture

### Backend (`backend/`)
- **Framework:** FastAPI + SQLAlchemy ORM + SQLite (configurable via `DATABASE_URL`)
- **Pattern:** Router → Service → Repository (3-layer separation)
- **Auth:** JWT tokens (python-jose), bcrypt password hashing
- **File uploads:** Local filesystem at `backend/uploads/<type>/YYYY/MM/<uuid>.ext`

### Frontend (`frontend/`)
- **Framework:** Vue 3 (Composition API, `<script setup>`) + Vite
- **State:** Pinia store for auth
- **Styling:** TailwindCSS v4 (requires `@reference "../style.css"` in scoped `<style>` blocks)
- **Editor:** TipTap WYSIWYG for admin content editing

## Key Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
python seed.py                        # Create admin user + initial pages
uvicorn app.main:app --reload         # Start dev server on :8000
python -m pytest tests/ -v            # Run all 34 tests
```

### Frontend
```bash
cd frontend
npm install
npm run dev                           # Start dev server on :5173
npm run build                         # Production build to dist/
```

## Important Conventions
- **Slug validation:** Slugs must match `^[a-z0-9]+(?:-[a-z0-9]+)*$`
- **Post categories:** Only `"news"` or `"calendar"` (enforced via `Literal` type)
- **Mass assignment protection:** Repositories use `UPDATABLE_FIELDS` whitelists
- **Path traversal protection:** File deletion uses `resolve()` + `is_relative_to()` checks
- **Timezone:** All datetimes use `datetime.now(timezone.utc)`, never `utcnow()`
- **Tests:** pytest with in-memory SQLite, fixtures in `tests/conftest.py`
- **TailwindCSS v4 scoped styles:** Every Vue component with `<style scoped>` must include `@reference "../style.css";` (or correct relative path) as the first line

## Project Structure
```
backend/
  app/
    main.py              # FastAPI entry point, CORS, routes
    config.py            # Env-based configuration
    database.py          # SQLAlchemy engine + session
    auth.py              # Password hashing, JWT, FastAPI deps
    models.py            # ORM models (User, Post, Page, Document, Attachment)
    schemas.py           # Pydantic schemas with validation
    routers/             # API endpoint definitions
    services/            # Business logic layer
    repositories/        # Database query layer
  tests/                 # pytest test suite (34 tests)
  seed.py                # DB seed script
  requirements.txt
frontend/
  src/
    api/index.js         # Axios client with auth interceptor
    stores/auth.js       # Pinia auth store
    router/index.js      # Vue Router (public + admin routes)
    components/          # Shared components (header, footer, cards)
    views/               # Page views (public + admin/)
  style.css              # TailwindCSS entry point
```

## API Endpoints
- `POST /api/auth/login` — Login, returns JWT
- `GET /api/auth/me` — Current user info
- `GET/POST /api/posts` — List/create posts (news & calendar)
- `GET/PUT/DELETE /api/posts/{slug}` — Single post CRUD
- `GET/POST /api/pages` — List/create pages
- `GET/PUT /api/pages/{slug}` — Single page CRUD
- `GET/POST/DELETE /api/documents` — Document management
- `POST /api/upload` — File upload (WYSIWYG editor)
- `GET /api/search?q=` — Cross-model search

## Default Credentials
- Admin: `admin` / `admin123` (created by seed.py, change in production)
