#!/bin/bash
# Port Availability Checker and Server Starter

echo "🔍 PORT AVAILABILITY CHECKER"
echo "============================"

# Function to check if port is available
check_port() {
    local port=$1
    local service=$2
    if lsof -i :$port > /dev/null 2>&1; then
        echo "❌ Port $port ($service): IN USE"
        lsof -i :$port | head -2
        return 1
    else
        echo "✅ Port $port ($service): AVAILABLE"
        return 0
    fi
}

# Function to start server if port is available
start_server_if_available() {
    local port=$1
    local service=$2
    local command=$3
    
    if check_port $port $service; then
        echo "🚀 Starting $service on port $port..."
        eval "$command"
        sleep 2
        if lsof -i :$port > /dev/null 2>&1; then
            echo "✅ $service started successfully on port $port"
        else
            echo "❌ Failed to start $service on port $port"
        fi
    else
        echo "⚠️  Skipping $service - port $port is in use"
    fi
}

# Check all required ports
echo "📊 Current Port Status:"
check_port 5000 "Flask App"
check_port 8000 "Context Manager"
check_port 8001 "Persona Manager" 
check_port 5433 "Database"

echo -e "\n🎯 Starting Services:"

# Start Context Manager (port 8000)
start_server_if_available 8000 "Context Manager" "cd /Users/wynnfarm/dev/context-manager-mcp && python -c \"import uvicorn; from server import app; uvicorn.run(app, host='0.0.0.0', port=8000)\" &"

# Start Persona Manager (port 8001)
start_server_if_available 8001 "Persona Manager" "cd /Users/wynnfarm/dev/persona-manager-mcp && python -c \"import uvicorn; from http_server import app; uvicorn.run(app, host='0.0.0.0', port=8001)\" &"

# Start Flask App (try port 5000, then 5001)
if check_port 5000 "Flask App"; then
    echo "🚀 Starting Flask App on port 5000..."
    cd /Users/wynnfarm/dev/landscaper && python app.py &
    sleep 2
    if lsof -i :5000 > /dev/null 2>&1; then
        echo "✅ Flask App started successfully on port 5000"
    else
        echo "❌ Failed to start Flask App on port 5000"
    fi
else
    echo "🔄 Trying alternative port 5001 for Flask App..."
    if check_port 5001 "Flask App (Alternative)"; then
        echo "🚀 Starting Flask App on port 5001..."
        cd /Users/wynnfarm/dev/landscaper && python -c "import app; app.app.run(host='0.0.0.0', port=5001, debug=True)" &
        sleep 2
        if lsof -i :5001 > /dev/null 2>&1; then
            echo "✅ Flask App started successfully on port 5001"
        else
            echo "❌ Failed to start Flask App on port 5001"
        fi
    else
        echo "❌ Both ports 5000 and 5001 are unavailable for Flask App"
    fi
fi

echo -e "\n📋 Final Port Status:"
check_port 5000 "Flask App"
check_port 5001 "Flask App (Alternative)"
check_port 8000 "Context Manager"
check_port 8001 "Persona Manager"
check_port 5433 "Database"

echo -e "\n🎉 Server startup complete!"
