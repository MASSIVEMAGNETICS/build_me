import React, { useState } from 'react'
import './App.css'
import Dashboard from './components/Dashboard'
import AnalysisForm from './components/AnalysisForm'
import ResultsPanel from './components/ResultsPanel'

function App() {
  const [analysisResult, setAnalysisResult] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const handleAnalysisStart = () => {
    setIsAnalyzing(true)
    setAnalysisResult(null)
  }

  const handleAnalysisComplete = (result) => {
    setIsAnalyzing(false)
    setAnalysisResult(result)
  }

  const handleAnalysisError = (error) => {
    setIsAnalyzing(false)
    console.error('Analysis error:', error)
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-icon">⚡</div>
            <h1 className="logo-text">OmniForge</h1>
          </div>
          <p className="tagline">The Absolute Upgrade Engine</p>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          <Dashboard />
          
          <div className="analysis-section">
            <AnalysisForm
              onAnalysisStart={handleAnalysisStart}
              onAnalysisComplete={handleAnalysisComplete}
              onAnalysisError={handleAnalysisError}
              isAnalyzing={isAnalyzing}
            />

            {analysisResult && (
              <ResultsPanel result={analysisResult} />
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>&copy; 2024 OmniForge. Built with intelligence and precision.</p>
      </footer>
    </div>
  )
}

export default App
