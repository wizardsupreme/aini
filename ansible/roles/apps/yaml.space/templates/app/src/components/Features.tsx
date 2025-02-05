export function Features() {
  const features = [
    {
      title: "Nextcloud Integration",
      description: "Secure file storage and collaboration platform with integrated office suite",
      icon: "🗄️"
    },
    {
      title: "LibreChat",
      description: "Advanced AI chat interface supporting multiple models",
      icon: "💬"
    },
    {
      title: "NocoDB",
      description: "Open-source Airtable alternative for structured data management",
      icon: "📊"
    },
    {
      title: "Authentication",
      description: "Secure access management with Authelia",
      icon: "🔐"
    }
  ]

  return (
    <section id="features" className="py-20 px-6 bg-black/30">
      <div className="container mx-auto">
        <h2 className="text-4xl font-bold text-center mb-16">Features</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="p-6 rounded-lg bg-gray-800/50 backdrop-blur-sm hover:bg-gray-800/70 transition">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-400">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
} 