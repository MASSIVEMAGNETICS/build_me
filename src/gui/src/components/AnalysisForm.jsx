import React, { useState } from 'react'
import './AnalysisForm.css'

function AnalysisForm({ onAnalysisStart, onAnalysisComplete, onAnalysisError, isAnalyzing }) {
  const [repoPath, setRepoPath] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!repoPath.trim()) {
      alert('Please enter a repository path')
      return
    }

    onAnalysisStart()

    try {
      const response = await fetch('/api/analyze-sync', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repo_path: repoPath }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      onAnalysisComplete(data)
    } catch (error) {
      onAnalysisError(error)
      alert(`Analysis failed: ${error.message}`)
    }
  }

  return (
    <div className="analysis-form-container fade-in">
      <h2>🚀 Analyze Repository</h2>
      <form onSubmit={handleSubmit} className="analysis-form">
        <div className="form-group">
          <label htmlFor="repoPath">Repository Path</label>
          <input
            type="text"
            id="repoPath"
            value={repoPath}
            onChange={(e) => setRepoPath(e.target.value)}
            placeholder="/path/to/your/repository"
            disabled={isAnalyzing}
            className="form-input"
          />
          <p className="form-help">
            Enter the absolute path to the repository you want to analyze
          </p>
        </div>

        <button
          type="submit"
          disabled={isAnalyzing}
          className={`btn btn-primary ${isAnalyzing ? 'btn-loading' : ''}`}
        >
          {isAnalyzing ? (
            <>
              <span className="spinner"></span>
              Analyzing...
            </>
          ) : (
            <>
              <span>⚡</span>
              Start Analysis
            </>
          )}
        </button>
      </form>
    </div>
  )
}

export default AnalysisForm
