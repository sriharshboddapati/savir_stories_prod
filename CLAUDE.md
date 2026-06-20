# Savir Stories — Claude Code Guide

## Project Overview

Baby milestone tracker for Savir. Users upload photos; GPT-4.1 vision generates titles and descriptions; milestones are stored in Azure Cosmos DB and displayed on a timeline.

**Architecture:**
- `main.py` — FastAPI backend (active)
- `app.py` — Streamlit UI (legacy, kept for reference)
- `utils.py` — shared business logic (Cosmos DB, OpenAI calls, timeline rendering)
- `savir-frontend/` — Next.js 15 frontend (in progress, not yet connected to API)

---

## Environment Setup

Always activate the Python venv before running backend commands:

```bash
source venv/bin/activate
```

Required `.env` variables:
```
OPENAI_API_KEY=
COSMOS_ENDPOINT=
COSMOS_KEY=
```

---

## Running the Project

**FastAPI backend:**
```bash
uvicorn main:app --reload
```

**Next.js frontend:**
```bash
cd savir-frontend
npm run dev
```

**Streamlit (legacy):**
```bash
streamlit run app.py
```

---

## Backend Conventions (FastAPI + Python)

- Keep route handlers in `main.py` thin — business logic belongs in `utils.py`
- Use `async def` for route handlers when possible
- Return plain dicts or Pydantic models from endpoints; do not return raw Cosmos DB items directly (they include internal `_rid`, `_etag` fields)
- Use `python-dotenv` with `load_dotenv()` — never hardcode credentials
- The Cosmos DB client is initialized at module level in `utils.py`; do not re-initialize it per-request
- Partition key for Cosmos DB container is `/date`

## OpenAI Usage

- Model: `gpt-4.1` (vision)
- Use `client.responses.create()` with `input_image` content type for photo analysis
- Generate title and description once at save time — do not re-call the API on every render or read
- Store generated title and description in Cosmos DB alongside the milestone record

## Azure Cosmos DB

- Database: `savirstoriesmain`
- Container: `savir1`
- Always use `upsert_item` to avoid duplicate writes
- Set a meaningful `id` field (currently `uuid4`) before upserting
- Use `enable_cross_partition_query=True` for full-scan queries

---

## Frontend Conventions (Next.js + TypeScript)

- Framework: Next.js 15 App Router (`app/` directory)
- UI: Chakra UI + Tailwind CSS
- Fetch milestone data from the FastAPI backend at `/` or `/milestone/`
- Use `'use client'` directive only for components that need browser APIs or interactivity
- Prefer server components for data fetching where possible
- API base URL should come from an environment variable (`NEXT_PUBLIC_API_URL`), not be hardcoded

---

## Code Style

**Python:**
- Use f-strings for string formatting
- Keep functions single-purpose
- Do not leave `pdb` or debug statements in committed code

**TypeScript/React:**
- Use functional components with explicit TypeScript types
- Avoid `any` types
- Keep page-level components in `app/`, reusable UI in `components/`

---

## What to Avoid

- Do not call OpenAI on every page render or data fetch — results must be cached in Cosmos DB
- Do not commit `.env` files
- Do not store images in the repo (a `media/` folder is used locally; images are not persisted in the cloud currently)
- Do not add Streamlit dependencies to new features — the frontend is moving to Next.js
