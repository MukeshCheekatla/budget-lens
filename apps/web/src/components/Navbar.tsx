'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const links = [
  { href: '/', label: 'Home' },
  { href: '/departments', label: 'Departments' },
  { href: '/schemes', label: 'Top Schemes' },
  { href: '/scst', label: 'SC/ST' },
]

export default function Navbar() {
  const pathname = usePathname()
  return (
    <nav className="bg-primary-800 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-accent-500 text-2xl font-bold">AP</span>
            <span className="font-semibold text-lg hidden sm:block">Budget 2026-27</span>
          </Link>
          <div className="flex gap-1">
            {links.map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  pathname === href
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-300 hover:bg-primary-700 hover:text-white'
                }`}
              >
                {label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}
