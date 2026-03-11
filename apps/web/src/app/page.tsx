import Link from 'next/link'
import SearchBar from '@/components/SearchBar'
import StatCard from '@/components/StatCard'
import { getSummary, getDepartments, getSCSP, getTSP, formatCrores } from '@/lib/api'

export const revalidate = 3600

export default async function HomePage() {
  let totalBE = 0, totalSCSP = 0, totalTSP = 0, deptCount = 0

  try {
    const [summary, depts, scsp, tsp] = await Promise.all([
      getSummary(), getDepartments(), getSCSP(), getTSP()
    ])
    const row = summary.find(r => r.fiscal_year === '2026-27') ?? summary[0]
    totalBE = row?.total_budget_estimate_lakhs ?? 0
    deptCount = depts.length
    totalSCSP = scsp.reduce((s, r) => s + (r.budget_estimate ?? 0), 0)
    totalTSP = tsp.reduce((s, r) => s + (r.budget_estimate ?? 0), 0)
  } catch (_) {}

  return (
    <div>
      {/* Hero */}
      <div className="bg-gradient-to-br from-primary-800 to-primary-900 text-white py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-block bg-accent-500 text-white text-xs font-bold px-3 py-1 rounded-full mb-4 uppercase tracking-wide">
            Open Budget Data
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-4">
            Andhra Pradesh Budget
            <span className="text-accent-400"> 2026-27</span>
          </h1>
          <p className="text-lg text-blue-200 mb-8">
            Explore how public money is allocated — by department, scheme, and community.
          </p>
          <SearchBar />
        </div>
      </div>

      {/* Stats */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatCard label="Total Budget" value={formatCrores(totalBE)} sub="Budget Estimate 2026-27" color="blue" />
          <StatCard label="Departments" value={deptCount.toString()} sub="Active in 2026-27" color="purple" />
          <StatCard label="SCSP Allocation" value={formatCrores(totalSCSP)} sub="Scheduled Caste Sub-Plan" color="green" />
          <StatCard label="TSP Allocation" value={formatCrores(totalTSP)} sub="Tribal Sub-Plan" color="orange" />
        </div>
      </div>

      {/* Quick Links */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 pb-12">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Explore Budget Data</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <Link href="/departments" className="block bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md hover:border-primary-300 transition-all group">
            <div className="text-3xl mb-3">🏗️</div>
            <h3 className="font-bold text-gray-900 group-hover:text-primary-700">Browse Departments</h3>
            <p className="text-sm text-gray-500 mt-1">See all {deptCount} departments and their total allocations</p>
          </Link>
          <Link href="/schemes" className="block bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md hover:border-primary-300 transition-all group">
            <div className="text-3xl mb-3">📋</div>
            <h3 className="font-bold text-gray-900 group-hover:text-primary-700">Top Schemes</h3>
            <p className="text-sm text-gray-500 mt-1">The 50 highest-funded schemes in the state budget</p>
          </Link>
          <Link href="/scst" className="block bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md hover:border-primary-300 transition-all group">
            <div className="text-3xl mb-3">🤝</div>
            <h3 className="font-bold text-gray-900 group-hover:text-primary-700">SC/ST Explorer</h3>
            <p className="text-sm text-gray-500 mt-1">Scheduled Caste and Tribe sub-plan allocations</p>
          </Link>
        </div>
      </div>
    </div>
  )
}
