"""
database.py -- asyncpg connection pool for the AP Budget API.

Reads DATABASE_URL from environment (set in .env or Railway/Render dashboard).
Pool is created on startup via FastAPI lifespan and closed on shutdown.
"""

import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

_pool: asyncpg.Pool | None = None

async def init_db() -> None:
    global _pool
    database_url = os.environ["DATABASE_URL"]
    _pool = await asyncpg.create_pool(
        dsn=database_url,
        min_size=2,
        max_size=10,
        command_timeout=30,
        statement_cache_size=0,
    )

async def close_db() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None

async def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Database pool is not initialized. Call init_db() first.")
    return _pool

async def create_tables() -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS budget_allocations (
                id                  SERIAL PRIMARY KEY,
                state               VARCHAR(100),
                fiscal_year         VARCHAR(10),
                demand_no           VARCHAR(20),
                department_name     VARCHAR(255),
                major_head          VARCHAR(20),
                sub_major_head      VARCHAR(20),
                minor_head          VARCHAR(20),
                sub_head            VARCHAR(20),
                detail_head         VARCHAR(20),
                scheme_name         TEXT,
                scheme_key          VARCHAR(100),
                row_type            VARCHAR(50),
                budget_estimate     NUMERIC(18, 4),
                revised_estimate    NUMERIC(18, 4),
                actual_expenditure  NUMERIC(18, 4),
                source_pdf          VARCHAR(255),
                page_number         INTEGER,
                row_index           INTEGER,
                dataset_version     VARCHAR(50),
                created_at          TIMESTAMPTZ DEFAULT NOW()
            );
            CREATE INDEX IF NOT EXISTS idx_ba_department ON budget_allocations (department_name);
            CREATE INDEX IF NOT EXISTS idx_ba_fiscal_year ON budget_allocations (fiscal_year);
            CREATE INDEX IF NOT EXISTS idx_ba_major_head ON budget_allocations (major_head);
            CREATE INDEX IF NOT EXISTS idx_ba_scheme_key ON budget_allocations (scheme_key);
            CREATE INDEX IF NOT EXISTS idx_ba_row_type ON budget_allocations (row_type);
            CREATE INDEX IF NOT EXISTS idx_ba_source_pdf ON budget_allocations (source_pdf);
        """)
        try:
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_ba_scheme_name_trgm
                    ON budget_allocations USING GIN (scheme_name gin_trgm_ops);
                CREATE INDEX IF NOT EXISTS idx_ba_dept_name_trgm
                    ON budget_allocations USING GIN (department_name gin_trgm_ops);
            """)
        except Exception:
            pass
