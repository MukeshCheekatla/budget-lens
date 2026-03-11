import { Suspense } from 'react'
import SearchBar from '@/components/SearchBar'
import BudgetTable from '@/components/BudgetTable'
import { searchBudget } from '@/lib/api'

export const metadata = { title: 'Search | AP Budget 2026-27' }

async function SearchResults({ q }: { q: string }) {
  if (!q || q.length < 2) {
    return <p className="text-gray-400 text-center py-12">Enter at least 2 characters to search.</p>
  }
  let results: any[] = []
  let error = ''
  try {
    results = await searchBudget(q)
  } catch (e: any) {
    error = e.message
  }
  if (error) {
    return <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3">{error}</div>
  }
  if (!results.length) {
    return (
      <div className="text-center py-16">
        <p className="text-gray-500 text-lg">No results found for &quot;{q}&quot;</p>
        <p className="text-gray-400 text-sm mt-2">Try a different keyword, e.g. &quot;education&quot; or &quot;health&quot;</p>
      </div>
    )
  }
  return (
    <div>
      <p className="text-sm text-gray-500 mb-4">{results.length} result{results.length !== 1 ? 's' : ''} for &quot;{q}&quot;</p>
      <BudgetTable rows={results} showDept />
    </div>
  )
}

export default function SearchPage({ searchParams }: { searchParams: { q?: string } }) {
  const q = searchParams.q ?? ''
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Search Budget Data</h1>
      <SearchBar defaultValue={q} />
      <div className="mt-8">
        <Suspense fallback={
          <div className="animate-pulse space-y-3">
            {[...Array(5)].map((_, i) => <div key={i} className="h-10 bg-gray-200 rounded" />)}
          </div>
        }>
          <SearchResults q={q} />
        </Suspense>
      </div>
    </div>
  )
}
