export function Hero() {
  return (
    <section className="pt-32 pb-20 px-6">
      <div className="container mx-auto text-center">
        <h1 className="text-5xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
          AI Development Stack
        </h1>
        <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto mb-12">
          A complete, integrated suite of tools for modern AI development and collaboration
        </p>
        <div className="flex justify-center space-x-6">
          <a href="#features" className="bg-blue-500 hover:bg-blue-600 px-8 py-3 rounded-lg font-semibold transition">
            Explore Features
          </a>
          <a href="https://auth.yaml.space" className="border border-blue-500 hover:bg-blue-500/10 px-8 py-3 rounded-lg font-semibold transition">
            Login
          </a>
        </div>
      </div>
    </section>
  )
} 