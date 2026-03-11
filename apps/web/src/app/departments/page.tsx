import DepartmentCard from '@/components/DepartmentCard'
import { getDepartments } from '@/lib/api'

export const revalidate = 3600
export const metadata = { title: 'Departments | AP Budget 2026-27' }

export default async function DepartmentsPage() {
  let depts = []
  let error = ''
  try {
    depts = await getDepartments()
  } catch (e: any) {
    error = e.message
  }

  const maxBudget = depts[0]?.total_budget_estimate_lakhs ?? 1

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">All Departments</h1>
        <p className="text-gray-500 mt-2">Andhra Pradesh Budget 2026-27 — sorted by Budget Estimate (highest first)</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 mb-6">
          Could not load data: {error}. Make sure the API is running.
        </div>
      )}

      {!error && depts.length === 0 && (
        <div className="text-center py-20 text-gray-400">
          <p className="text-lg">No departments found.</p>
          <p className="text-sm mt-2">Ensure the database is loaded and the API is reachable.</p>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {depts.map((dept, i) => (
          <DepartmentCard key={i} dept={dept} maxBudget={maxBudget} rank={i + 1} />
        ))}
      </div>
    </div>
  )
}
