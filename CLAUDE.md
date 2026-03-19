# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ICH Museum (非遗博物馆) - A Chinese Intangible Cultural Heritage exhibition platform. Monorepo with a Django REST backend (`ich_museum/`) and a Next.js frontend (`ich_museum_frontend/`).

## Commands

### Backend (`ich_museum/`)

All backend commands run from the `ich_museum/` directory with the virtualenv activated.

```bash
# Infrastructure (PostgreSQL 15, Redis 7, Elasticsearch 8.11)
docker-compose up -d

# Install dependencies
pip install -r requirements/dev.txt    # dev (includes ruff)
pip install -r requirements/test.txt   # test (includes pytest, factory-boy)

# Run dev server
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py runserver

# Database
python manage.py migrate
python manage.py loaddata apps/heritage/fixtures/categories.json

# Tests
pytest                                 # all tests (uses config.settings.test)
pytest apps/accounts/tests/test_services.py  # single file
pytest -k test_login_user              # single test by name
pytest --cov=apps --cov-report=html    # with coverage

# Lint
ruff check apps/
ruff format apps/
```

### Frontend (`ich_museum_frontend/`)

```bash
npm install
npm run dev       # dev server on :3000
npm run build     # production build
npm run lint      # ESLint
```

## Architecture

### Backend - Service Layer Pattern

Business logic lives in `services.py`, not in views or models. Each app follows:
- `models.py` - Django ORM models (UUIDs as primary keys throughout)
- `services.py` - All business logic and cross-app interface functions
- `serializers.py` - DRF serialization/validation
- `views.py` - Thin DRF views delegating to services
- `tests/` - Tests use `factory-boy` factories

Cross-app communication goes through public service functions (top of each `services.py`), not direct model imports. For example, `search` app imports `heritage.services.get_item_summary`, not `heritage.models.HeritageItem`.

### Backend Apps

- **core** - Shared utilities: standardized API response envelope (`{code, message, data}`), custom exception handler, pagination, permissions, request logging middleware
- **accounts** - Custom `User` model (email-based, UUID PK), JWT auth with blacklist via Redis, login lockout, email verification, password reset, role-based permissions (user/content_manager/admin)
- **heritage** - `HeritageItem`, `Category`, `Region`, `Inheritor`, `Favorite` models. Heritage CRUD fires Django signals that trigger Elasticsearch indexing
- **media** - Generic `MediaFile` model linked to any object via `object_type`/`object_id` (polymorphic association, not GenericForeignKey)
- **reviews** - `Review` model with 1-5 ratings, threaded replies via self-referential FK, soft delete
- **search** - Elasticsearch integration. Uses `ik_smart` analyzer for Chinese text. Signal handlers auto-sync heritage items to ES index on save/delete

### Frontend

- Next.js 14 (App Router) with `next-intl` for i18n (zh/en, default zh)
- Locale-based routing: `src/app/[locale]/`
- Tailwind CSS for styling
- API client in `src/lib/api.ts` proxies through Next.js rewrites to Django backend at `:8000`
- Auth state via React Context + `useReducer` in `src/contexts/AuthContext.tsx`
- Shared TypeScript types in `src/lib/types.ts` mirror Django API response shapes

### API Response Format

All API endpoints return a consistent envelope:
```json
{"code": 200, "message": "success", "data": {...}}
```
Use `apps.core.response.success_response` / `error_response` helpers.

## Key Configuration

- Django settings split: `config/settings/{base,dev,test}.py`. Set `DJANGO_SETTINGS_MODULE` env var
- Test settings use MD5 hasher and in-memory cache for speed
- Ruff config: line-length 120, single quotes, Python 3.11 target
- Frontend proxies `/api/*` to `http://localhost:8000/api/*` via Next.js rewrites

## AI-DLC Workflow

This project uses the AI-DLC (AI Development Lifecycle) workflow defined in `.kiro/steering/aws-aidlc-rules/core-workflow.md`. Design artifacts are stored in `aidlc-docs/` following Inception (requirements, stories, design) and Construction (functional design, NFR, infrastructure, code generation) phases.
