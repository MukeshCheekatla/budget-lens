import BudgetTable from '@/components/BudgetTable'
import StatCard from '@/components/StatCard'
import { getSCSP, getTSP, formatCrores } from '@/lib/api'

export const revalidate = 3600
export const metadata = { title: 'SC/ST Allocations | AP Budget 2026-27' }

export default async function SCSTPage() {
  let scsp: any[] = [], tsp: any[] = [], error = ''
  try {
    ;[scsp, tsp] = await Promise.all([getSCSP(), getTSP()])
  } catch (e: any) {
    error = e.message
  }

  const totalSCSP = scsp.reduce((s, r) => s + (r.budget_estimate ?? 0), 0)
  const totalTSP  = tsp.reduce((s, r) => s + (r.budget_estimate ?? 0), 0)

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">SC/ST Allocations</h1>
      <p className="text-gray-500 mb-8">Scheduled Caste Sub-Plan (SCSP) and Tribal Sub-Plan (TSP) — AP Budget 2026-27</p>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 mb-6">{error}</div>
      )}

      <div className="grid grid-cols-2 gap-4 mb-10">
        <StatCard label="Total SCSP (SC)" value={formatCrores(totalSCSP)} sub={`${scsp.length} rows`} color="green" />
        <StatCard label="Total TSP (ST)"  value={formatCrores(totalTSP)}  sub={`${tsp.length} rows`}  color="orange" />
      </div>

      <div className="space-y-10">
        <section>
          <h2 className="text-xl font-semibold text-gray-800 mb-3">
            Scheduled Caste Sub-Plan (SCSP)
            <span className="ml-2 text-sm font-normal text-gray-400">{scsp.length} allocations</span>
          </h2>
          <BudgetTable rows={scsp} showDept />
        </section>

        <section>
          <h2 className="text-xl font-semibold text-gray-800 mb-3">
            Tribal Sub-Plan (TSP)
            <span className="ml-2 text-sm font-normal text-gray-400">{tsp.length} allocations</span>
          </h2>
          <BudgetTable rows={tsp} showDept />
        </section>
      </div>
    </div>
  )
}
