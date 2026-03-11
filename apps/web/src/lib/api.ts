export const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface DepartmentSummary {
  department_name: string | null
  fiscal_year: string | null
  state: string | null
  total_budget_estimate_lakhs: number | null
  total_revised_estimate_lakhs: number | null
  total_actual_expenditure_lakhs: number | null
}

export interface BudgetRow {
  id: number
  state: string | null
  fiscal_year: string | null
  demand_no: string | null
  department_name: string | null
  major_head: string | null
  sub_major_head: string | null
  minor_head: string | null
  sub_head: string | null
  detail_head: string | null
  scheme_name: string | null
  scheme_key: string | null
  row_type: string | null
  budget_estimate: number | null
  revised_estimate: number | null
  actual_expenditure: number | null
  source_pdf: string | null
  page_number: number | null
}

export interface SearchResult {
  id: number
  state: string | null
  fiscal_year: string | null
  department_name: string | null
  major_head: string | null
  scheme_name: string | null
  scheme_key: string | null
  row_type: string | null
  budget_estimate: number | null
  revised_estimate: number | null
  actual_expenditure: number | null
}

export interface TopScheme {
  scheme_name: string | null
  scheme_key: string | null
  department_name: string | null
  fiscal_year: string | null
  state: string | null
  major_head: string | null
  total_budget_estimate_lakhs: number | null
  total_revised_estimate_lakhs: number | null
  total_actual_expenditure_lakhs: number | null
}

export interface SummaryRow {
  fiscal_year: string | null
  state: string | null
  total_budget_estimate_lakhs: number | null
  total_revised_estimate_lakhs: number | null
  total_actual_expenditure_lakhs: number | null
  row_count: number
}

export interface SCSTRow {
  id: number
  state: string | null
  fiscal_year: string | null
  department_name: string | null
  major_head: string | null
  scheme_name: string | null
  scheme_key: string | null
  row_type: string | null
  budget_estimate: number | null
  revised_estimate: number | null
  actual_expenditure: number | null
  source_pdf: string | null
  page_number: number | null
}

async function apiFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { next: { revalidate: 3600 } })
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`)
  return res.json()
}

export async function getDepartments(year = '2026-27'): Promise<DepartmentSummary[]> {
  return apiFetch<DepartmentSummary[]>(`/departments?fiscal_year=${encodeURIComponent(year)}&limit=100`)
}

export async function getDepartment(name: string, year = '2026-27'): Promise<BudgetRow[]> {
  return apiFetch<BudgetRow[]>(`/department/${encodeURIComponent(name)}?fiscal_year=${encodeURIComponent(year)}&limit=200`)
}

export async function searchBudget(q: string): Promise<SearchResult[]> {
  return apiFetch<SearchResult[]>(`/search?q=${encodeURIComponent(q)}&limit=50`)
}

export async function getTopSchemes(year = '2026-27'): Promise<TopScheme[]> {
  return apiFetch<TopScheme[]>(`/schemes/top?fiscal_year=${encodeURIComponent(year)}&limit=50`)
}

export async function getSCSP(year = '2026-27'): Promise<SCSTRow[]> {
  return apiFetch<SCSTRow[]>(`/scsp?fiscal_year=${encodeURIComponent(year)}&limit=200`)
}

export async function getTSP(year = '2026-27'): Promise<SCSTRow[]> {
  return apiFetch<SCSTRow[]>(`/tsp?fiscal_year=${encodeURIComponent(year)}&limit=200`)
}

export async function getSummary(): Promise<SummaryRow[]> {
  return apiFetch<SummaryRow[]>('/summary')
}

// Format lakhs to crores with Indian number formatting
export function formatCrores(lakhs: number | null | undefined): string {
  if (lakhs == null) return 'N/A'
  const crores = lakhs / 100
  if (crores >= 1000) {
    return '\u20b9' + (crores / 1000).toLocaleString('en-IN', { maximumFractionDigits: 1 }) + 'K Cr'
  }
  return '\u20b9' + crores.toLocaleString('en-IN', { maximumFractionDigits: 0 }) + ' Cr'
}

export function formatLakhs(lakhs: number | null | undefined): string {
  if (lakhs == null) return 'N/A'
  return '\u20b9' + lakhs.toLocaleString('en-IN', { maximumFractionDigits: 0 }) + ' L'
}
