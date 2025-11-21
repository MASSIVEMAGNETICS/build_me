import React, { useState, useEffect } from 'react'
import './Dashboard.css'

function Dashboard() {
  const [stats, setStats] = useState({
    features: 8,
    languages: 7,
    scansCompleted: 0
  })

  const features = [
    { icon: '🔍', name: 'Code Analysis', desc: 'Deep code quality metrics' },
    { icon: '🛡️', name: 'Security Scan', desc: 'Vulnerability detection' },
    { icon: '⚡', name: 'Auto Upgrade', desc: 'Modern pattern conversion' },
    { icon: '📊', name: 'Metrics', desc: 'Complexity & maintainability' },
  ]

  return (
    <div className="dashboard fade-in">
      <div className="dashboard-header">
        <h2>System Overview</h2>
        <div className="status-indicator">
          <span className="status-dot"></span>
          <span>All Systems Operational</span>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">✨</div>
          <div className="stat-content">
            <div className="stat-value">{stats.features}</div>
            <div className="stat-label">Features</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💻</div>
          <div className="stat-content">
            <div className="stat-value">{stats.languages}</div>
            <div className="stat-label">Languages</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🚀</div>
          <div className="stat-content">
            <div className="stat-value">{stats.scansCompleted}</div>
            <div className="stat-label">Scans Today</div>
          </div>
        </div>
      </div>

      <div className="features-grid">
        {features.map((feature, index) => (
          <div key={index} className="feature-card">
            <div className="feature-icon">{feature.icon}</div>
            <h3>{feature.name}</h3>
            <p>{feature.desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Dashboard
