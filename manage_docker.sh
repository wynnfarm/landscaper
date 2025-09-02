#!/bin/bash

# Landscaper Docker Management Script
# This script helps manage the Docker-based Landscaper application

echo "🏠 Landscaper Docker Management"
echo "==============================="

case "$1" in
    "start")
        echo "Starting Landscaper Docker services..."
        docker compose up -d
        echo "✅ Services started"
        echo "🌐 Application available at: http://localhost:5000"
        echo "🗄️  Database available at: localhost:5433"
        echo "📊 pgAdmin available at: http://localhost:8080 (if enabled)"
        ;;
    "stop")
        echo "Stopping Landscaper Docker services..."
        docker compose down
        echo "✅ Services stopped"
        ;;
    "restart")
        echo "Restarting Landscaper Docker services..."
        docker compose down
        docker compose up -d
        echo "✅ Services restarted"
        ;;
    "rebuild")
        echo "Rebuilding and starting Landscaper Docker services..."
        docker compose down
        docker compose build --no-cache
        docker compose up -d
        echo "✅ Services rebuilt and started"
        ;;
    "status")
        echo "Checking Docker services status..."
        docker compose ps
        ;;
    "logs")
        echo "Showing application logs..."
        docker compose logs landscaper-web --tail 20
        ;;
    "logs-follow")
        echo "Following application logs (Ctrl+C to stop)..."
        docker compose logs -f landscaper-web
        ;;
    "logs-all")
        echo "Showing all services logs..."
        docker compose logs --tail 20
        ;;
    "shell")
        echo "Opening shell in web container..."
        docker compose exec landscaper-web /bin/bash
        ;;
    "test")
        echo "Testing application connectivity..."
        if curl -s http://localhost:5000 > /dev/null; then
            echo "✅ Application is responding at http://localhost:5000"
        else
            echo "❌ Application is not responding"
        fi
        ;;
    "clean")
        echo "Cleaning up Docker resources..."
        docker compose down -v
        docker system prune -f
        echo "✅ Cleanup completed"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|rebuild|status|logs|logs-follow|logs-all|shell|test|clean}"
        echo ""
        echo "Commands:"
        echo "  start        - Start all Docker services"
        echo "  stop         - Stop all Docker services"
        echo "  restart      - Restart all Docker services"
        echo "  rebuild      - Rebuild and start services"
        echo "  status       - Show service status"
        echo "  logs         - Show web app logs"
        echo "  logs-follow  - Follow web app logs"
        echo "  logs-all     - Show all service logs"
        echo "  shell        - Open shell in web container"
        echo "  test         - Test application connectivity"
        echo "  clean        - Clean up Docker resources"
        ;;
esac
