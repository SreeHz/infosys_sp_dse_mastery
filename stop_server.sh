#!/usr/bin/env bash
# ==============================================================================
# Infosys SP & DSE Web-Lab Engine: Stop Server Script
# ==============================================================================

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$PROJECT_DIR/.server.pid"
PORT=8080

STOPPED=0

# 1. Stop via PID file
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "\033[93m🛑 Terminating server process (PID: $PID)...\033[0m"
        kill "$PID" 2>/dev/null
        # Wait up to 3 seconds for graceful shutdown
        for i in {1..15}; do
            if ! ps -p "$PID" > /dev/null 2>&1; then
                break
            fi
            sleep 0.2
        done
        # Force kill if still lingering
        if ps -p "$PID" > /dev/null 2>&1; then
            kill -9 "$PID" 2>/dev/null
        fi
        STOPPED=1
    fi
    rm -f "$PID_FILE"
fi

# 2. Check for any remaining processes on port 8080 or matching vertex_lab_server
REMAINING_PIDS=$(lsof -Pi :$PORT -sTCP:LISTEN -t 2>/dev/null)
if [ -n "$REMAINING_PIDS" ]; then
    echo -e "\033[93m🧹 Releasing remaining processes on port $PORT ($REMAINING_PIDS)...\033[0m"
    kill -9 $REMAINING_PIDS 2>/dev/null
    STOPPED=1
fi

# 3. Double check process name
PY_PIDS=$(pgrep -f "vertex_lab_server.py" 2>/dev/null)
if [ -n "$PY_PIDS" ]; then
    echo -e "\033[93m🧹 Terminating vertex_lab_server process ($PY_PIDS)...\033[0m"
    kill -9 $PY_PIDS 2>/dev/null
    STOPPED=1
fi

if [ $STOPPED -eq 1 ]; then
    echo -e "\033[92m========================================================\033[0m"
    echo -e "\033[92m✅ Server has been STOPPED successfully!\033[0m"
    echo -e "   Port $PORT is now free."
    echo -e "   To start it again: ./start_server.sh"
    echo -e "\033[92m========================================================\033[0m"
else
    echo -e "\033[90mℹ️  No running server was found on port $PORT.\033[0m"
fi
