#!/usr/bin/env bash
#
# OmniForge Startup Script
# Start API server and optionally the web GUI
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

GUI_MODE=false
PORT=8000

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --gui)
            GUI_MODE=true
            shift
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--gui] [--port PORT]"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}Starting OmniForge...${NC}"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Run ./scripts/install.sh first."
    exit 1
fi

if [ "$GUI_MODE" = true ]; then
    echo -e "${GREEN}Starting in GUI mode...${NC}"
    echo -e "${BLUE}API Server: http://localhost:$PORT${NC}"
    echo -e "${BLUE}Web GUI: http://localhost:5173${NC}"
    echo ""
    
    # Start API server in background
    python -m uvicorn src.core.api:app --host 0.0.0.0 --port $PORT &
    API_PID=$!
    
    # Wait a bit for API to start
    sleep 2
    
    # Start frontend dev server
    npm run dev
    
    # Cleanup on exit
    kill $API_PID
else
    echo -e "${GREEN}Starting API server...${NC}"
    echo -e "${BLUE}Server: http://localhost:$PORT${NC}"
    echo -e "${BLUE}Docs: http://localhost:$PORT/docs${NC}"
    echo ""
    
    python -m uvicorn src.core.api:app --host 0.0.0.0 --port $PORT --reload
fi
