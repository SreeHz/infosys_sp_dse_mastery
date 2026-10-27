#!/usr/bin/env bash
# ==============================================================================
# Infosys SP & DSE Web-Lab Engine: Unified Server Manager
# Usage: ./server.sh [start | stop | restart | status]
# ==============================================================================

ACTION="${1:-status}"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT=8080

case "$ACTION" in
    start)
        "$PROJECT_DIR/start_server.sh"
        ;;
    stop)
        "$PROJECT_DIR/stop_server.sh"
        ;;
    restart)
        echo -e "\033[96m🔄 Restarting Web-Lab Server...\033[0m"
        "$PROJECT_DIR/stop_server.sh"
        sleep 0.5
        "$PROJECT_DIR/start_server.sh"
        ;;
    status)
        if curl -s "http://localhost:$PORT/api/status" > /dev/null 2>&1; then
            PID=$(lsof -Pi :$PORT -sTCP:LISTEN -t 2>/dev/null | head -n 1)
            echo -e "\033[92m● Web-Lab Server is ONLINE (PID: ${PID:-active})\033[0m"
            echo -e "  📍 URL:  http://localhost:$PORT/index.html"
            echo -e "  📍 Port: $PORT"
        else
            echo -e "\033[91m○ Web-Lab Server is STOPPED\033[0m"
            echo -e "  To start it: ./start_server.sh"
        fi
        ;;
    *)
        echo "Usage: ./server.sh [start | stop | restart | status]"
        exit 1
        ;;
esac
