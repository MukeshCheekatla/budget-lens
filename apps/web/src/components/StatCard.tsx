interface StatCardProps {
  label: string
  value: string
  sub?: string
  color?: 'blue' | 'orange' | 'green' | 'purple'
}

const colorMap = {
  blue:   'border-primary-500 bg-primary-50 text-primary-800',
  orange: 'border-accent-500 bg-orange-50 text-orange-800',
  green:  'border-green-500 bg-green-50 text-green-800',
  purple: 'border-purple-500 bg-purple-50 text-purple-800',
}

export default function StatCard({ label, value, sub, color = 'blue' }: StatCardProps) {
  return (
    <div className={`rounded-xl border-l-4 p-5 shadow-sm ${colorMap[color]}`}>
      <p className="text-sm font-medium opacity-70">{label}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
      {sub && <p className="text-xs mt-1 opacity-60">{sub}</p>}
    </div>
  )
}
