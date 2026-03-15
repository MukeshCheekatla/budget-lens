"""
models.py -- Pydantic v2 response models for the AP Budget API.

All amount fields are in Lakhs INR (float).
Optional fields map to nullable DB columns.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    status: str
    version: str
    description: str


class DepartmentSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    department_name: Optional[str]
    total_budget_estimate_lakhs: Optional[float]
    total_revised_estimate_lakhs: Optional[float]
    total_actual_expenditure_lakhs: Optional[float]
    fiscal_year: Optional[str]
    state: Optional[str]


class BudgetRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    state: Optional[str]
    fiscal_year: Optional[str]
    demand_no: Optional[str]
    department_name: Optional[str]
    major_head: Optional[str]
    sub_major_head: Optional[str]
    minor_head: Optional[str]
    sub_head: Optional[str]
    detail_head: Optional[str]
    scheme_name: Optional[str]
    scheme_key: Optional[str]
    row_type: Optional[str]
    budget_estimate: Optional[float]
    revised_estimate: Optional[float]
    actual_expenditure: Optional[float]
    source_pdf: Optional[str]
    page_number: Optional[int]
    row_index: Optional[int]
    dataset_version: Optional[str]


class SearchResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    state: Optional[str]
    fiscal_year: Optional[str]
    department_name: Optional[str]
    major_head: Optional[str]
    scheme_name: Optional[str]
    scheme_key: Optional[str]
    row_type: Optional[str]
    budget_estimate: Optional[float]
    revised_estimate: Optional[float]
    actual_expenditure: Optional[float]
    source_pdf: Optional[str]


class MajorHeadRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    major_head: Optional[str]
    fiscal_year: Optional[str]
    state: Optional[str]
    department_name: Optional[str]
    scheme_name: Optional[str]
    row_type: Optional[str]
    budget_estimate: Optional[float]
    revised_estimate: Optional[float]
    actual_expenditure: Optional[float]


class TopScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    scheme_name: Optional[str]
    scheme_key: Optional[str]
    department_name: Optional[str]
    fiscal_year: Optional[str]
    state: Optional[str]
    major_head: Optional[str]
    total_budget_estimate_lakhs: Optional[float]
    total_revised_estimate_lakhs: Optional[float]
    total_actual_expenditure_lakhs: Optional[float]


class SummaryRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    fiscal_year: Optional[str]
    state: Optional[str]
    total_budget_estimate_lakhs: Optional[float]
    total_revised_estimate_lakhs: Optional[float]
    total_actual_expenditure_lakhs: Optional[float]
    row_count: int


class SCSPRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    state: Optional[str]
    fiscal_year: Optional[str]
    department_name: Optional[str]
    major_head: Optional[str]
    scheme_name: Optional[str]
    scheme_key: Optional[str]
    row_type: Optional[str]
    budget_estimate: Optional[float]
    revised_estimate: Optional[float]
    actual_expenditure: Optional[float]
    source_pdf: Optional[str]
    page_number: Optional[int]


class TSPRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    state: Optional[str]
    fiscal_year: Optional[str]
    department_name: Optional[str]
    major_head: Optional[str]
    scheme_name: Optional[str]
    scheme_key: Optional[str]
    row_type: Optional[str]
    budget_estimate: Optional[float]
    revised_estimate: Optional[float]
    actual_expenditure: Optional[float]
    source_pdf: Optional[str]
    page_number: Optional[int]


class YearsResponse(BaseModel):
    fiscal_years: list[str]
    count: int


class PaginationMeta(BaseModel):
    total: int
    limit: int
    offset: int
    has_more: bool
