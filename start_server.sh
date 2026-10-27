#!/usr/bin/env bash
# ==============================================================================
# Infosys SP & DSE Web-Lab Engine: Start Server Script
# ==============================================================================

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$PROJECT_DIR/.server.pid"
LOG_FILE="$PROJECT_DIR/server.log"
PORT=8080

# 1. Check if server is already responding on port 8080
if curl -s "http://localhost:$PORT/api/status" > /dev/null 2>&1; then
    RUNNING_PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t 2>/dev/null | head -n 1)
    echo -e "\033[93m⚠️  Server is ALREADY RUNNING (PID: ${RUNNING_PID:-active}) on http://localhost:$PORT\033[0m"
    echo -e "   📍 Open in Chrome: http://localhost:$PORT/index.html"
    echo -e "   📍 View logs:      tail -f $LOG_FILE"
    echo -e "   🛑 Stop it:        ./stop_server.sh"
    exit 0
fi

# 2. Clean up any stale PID file
if [ -f "$PID_FILE" ]; then
    rm -f "$PID_FILE"
fi

echo -e "\033[96m🚀 Starting Vertex AI Web-Lab Server...\033[0m"

# 3. Start completely detached via setsid
setsid /usr/bin/python3 "$PROJECT_DIR/vertex_lab_server.py" > "$LOG_FILE" 2>&1 </dev/null &
LAUNCH_PID=$!

# 4. Wait up to 3 seconds for it to become healthy
HEALTHY=0
for i in {1..15}; do
    if curl -s "http://localhost:$PORT/api/status" > /dev/null 2>&1; then
        HEALTHY=1
        break
    fi
    sleep 0.2
done

if [ $HEALTHY -eq 1 ]; then
    # Grab the actual listening PID on port 8080
    ACTUAL_PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t 2>/dev/null | head -n 1)
    FINAL_PID=${ACTUAL_PID:-$LAUNCH_PID}
    echo "$FINAL_PID" > "$PID_FILE"

    echo -e "\033[92m========================================================\033[0m"
    echo -e "\033[92m✅ Server started successfully! (PID: $FINAL_PID)\033[0m"
    echo -e "\033[1;97m📍 Master Hub:   \033[96mhttp://localhost:$PORT/index.html\033[0m"
    echo -e "\033[1;97m📍 Logs:         \033[90m$LOG_FILE\033[0m"
    echo -e "\033[1;97m🛑 Stop Command: \033[93m./stop_server.sh\033[0m"
    echo -e "\033[92m========================================================\033[0m"
else
    echo -e "\033[91m❌ Server failed to respond on http://localhost:$PORT within 3 seconds.\033[0m"
    echo -e "   Check log file: cat $LOG_FILE"
    exit 1
fi
