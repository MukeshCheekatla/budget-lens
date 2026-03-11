'use client'
import { useRouter } from 'next/navigation'
import { useState } from 'react'

export default function SearchBar({ defaultValue = '' }: { defaultValue?: string }) {
  const [query, setQuery] = useState(defaultValue)
  const router = useRouter()

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim().length >= 2) {
      router.push(`/search?q=${encodeURIComponent(query.trim())}`)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search schemes, departments... e.g. education, health, SCSP"
          className="flex-1 px-4 py-3 rounded-xl border border-gray-300 shadow-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-base"
        />
        <button
          type="submit"
          className="px-6 py-3 bg-primary-800 text-white rounded-xl font-semibold hover:bg-primary-700 transition-colors shadow-sm"
        >
          Search
        </button>
      </div>
    </form>
  )
}
