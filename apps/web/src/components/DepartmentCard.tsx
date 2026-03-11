import Link from 'next/link'
import { DepartmentSummary, formatCrores } from '@/lib/api'

interface Props {
  dept: DepartmentSummary
  maxBudget: number
  rank: number
}

export default function DepartmentCard({ dept, maxBudget, rank }: Props) {
  const be = dept.total_budget_estimate_lakhs ?? 0
  const pct = maxBudget > 0 ? Math.round((be / maxBudget) * 100) : 0
  const name = dept.department_name ?? 'Unknown'

  return (
    <Link
      href={`/department/${encodeURIComponent(name)}`}
      className="block bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:shadow-md hover:border-primary-200 transition-all group"
    >
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-3">
          <span className="text-xs font-bold text-gray-400 w-6">{rank}</span>
          <h3 className="font-semibold text-gray-900 text-sm leading-snug group-hover:text-primary-700 line-clamp-2">
            {name}
          </h3>
        </div>
        <span className="text-sm font-bold text-primary-800 whitespace-nowrap">
          {formatCrores(be)}
        </span>
      </div>
      <div className="mt-3 ml-9">
        <div className="w-full bg-gray-100 rounded-full h-1.5">
          <div
            className="bg-primary-500 h-1.5 rounded-full transition-all"
            style={{ width: `${pct}%` }}
          />
        </div>
        <div className="flex justify-between mt-1">
          <span className="text-xs text-gray-400">RE: {formatCrores(dept.total_revised_estimate_lakhs)}</span>
          <span className="text-xs text-gray-400">{pct}% of top</span>
        </div>
      </div>
    </Link>
  )
}
