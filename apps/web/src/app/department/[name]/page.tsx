import Link from 'next/link'
import BudgetTable from '@/components/BudgetTable'
import StatCard from '@/components/StatCard'
import { getDepartment, formatCrores } from '@/lib/api'

export const revalidate = 3600

export default async function DepartmentDetailPage({ params }: { params: { name: string } }) {
  const name = decodeURIComponent(params.name)
  let rows: any[] = []
  let error = ''

  try {
    rows = await getDepartment(name)
  } catch (e: any) {
    error = e.message
  }

  const totalBE = rows.reduce((s, r) => s + (r.budget_estimate ?? 0), 0)
  const totalRE = rows.reduce((s, r) => s + (r.revised_estimate ?? 0), 0)
  const totalAct = rows.reduce((s, r) => s + (r.actual_expenditure ?? 0), 0)
  const schemeRows = rows.filter(r => r.row_type !== 'total' && r.row_type !== 'grand_total' && r.row_type !== 'sub_total')

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <Link href="/departments" className="text-primary-600 hover:underline text-sm mb-4 inline-block">
        &larr; Back to Departments
      </Link>

      <h1 className="text-2xl font-bold text-gray-900 mt-2 mb-1">{name}</h1>
      <p className="text-gray-500 text-sm mb-6">Andhra Pradesh Budget 2026-27</p>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 mb-6">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <StatCard label="Budget Estimate" value={formatCrores(totalBE)} color="blue" />
        <StatCard label="Revised Estimate" value={formatCrores(totalRE)} color="purple" />
        <StatCard label="Actual Expenditure" value={formatCrores(totalAct)} color="green" />
      </div>

      <h2 className="text-lg font-semibold text-gray-800 mb-3">
        Schemes &amp; Heads ({schemeRows.length} rows)
      </h2>
      <BudgetTable rows={schemeRows} />
    </div>
  )
}
