"""
main.py -- AP Budget 2026-27 FastAPI application.

Endpoints:
  GET /                      health check + version info
  GET /years                 all available fiscal years
  GET /departments           top 50 departments by total budget_estimate
  GET /department/{name}     all rows for a department (filterable)
  GET /search                fuzzy search across scheme_name + department_name
  GET /majorhead/{code}      all rows for a major_head code
  GET /schemes/top           top 50 schemes by budget_estimate
  GET /summary               grand totals grouped by fiscal_year + state
  GET /scsp                  SC component rows
  GET /tsp                   ST component rows

All amounts are in Lakhs INR.
"""

import os as _os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from database import init_db, close_db, get_pool
from models import (
    HealthResponse,
    DepartmentSummary,
    BudgetRow,
    SearchResult,
    MajorHeadRow,
    TopScheme,
    SummaryRow,
    SCSPRow,
    TSPRow,
    YearsResponse,
)

# ---------------------------------------------------------------------------
# Lifespan: create / close DB pool
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AP Budget 2026-27 API",
    version="1.0.0",
    description=(
        "Query normalized Andhra Pradesh government budget data for 2026-27. "
        "All amount fields are in Lakhs INR. "
        "Source: AP Finance Department budget documents."
    ),
    lifespan=lifespan,
)

# CORS -- allow all origins by default.
# IMPORTANT: restrict allow_origins to your frontend domain in production.
# e.g. allow_origins=["https://your-app.vercel.app"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _rows_to_dicts(rows) -> list[dict]:
    """Convert asyncpg Record list to list of plain dicts."""
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

@app.get("/", response_model=HealthResponse, tags=["Health"])
async def root():
    """Health check -- returns API version and description."""
    return HealthResponse(
        status="ok",
        version="1.0.0",
        description="AP Budget 2026-27 API. Visit /docs for interactive documentation.",
    )


# ---------------------------------------------------------------------------
# GET /years
# ---------------------------------------------------------------------------

@app.get("/years", response_model=YearsResponse, tags=["Budget"])
async def get_years():
    """Return all distinct fiscal years present in the database."""
    pool = await get_pool()
    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT DISTINCT fiscal_year
                FROM budget_allocations
                WHERE fiscal_year IS NOT NULL
                ORDER BY fiscal_year
                """
            )
        years = [r["fiscal_year"] for r in rows]
        return YearsResponse(fiscal_years=years, count=len(years))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------------
# GET /departments
# ---------------------------------------------------------------------------

@app.get("/departments", response_model=list[DepartmentSummary], tags=["Departments"])
async def list_departments(
    fiscal_year: Optional[str] = Query(None, description="Filter by fiscal year e.g. 2026-27"),
    state: Optional[str] = Query(None, description="Filter by state e.g. AP"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    List departments with total budget_estimate, sorted descending.
    Optionally filter by fiscal_year or state.
    """
    pool = await get_pool()
    conditions = []
    params = []
    idx = 1

    if fiscal_year:
        conditions.append(f"fiscal_year = ${idx}")
        params.append(fiscal_year)
        idx += 1
    if state:
        conditions.append(f"state ILIKE ${idx}")
        params.append(state)
        idx += 1

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    params.extend([limit, offset])

    sql = f"""
        SELECT
            department_name,
            fiscal_year,
            state,
            SUM(budget_estimate)    AS total_budget_estimate_lakhs,
            SUM(revised_estimate)   AS total_revised_estimate_lakhs,
            SUM(actual_expenditure) AS total_actual_expenditure_lakhs
        FROM budget_allocations
        {where}
        GROUP BY department_name, fiscal_year, state
        ORDER BY total_budget_estimate_lakhs DESC NULLS LAST
        LIMIT ${idx} OFFSET ${idx + 1}
    """

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        return [DepartmentSummary(**dict(r)) for r in rows]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------------
# GET /department/{dept_name}
# ---------------------------------------------------------------------------

@app.get("/department/{dept_name}", response_model=list[BudgetRow], tags=["Departments"])
async def get_department(
    dept_name: str,
    fiscal_year: Optional[str] = Query(None),
    row_type: Optional[str] = Query(None, description="e.g. scheme, total, sub_total"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """
    All budget rows for a department (case-insensitive partial match).
    Filterable by fiscal_year and row_type.
    """
    pool = await get_pool()
    conditions = ["department_name ILIKE $1"]
    params: list = ["%" + dept_name + "%"]
    idx = 2

    if fiscal_year:
        conditions.append(f"fiscal_year = ${idx}")
        params.append(fiscal_year)
        idx += 1
    if row_type:
        conditions.append(f"row_type ILIKE ${idx}")
        params.append(row_type)
        idx += 1

    where = "WHERE " + " AND ".join(conditions)
    params.extend([limit, offset])

    sql = f"""
        SELECT *
        FROM budget_allocations
        {where}
        ORDER BY fiscal_year, major_head, row_index
        LIMIT ${idx} OFFSET ${idx + 1}
    """

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"No rows found for department matching '{dept_name}'.",
            )
        return [BudgetRow(**dict(r)) for r in rows]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------------
# GET /search
# ---------------------------------------------------------------------------

@app.get("/search", response_model=list[SearchResult], tags=["Search"])
async def search(
    q: str = Query(..., min_length=2, description="Search term"),
    fiscal_year: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    Fuzzy search across scheme_name and department_name.
    Uses pg_trgm similarity if available, falls back to ILIKE.
    Returns top results ranked by relevance.
    """
    pool = await get_pool()
    pattern = "%" + q + "%"

    # Try pg_trgm similarity first; fall back to ILIKE on failure
    trgm_sql_base = """
        SELECT
            id, state, fiscal_year, department_name, major_head,
            scheme_name, scheme_key, row_type,
            budget_estimate, revised_estimate, actual_expenditure, source_pdf,
            GREATEST(
                similarity(COALESCE(scheme_name, ''), $1),
                similarity(COALESCE(department_name, ''), $1)
            ) AS score
        FROM budget_allocations
        WHERE (
            scheme_name ILIKE $2
            OR department_name ILIKE $2
            OR similarity(COALESCE(scheme_name, ''), $1) > 0.15
            OR similarity(COALESCE(department_name, ''), $1) > 0.15
        )
    """

    ilike_sql_base = """
        SELECT
            id, state, fiscal_year, department_name, major_head,
            scheme_name, scheme_key, row_type,
            budget_estimate, revised_estimate, actual_expenditure, source_pdf,
            1.0 AS score
        FROM budget_allocations
        WHERE (
            scheme_name ILIKE $1
            OR department_name ILIKE $1
        )
    """

    try:
        async with pool.acquire() as conn:
            # Detect pg_trgm availability
            has_trgm = await conn.fetchval(
                "SELECT COUNT(*) FROM pg_extension WHERE extname = 'pg_trgm'"
            )

            if has_trgm:
                conditions = []
                params = [q, pattern]
                idx = 3
                if fiscal_year:
                    conditions.append(f"fiscal_year = ${idx}")
                    params.append(fiscal_year)
                    idx += 1
                where_extra = ("AND " + " AND ".join(conditions)) if conditions else ""
                params.extend([limit, offset])
                sql = f"""
                    {trgm_sql_base}
                    {where_extra}
                    ORDER BY score DESC
                    LIMIT ${idx} OFFSET ${idx + 1}
                """
                rows = await conn.fetch(sql, *params)
            else:
                conditions = []
                params = [pattern]
                idx = 2
                if fiscal_year:
                    conditions.append(f"fiscal_year = ${idx}")
                    params.append(fiscal_year)
                    idx += 1
                where_extra = ("AND " + " AND ".join(conditions)) if conditions else ""
                params.extend([limit, offset])
                sql = f"""
                    {ilike_sql_base}
                    {where_extra}
                    ORDER BY budget_estimate DESC NULLS LAST
                    LIMIT ${idx} OFFSET ${idx + 1}
                """
                rows = await conn.fetch(sql, *params)

        return [SearchResult(**{k: v for k, v in dict(r).items() if k != "score"}) for r in rows]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------------
# GET /majorhead/{code}
# ---------------------------------------------------------------------------

@app.get("/majorhead/{code}", response_model=list[MajorHeadRow], tags=["Major Heads"])
async def get_majorhead(
    code: str,
    fiscal_year: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """All rows for a given major_head code. Optionally filter by fiscal_year."""
    pool = await get_pool()
    conditions = ["major_head = $1"]
    params: list = [code]
    idx = 2

    if fiscal_year:
        conditions.append(f"fiscal_year = ${idx}")
        params.append(fiscal_year)
        idx += 1

    where = "WHERE " + " AND ".join(conditions)
    params.extend([limit, offset])

    sql = f"""
        SELECT
            major_head, fiscal_year, state, department_name,
            scheme_name, row_type,
            budget_estimate, revised_estimate, actual_expenditure
        FROM budget_allocations
        {where}
        ORDER BY fiscal_year, department_name, row_index
        LIMIT ${idx} OFFSET ${idx + 1}
    """

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"No rows found for major_head '{code}'.",
            )
        return [MajorHeadRow(**dict(r)) for r in rows]
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------------
# GET /schemes/top
# ---------------------------------------------------------------------------

@app.get("/schemes/top", response_model=list[TopScheme], tags=["Schemes"])
async def top_schemes(
    fiscal_year: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """
    Top schemes by total budget_estimate.
    Excludes rows where row_type = 'total' or 'sub_total'.
    """
    pool = await get_pool()
    conditions = ["row_type NOT IN ('total', 'sub_total', 'grand_total')"]
    params: list = []
    idx = 1

    if fiscal_year:
        conditions.append(f"fiscal_year = ${idx}")
        params.append(fiscal_year)
        idx += 1
    if state:
        conditions.append(f"state ILIKE ${idx}")
        params.append(state)
        idx += 1

    where = "WHERE " + " AND ".join(conditions)
    params.extend([limit, offset])

    sql = f"""
        SELECT
            scheme_name,
            scheme_key::TEXT AS scheme_key,
            department_name,
            fiscal_year,
            state,
            major_head,
            SUM(budget_estimate)    AS total_budget_estimate_lakhs,
            SUM(revised_estimate)   AS total_revised_estimate_lakhs,
            SUM(actual_expenditure) AS total_actual_expenditure_lakhs
        FROM budget_allocations
        {where}
        GROUP BY scheme_name, scheme_key, department_name, fiscal_year, state, major_head
        ORDER BY total_budget_estimate_lakhs DESC NULLS LAST
        LIMIT ${idx} OFFSET ${idx + 1}
    """

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        return [TopScheme(**dict(r)) for r in rows]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------------
# GET /summary
# ---------------------------------------------------------------------------

@app.get("/summary", response_model=list[SummaryRow], tags=["Budget"])
async def get_summary(
    fiscal_year: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
):
    """
    Grand totals of BE, RE, and Actuals grouped by fiscal_year and state.
    Optionally filter by fiscal_year or state.
    """
    pool = await get_pool()
    conditions = []
    params: list = []
    idx = 1

    if fiscal_year:
        conditions.append(f"fiscal_year = ${idx}")
        params.append(fiscal_year)
        idx += 1
    if state:
        conditions.append(f"state ILIKE ${idx}")
        params.append(state)
        idx += 1

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    sql = f"""
        SELECT
            fiscal_year,
            state,
            SUM(budget_estimate)    AS total_budget_estimate_lakhs,
            SUM(revised_estimate)   AS total_revised_estimate_lakhs,
            SUM(actual_expenditure) AS total_actual_expenditure_lakhs,
            COUNT(*)                AS row_count
        FROM budget_allocations
        {where}
        GROUP BY fiscal_year, state
        ORDER BY fiscal_year, state
    """

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        return [SummaryRow(**dict(r)) for r in rows]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------------
# GET /scsp
# ---------------------------------------------------------------------------

@app.get("/scsp", response_model=list[SCSPRow], tags=["SC/ST"])
async def get_scsp(
    fiscal_year: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """
    Scheduled Caste Sub-Plan (SCSP) rows.
    Matches source_pdf ILIKE '%sc%' OR scheme_name ILIKE '%scheduled caste%'
    OR scheme_name ILIKE '%scsp%' OR scheme_name ILIKE '% sc %'.
    """
    pool = await get_pool()
    conditions = [
        """(
            source_pdf ILIKE '%sc%'
            OR scheme_name ILIKE '%scheduled caste%'
            OR scheme_name ILIKE '%scsp%'
            OR scheme_name ILIKE '% sc %'
            OR scheme_name ILIKE '%sc component%'
        )"""
    ]
    params: list = []
    idx = 1

    if fiscal_year:
        conditions.append(f"fiscal_year = ${idx}")
        params.append(fiscal_year)
        idx += 1

    params.extend([limit, offset])
    where = "WHERE " + " AND ".join(conditions)

    sql = f"""
        SELECT
            id, state, fiscal_year, department_name, major_head,
            scheme_name, scheme_key::TEXT AS scheme_key, row_type,
            budget_estimate, revised_estimate, actual_expenditure,
            source_pdf, page_number
        FROM budget_allocations
        {where}
        ORDER BY fiscal_year, department_name, major_head
        LIMIT ${idx} OFFSET ${idx + 1}
    """

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        return [SCSPRow(**dict(r)) for r in rows]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ---------------------------------------------------------------------------
# GET /tsp
# ---------------------------------------------------------------------------

@app.get("/tsp", response_model=list[TSPRow], tags=["SC/ST"])
async def get_tsp(
    fiscal_year: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """
    Tribal Sub-Plan (TSP) rows.
    Matches source_pdf ILIKE '%st%' OR scheme_name ILIKE '%scheduled tribe%'
    OR scheme_name ILIKE '%tribal%' OR scheme_name ILIKE '%tsp%'.
    """
    pool = await get_pool()
    conditions = [
        """(
            source_pdf ILIKE '%st%'
            OR scheme_name ILIKE '%scheduled tribe%'
            OR scheme_name ILIKE '%tribal%'
            OR scheme_name ILIKE '%tsp%'
            OR scheme_name ILIKE '%st component%'
        )"""
    ]
    params: list = []
    idx = 1

    if fiscal_year:
        conditions.append(f"fiscal_year = ${idx}")
        params.append(fiscal_year)
        idx += 1

    params.extend([limit, offset])
    where = "WHERE " + " AND ".join(conditions)

    sql = f"""
        SELECT
            id, state, fiscal_year, department_name, major_head,
            scheme_name, scheme_key::TEXT AS scheme_key, row_type,
            budget_estimate, revised_estimate, actual_expenditure,
            source_pdf, page_number
        FROM budget_allocations
        {where}
        ORDER BY fiscal_year, department_name, major_head
        LIMIT ${idx} OFFSET ${idx + 1}
    """

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *params)
        return [TSPRow(**dict(r)) for r in rows]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
