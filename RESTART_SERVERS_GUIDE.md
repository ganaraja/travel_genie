# How to Restart Travel Genie Servers

## Why Restart?

When you make code changes to the backend (api_server.py, tools, agent, core), you need to restart the backend server for the changes to take effect. The server loads the code once at startup and doesn't automatically reload.

## Quick Restart Commands

### Option 1: Using Terminal (Recommended)

**Step 1: Stop any running servers**

```bash
# Find and kill any running Python processes
pkill -f "python.*api_server.py"
pkill -f "npm.*start"
```

**Step 2: Start Backend Server**

```bash
# In the project root directory
python api_server.py
```

This should show:

```
 * Running on http://127.0.0.1:5000
```

**Step 3: Start Frontend Server (in a new terminal)**

```bash
cd frontend
npm start
```

This should show:

```
Compiled successfully!
You can now view travel-genie-frontend in the browser.
Local: http://localhost:3000
```

### Option 2: Using Background Processes

If you started servers as background processes, you need to stop them first:

```bash
# List all background processes
ps aux | grep -E "(api_server|npm start)"

# Kill specific process by PID
kill <PID>

# Or kill all matching processes
pkill -f "python.*api_server.py"
pkill -f "npm.*start"
```

## Verification

### Check Backend is Running

```bash
curl http://localhost:5000/health
```

Should return: `{"status": "healthy"}`

### Check Frontend is Running

Open browser to: http://localhost:3000

### Test Destination Detection

Try these queries in the UI:

- "best time to visit zurich" → Should show Zurich, Switzerland
- "when to go to paris" → Should show Paris, France
- "best time for tokyo" → Should show Tokyo, Japan
- "bangalore weather" → Should show Bangalore, India

## Common Issues

### Issue: Backend shows old data

**Solution**: Make sure you restarted the backend server after code changes

### Issue: Frontend shows old UI

**Solution**:

1. Hard refresh browser: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
2. Clear browser cache
3. Restart frontend server

### Issue: Port already in use

**Solution**:

```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port
python api_server.py --port 5001
```

### Issue: Changes not reflecting

**Solution**:

1. Stop both servers
2. Clear Python cache: `find . -type d -name __pycache__ -exec rm -rf {} +`
3. Restart both servers
4. Hard refresh browser

## Development Workflow

For active development, use this workflow:

1. **Make code changes**
2. **Restart backend** (if backend changes)
3. **Hard refresh browser** (if frontend changes)
4. **Test the changes**
5. **Run tests**: `python -m pytest tests/backend/ -v`

## Automated Restart (Optional)

For development, you can use auto-reload tools:

### Backend Auto-reload

```bash
# Install watchdog
pip install watchdog

# Run with auto-reload
python api_server.py --reload
```

### Frontend Auto-reload

Frontend already has hot-reload enabled by default with `npm start`

## Current Status Check

Run this to check what's currently running:

```bash
echo "=== Backend Server ==="
curl -s http://localhost:5000/health 2>/dev/null && echo "✓ Backend is running" || echo "✗ Backend is not running"

echo ""
echo "=== Frontend Server ==="
curl -s http://localhost:3000 2>/dev/null > /dev/null && echo "✓ Frontend is running" || echo "✗ Frontend is not running"

echo ""
echo "=== Running Processes ==="
ps aux | grep -E "(api_server|npm start)" | grep -v grep
```
