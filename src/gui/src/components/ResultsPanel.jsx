import React from 'react'
import './ResultsPanel.css'

function ResultsPanel({ result }) {
  const { report, summary } = result

  const getSeverityColor = (count, isCritical = false) => {
    if (count === 0) return 'success'
    if (isCritical || count > 5) return 'error'
    return 'warning'
  }

  return (
    <div className="results-panel fade-in">
      <h2>📊 Analysis Results</h2>

      <div className="results-grid">
        {/* Code Analysis Card */}
        <div className="result-card">
          <h3>Code Analysis</h3>
          <div className="metrics-list">
            <div className="metric-item">
              <span className="metric-label">Total Files:</span>
              <span className="metric-value">{report.analysis.total_files}</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Total Lines:</span>
              <span className="metric-value">{report.analysis.total_lines.toLocaleString()}</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Architecture:</span>
              <span className="metric-value badge">{report.analysis.architecture_type}</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Maintainability:</span>
              <span className={`metric-value ${report.analysis.maintainability_score >= 50 ? 'text-success' : 'text-warning'}`}>
                {report.analysis.maintainability_score.toFixed(1)}/100
              </span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Avg Complexity:</span>
              <span className={`metric-value ${report.analysis.complexity_stats.avg <= 10 ? 'text-success' : 'text-warning'}`}>
                {report.analysis.complexity_stats.avg.toFixed(1)}
              </span>
            </div>
          </div>

          {/* Languages */}
          {Object.keys(report.analysis.languages).length > 0 && (
            <div className="languages-section">
              <h4>Languages Detected</h4>
              <div className="languages-grid">
                {Object.entries(report.analysis.languages).map(([lang, count]) => (
                  <div key={lang} className="language-tag">
                    <span className="lang-name">{lang}</span>
                    <span className="lang-count">{count}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Security Scan Card */}
        <div className="result-card">
          <h3>🛡️ Security Scan</h3>
          <div className="security-summary">
            <div className="security-total">
              <span className="total-label">Total Issues:</span>
              <span className="total-value">{report.security_scan.total_issues}</span>
            </div>
            <div className="security-breakdown">
              <div className={`severity-item severity-${getSeverityColor(report.security_scan.critical, true)}`}>
                <span className="severity-label">Critical</span>
                <span className="severity-value">{report.security_scan.critical}</span>
              </div>
              <div className={`severity-item severity-${getSeverityColor(report.security_scan.high)}`}>
                <span className="severity-label">High</span>
                <span className="severity-value">{report.security_scan.high}</span>
              </div>
              <div className={`severity-item severity-${getSeverityColor(report.security_scan.medium)}`}>
                <span className="severity-label">Medium</span>
                <span className="severity-value">{report.security_scan.medium}</span>
              </div>
              <div className="severity-item severity-success">
                <span className="severity-label">Low</span>
                <span className="severity-value">{report.security_scan.low}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations */}
      {report.recommendations && report.recommendations.length > 0 && (
        <div className="result-card recommendations-card">
          <h3>💡 Recommendations</h3>
          <ul className="recommendations-list">
            {report.recommendations.map((rec, index) => (
              <li key={index} className="recommendation-item">
                <span className="rec-number">{index + 1}</span>
                <span className="rec-text">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Summary Text */}
      {summary && (
        <div className="result-card summary-card">
          <h3>📋 Detailed Summary</h3>
          <pre className="summary-text">{summary}</pre>
        </div>
      )}
    </div>
  )
}

export default ResultsPanel
