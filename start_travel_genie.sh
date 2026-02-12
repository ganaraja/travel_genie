#!/bin/bash

# Travel Genie Startup Script
# This script starts both the API server and the frontend

echo "🌴 Starting Travel Genie..."
echo ""

# Check if Python virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run: uv venv"
    exit 1
fi

# Check if node_modules exists in frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
uv pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed"
echo ""

# Start API server in background
echo "🚀 Starting API server on port 5000..."
uv run python api_server.py &
API_PID=$!

# Wait for API to be ready
echo "⏳ Waiting for API server to start..."
sleep 3

# Start frontend
echo "🚀 Starting frontend on port 3000..."
cd frontend && npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Travel Genie is running!"
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping Travel Genie...'; kill $API_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Keep script running
wait
