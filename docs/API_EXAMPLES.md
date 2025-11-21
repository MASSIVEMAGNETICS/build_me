# API Examples

This document provides examples of using the OmniForge API.

## Table of Contents

- [Authentication](#authentication)
- [Health Check](#health-check)
- [System Information](#system-information)
- [Synchronous Analysis](#synchronous-analysis)
- [Asynchronous Analysis](#asynchronous-analysis)
- [Job Status](#job-status)
- [Python Client Examples](#python-client-examples)
- [JavaScript Client Examples](#javascript-client-examples)

---

## Authentication

Currently, the API does not require authentication. For production use, consider implementing:
- API keys
- OAuth 2.0
- JWT tokens

---

## Health Check

Check if the API is running:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "OmniForge",
  "version": "1.0.0"
}
```

---

## System Information

Get system capabilities:

```bash
curl http://localhost:8000/api/info
```

Response:
```json
{
  "name": "OmniForge",
  "version": "1.0.0",
  "description": "The Absolute Upgrade Engine",
  "features": [
    "Repository analysis",
    "Security scanning",
    "Code quality metrics",
    "Architecture detection",
    "Upgrade recommendations",
    "Self-healing capabilities"
  ],
  "supported_languages": [
    "Python",
    "JavaScript",
    "TypeScript",
    "Java",
    "Go",
    "Rust",
    "C/C++"
  ]
}
```

---

## Synchronous Analysis

For small repositories (< 1000 files):

```bash
curl -X POST http://localhost:8000/api/analyze-sync \
  -H "Content-Type: application/json" \
  -d '{
    "repo_path": "/path/to/repository"
  }'
```

Response:
```json
{
  "status": "completed",
  "report": {
    "timestamp": "2024-11-21T10:30:00",
    "repository_path": "/path/to/repository",
    "success": true,
    "analysis": {
      "total_files": 42,
      "total_lines": 1337,
      "languages": {
        "python": 30,
        "javascript": 12
      },
      "complexity_stats": {
        "avg": 5.2,
        "max": 15.0,
        "min": 1.0
      },
      "maintainability_score": 75.5,
      "architecture_type": "modular-library",
      "issues_count": 3
    },
    "security_scan": {
      "total_issues": 2,
      "critical": 0,
      "high": 1,
      "medium": 1,
      "low": 0
    },
    "recommendations": [
      "Add comprehensive unit tests",
      "Improve documentation coverage"
    ]
  },
  "summary": "..."
}
```

---

## Asynchronous Analysis

For large repositories:

### 1. Start Analysis Job

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "repo_path": "/path/to/large/repository"
  }'
```

Response:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Analysis job started"
}
```

### 2. Check Job Status

```bash
curl http://localhost:8000/api/jobs/550e8400-e29b-41d4-a716-446655440000
```

Response (pending):
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "progress": 45,
  "result": null,
  "error": null
}
```

Response (completed):
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "result": {
    "timestamp": "2024-11-21T10:35:00",
    "analysis": {...},
    "security_scan": {...},
    "recommendations": [...]
  },
  "error": null
}
```

---

## Python Client Examples

### Basic Usage

```python
import requests

# Start analysis
response = requests.post(
    'http://localhost:8000/api/analyze-sync',
    json={'repo_path': '/path/to/repo'}
)
result = response.json()

print(f"Files analyzed: {result['report']['analysis']['total_files']}")
print(f"Security issues: {result['report']['security_scan']['total_issues']}")
```

### Async Analysis with Polling

```python
import requests
import time

# Start job
response = requests.post(
    'http://localhost:8000/api/analyze',
    json={'repo_path': '/path/to/large/repo'}
)
job_id = response.json()['job_id']

# Poll for completion
while True:
    response = requests.get(f'http://localhost:8000/api/jobs/{job_id}')
    job = response.json()
    
    print(f"Status: {job['status']}, Progress: {job['progress']}%")
    
    if job['status'] == 'completed':
        print("Analysis complete!")
        print(job['result'])
        break
    elif job['status'] == 'failed':
        print(f"Analysis failed: {job['error']}")
        break
    
    time.sleep(2)
```

### Using the OmniForge Python Client

```python
from src.core.engine import OmniForgeEngine

# Direct usage (no API)
engine = OmniForgeEngine()
report = engine.analyze_repository('/path/to/repo')

# Print summary
summary = engine.generate_summary(report)
print(summary)

# Export to file
engine.export_report(report, 'report.json')
```

---

## JavaScript Client Examples

### Using Fetch API

```javascript
// Synchronous analysis
async function analyzeRepo(repoPath) {
  try {
    const response = await fetch('http://localhost:8000/api/analyze-sync', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ repo_path: repoPath }),
    });
    
    const result = await response.json();
    console.log('Analysis complete:', result);
    return result;
  } catch (error) {
    console.error('Analysis failed:', error);
  }
}

// Use it
analyzeRepo('/path/to/repo');
```

### Async Analysis with Polling

```javascript
async function analyzeRepoAsync(repoPath) {
  // Start job
  const startResponse = await fetch('http://localhost:8000/api/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repo_path: repoPath }),
  });
  
  const { job_id } = await startResponse.json();
  console.log('Job started:', job_id);
  
  // Poll for completion
  while (true) {
    const statusResponse = await fetch(
      `http://localhost:8000/api/jobs/${job_id}`
    );
    const job = await statusResponse.json();
    
    console.log(`Status: ${job.status}, Progress: ${job.progress}%`);
    
    if (job.status === 'completed') {
      console.log('Analysis complete!');
      return job.result;
    } else if (job.status === 'failed') {
      throw new Error(`Analysis failed: ${job.error}`);
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

// Use it
analyzeRepoAsync('/path/to/large/repo')
  .then(result => console.log('Result:', result))
  .catch(error => console.error('Error:', error));
```

### React Hook Example

```javascript
import { useState, useEffect } from 'react';

function useRepoAnalysis(repoPath) {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const analyze = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/analyze-sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_path: repoPath }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  return { result, loading, error, analyze };
}

// Usage in component
function AnalysisComponent() {
  const { result, loading, error, analyze } = useRepoAnalysis('/path/to/repo');
  
  return (
    <div>
      <button onClick={analyze} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze Repository'}
      </button>
      
      {error && <div>Error: {error}</div>}
      {result && <div>Files: {result.report.analysis.total_files}</div>}
    </div>
  );
}
```

---

## Error Handling

### Common Error Responses

**400 Bad Request**
```json
{
  "detail": "Repository path does not exist"
}
```

**404 Not Found**
```json
{
  "detail": "Job not found"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error",
  "detail": "Error message here"
}
```

### Handling Errors

```python
import requests

try:
    response = requests.post(
        'http://localhost:8000/api/analyze-sync',
        json={'repo_path': '/invalid/path'}
    )
    response.raise_for_status()  # Raises HTTPError for bad status
    result = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Response: {e.response.json()}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

---

## Rate Limiting

Currently, there is no rate limiting. For production:

```python
# Example: Simple rate limiting with decorator
from functools import wraps
import time

def rate_limit(calls=10, period=60):
    """Limit function calls"""
    min_interval = period / calls
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait = min_interval - elapsed
            if wait > 0:
                time.sleep(wait)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls=5, period=60)
def analyze_repo(path):
    # Your analysis code
    pass
```

---

## Best Practices

1. **Use async endpoints for large repositories** (> 1000 files)
2. **Implement retry logic** for transient failures
3. **Cache results** when analyzing the same repository
4. **Handle timeouts** appropriately
5. **Validate input** before sending to API
6. **Monitor job status** with exponential backoff
7. **Use connection pooling** for multiple requests

---

## Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can test all endpoints directly in your browser.

---

For more examples, see the [OmniForge repository](https://github.com/MASSIVEMAGNETICS/build_me).
