export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div>
            <span className="text-white font-semibold">AP Budget 2026-27</span>
            <p className="text-sm mt-1">Data sourced from the Andhra Pradesh Finance Department.</p>
          </div>
          <div className="text-sm text-center sm:text-right">
            <p>All amounts in Indian Rupees (Crores).</p>
            <p className="mt-1">Open data for public accountability.</p>
          </div>
        </div>
      </div>
    </footer>
  )
}
