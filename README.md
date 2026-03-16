# AP Budget App

Andhra Pradesh Government Budget 2026-27 — Public Transparency Dashboard

## Stack
- **Frontend**: Next.js 14, Tailwind CSS, TypeScript
- **Backend**: FastAPI, asyncpg, PostgreSQL
- **Monorepo**: Yarn Workspaces + Turborepo

## Structure
```
ap-budget-app/
├── apps/
│   ├── web/     Next.js 14 frontend
│   └── api/     FastAPI backend
└── package.json
```

## Quick Start

### 1. Install dependencies
```bash
yarn install
```

### 2. Set up API env
```bash
cp apps/api/.env.example apps/api/.env
# Edit apps/api/.env and set DATABASE_URL
```

### 3. Set up frontend env
```bash
cp apps/web/.env.example apps/web/.env.local
# Edit apps/web/.env.local — set NEXT_PUBLIC_API_URL
```

### 4. Run dev servers
```bash
yarn dev
# Frontend: http://localhost:3000
# API:      http://localhost:8000/docs
```

## Deployment
- **Frontend**: Vercel (import apps/web)
- **API**: Railway (import apps/api)
- **DB**: Neon.tech (free PostgreSQL)

## Pages
| Route | Description |
|-------|-------------|
| `/` | Home — search + summary stats |
| `/departments` | All departments with budget totals |
| `/department/[name]` | Single department detail + schemes |
| `/search?q=...` | Search results |
| `/schemes` | Top 50 schemes leaderboard |
