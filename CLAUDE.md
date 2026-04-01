# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SentinelAI is an AI-powered code security and quality review tool. It connects to GitHub repos, crawls codebases to build understanding, reviews PRs for security vulnerabilities and bugs, and surfaces issues with severity levels. It includes a FastAPI backend, a Next.js dashboard, and a chatbot for discussing findings.

## Running Locally

```bash
# Start all services (API + PostgreSQL + Redis)
docker-compose up --build

# Run API without Docker (requires .env with DATABASE_URL and REDIS_URL)
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API runs on `http://localhost:8000`. Postgres on `5432`, Redis on `6379`.

Required `.env` variables:
- `DATABASE_URL` — e.g. `postgresql://postgres:password@localhost:5432/sentinelai`

## Architecture

```
main.py          — FastAPI app entrypoint, mounts routers
database.py      — SQLAlchemy engine, SessionLocal, Base, get_db() dependency
models/          — SQLAlchemy ORM models (tables)
schemas/         — Pydantic schemas (request/response validation)
routers/         — FastAPI route handlers, one file per domain
```

Routers use `get_db()` as a FastAPI dependency for DB sessions. Models inherit from `Base` defined in `database.py`. All models must be imported before `Base.metadata.create_all()` is called.

## Agent Architecture

SentinelAI uses a **Supervisor → Sub-agent → Tools** pattern:

- A **Supervisor Agent** receives triggers (initial crawl request, PR webhook) and routes to specialized sub-agents
- **Sub-agents**: Crawl Agent (reads files/docs), Security Agent, Bug Detection Agent, PR Review Agent
- **Tools** are the only way agents interact with external systems: GitHub Tool, Email Tool, DB Tool, File Parser Tool, Diff Tool

AI provider is TBD — the tool interface is stable regardless of provider.

## Planned Phases

1. **Core Backend** — data models, repo ingestion, crawl agents, issue detection, severity classification
2. **GitHub Integration** — webhook receiver, PR diff analysis, PR commenting, email notifications
3. **Next.js Dashboard** — issue management UI, chatbot grounded in crawled repo context
4. **AWS Migration** — ECS, RDS, ElastiCache, SES, S3

## Issue Severity Levels

`critical` / `high` / `medium` / `low`
