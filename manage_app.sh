#!/bin/bash

# Landscaper Application Management Script
# This script helps manage the Flask application in the background

echo "🏠 Landscaper Application Management"
echo "===================================="

case "$1" in
    "start")
        echo "Starting Landscaper application in background..."
        nohup python app.py > app.log 2>&1 &
        echo "✅ Application started with PID: $!"
        echo "📝 Logs are being written to: app.log"
        echo "🌐 Access the application at: http://localhost:5000"
        ;;
    "stop")
        echo "Stopping Landscaper application..."
        pkill -f "python app.py"
        echo "✅ Application stopped"
        ;;
    "restart")
        echo "Restarting Landscaper application..."
        pkill -f "python app.py"
        sleep 2
        nohup python app.py > app.log 2>&1 &
        echo "✅ Application restarted with PID: $!"
        ;;
    "status")
        echo "Checking application status..."
        if pgrep -f "python app.py" > /dev/null; then
            PID=$(pgrep -f "python app.py")
            echo "✅ Application is running (PID: $PID)"
            echo "🌐 URL: http://localhost:5000"
            echo "📝 Log file: app.log"
        else
            echo "❌ Application is not running"
        fi
        ;;
    "logs")
        echo "Showing recent application logs..."
        echo "=== Last 20 lines of app.log ==="
        tail -20 app.log
        ;;
    "logs-follow")
        echo "Following application logs (Ctrl+C to stop)..."
        tail -f app.log
        ;;
    "test")
        echo "Testing application connectivity..."
        if curl -s http://localhost:5000 > /dev/null; then
            echo "✅ Application is responding at http://localhost:5000"
        else
            echo "❌ Application is not responding"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|logs-follow|test}"
        echo ""
        echo "Commands:"
        echo "  start        - Start the application in background"
        echo "  stop         - Stop the application"
        echo "  restart      - Restart the application"
        echo "  status       - Check if application is running"
        echo "  logs         - Show recent logs"
        echo "  logs-follow  - Follow logs in real-time"
        echo "  test         - Test application connectivity"
        ;;
esac
