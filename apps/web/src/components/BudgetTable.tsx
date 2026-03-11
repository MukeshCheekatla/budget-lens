import { formatCrores } from '@/lib/api'

interface Row {
  scheme_name?: string | null
  department_name?: string | null
  major_head?: string | null
  row_type?: string | null
  budget_estimate?: number | null
  revised_estimate?: number | null
  actual_expenditure?: number | null
}

interface Props {
  rows: Row[]
  showDept?: boolean
}

export default function BudgetTable({ rows, showDept = false }: Props) {
  if (!rows.length) {
    return <p className="text-gray-500 text-sm py-8 text-center">No data found.</p>
  }
  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-50 text-gray-600 uppercase text-xs">
          <tr>
            {showDept && <th className="px-4 py-3 text-left">Department</th>}
            <th className="px-4 py-3 text-left">Scheme / Head</th>
            <th className="px-4 py-3 text-left">Major Head</th>
            <th className="px-4 py-3 text-right">Budget Est.</th>
            <th className="px-4 py-3 text-right">Revised Est.</th>
            <th className="px-4 py-3 text-right">Actuals</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {rows.map((row, i) => (
            <tr
              key={i}
              className={`hover:bg-gray-50 ${
                row.row_type === 'total' || row.row_type === 'grand_total'
                  ? 'font-semibold bg-blue-50'
                  : ''
              }`}
            >
              {showDept && (
                <td className="px-4 py-2 text-gray-700 max-w-xs truncate">{row.department_name ?? '-'}</td>
              )}
              <td className="px-4 py-2 text-gray-900 max-w-sm">
                <span className="line-clamp-2">{row.scheme_name ?? '-'}</span>
              </td>
              <td className="px-4 py-2 text-gray-500">{row.major_head ?? '-'}</td>
              <td className="px-4 py-2 text-right font-medium text-primary-700">{formatCrores(row.budget_estimate)}</td>
              <td className="px-4 py-2 text-right text-gray-600">{formatCrores(row.revised_estimate)}</td>
              <td className="px-4 py-2 text-right text-gray-500">{formatCrores(row.actual_expenditure)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
