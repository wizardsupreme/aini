export function Header() {
  return (
    <header className="fixed w-full bg-transparent backdrop-blur-sm z-50">
      <nav className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="text-2xl font-bold">YAML.space</div>
          <div className="hidden md:flex space-x-8">
            <a href="#features" className="hover:text-blue-400 transition">Features</a>
            <a href="#contact" className="hover:text-blue-400 transition">Contact</a>
          </div>
        </div>
      </nav>
    </header>
  )
} 