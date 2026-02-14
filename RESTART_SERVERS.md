# How to Restart Travel Genie Servers

If you're seeing incorrect destination names (e.g., "Maui" when asking about "Bangalore"), you need to restart the servers to load the updated code.

## Quick Restart (Recommended)

### 1. Stop All Running Servers

```bash
# Find and kill any running Python/Node processes
pkill -f "python.*api_server"
pkill -f "npm.*start"
pkill -f "react-scripts"

# Or use Ctrl+C in each terminal window
```

### 2. Restart API Server

```bash
# In Terminal 1
python api_server.py
```

**Expected output:**

```
Starting Travel Genie API server on port 5000...
Frontend should connect to: http://localhost:5000
 * Running on http://0.0.0.0:5000
```

### 3. Restart Frontend

```bash
# In Terminal 2
cd frontend
npm start
```

**Expected output:**

```
Compiled successfully!

You can now view travel-genie-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

### 4. Clear Browser Cache

1. Open browser DevTools (F12 or Cmd+Option+I)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

OR

1. Open http://localhost:3000
2. Press Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows/Linux)

## Verify It's Working

### Test Backend Directly

```bash
python -c "from api_server import get_travel_recommendation; \
result = get_travel_recommendation('When should I visit Bangalore?', 'default'); \
print('Bangalore count:', result.count('Bangalore')); \
print('Maui count:', result.count('Maui'))"
```

**Expected output:**

```
Bangalore count: 6
Maui count: 0
```

### Test Frontend

1. Open http://localhost:3000
2. Click "When should I visit Bangalore?" example query
3. Verify the response shows:
   - "Bangalore" in weather section
   - "Bangalore" in hotel names (e.g., "Marriott Bangalore")
   - No mentions of "Maui"

## Troubleshooting

### Issue: API Server Shows Old Code

**Solution:**

```bash
# Kill all Python processes
pkill -f python

# Restart API server
python api_server.py
```

### Issue: Frontend Shows Cached Data

**Solution:**

```bash
# Stop frontend
pkill -f "npm.*start"

# Clear npm cache
cd frontend
rm -rf node_modules/.cache

# Restart
npm start
```

### Issue: Port Already in Use

**For API Server (Port 5000):**

```bash
# Find process using port 5000
lsof -ti:5000

# Kill it
kill -9 $(lsof -ti:5000)

# Restart
python api_server.py
```

**For Frontend (Port 3000):**

```bash
# Find process using port 3000
lsof -ti:3000

# Kill it
kill -9 $(lsof -ti:3000)

# Restart
cd frontend && npm start
```

### Issue: Changes Not Reflecting

1. **Check you're editing the right files:**

   ```bash
   # Verify api_server.py has the new destinations
   grep -A 5 "bangalore" api_server.py
   ```

2. **Verify Python is using the right file:**

   ```bash
   python -c "import api_server; print(api_server.__file__)"
   ```

3. **Check for syntax errors:**
   ```bash
   python -m py_compile api_server.py
   ```

## Complete Restart Script

Save this as `restart_all.sh`:

```bash
#!/bin/bash

echo "🛑 Stopping all servers..."
pkill -f "python.*api_server"
pkill -f "npm.*start"
pkill -f "react-scripts"

sleep 2

echo "🚀 Starting API server..."
python api_server.py &
API_PID=$!

sleep 3

echo "🚀 Starting frontend..."
cd frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ Servers started!"
echo "   API Server PID: $API_PID"
echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "📍 URLs:"
echo "   API: http://localhost:5000"
echo "   Frontend: http://localhost:3000"
echo ""
echo "To stop servers:"
echo "   kill $API_PID $FRONTEND_PID"
```

Make it executable:

```bash
chmod +x restart_all.sh
./restart_all.sh
```

## Testing After Restart

### Test Multiple Destinations

```bash
# Test Bangalore
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "When should I visit Bangalore?", "userId": "default"}' \
  | grep -o "Bangalore" | wc -l

# Should output: 6 or more

# Test Mumbai
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "When should I visit Mumbai?", "userId": "default"}' \
  | grep -o "Mumbai" | wc -l

# Should output: 6 or more
```

### Run Automated Tests

```bash
# Test all destinations
python test_destination_output.py

# Should show: "✅ All tests passed!"
```

## Common Mistakes

1. ❌ **Not restarting after code changes**
   - Always restart both API server and frontend

2. ❌ **Browser cache not cleared**
   - Use hard reload (Cmd+Shift+R)

3. ❌ **Wrong terminal/directory**
   - API server: run from project root
   - Frontend: run from `frontend/` directory

4. ❌ **Multiple instances running**
   - Check with `ps aux | grep python` and `ps aux | grep node`
   - Kill all instances before restarting

## Verification Checklist

After restarting, verify:

- [ ] API server running on port 5000
- [ ] Frontend running on port 3000
- [ ] Backend test shows correct destination count
- [ ] Frontend shows correct destination in responses
- [ ] No "Maui" appears when asking about other cities
- [ ] Weather section shows correct city name
- [ ] Hotel names include correct city name

## Need Help?

If issues persist:

1. Check logs in terminal windows
2. Run `python test_destination_output.py`
3. Check browser console (F12) for errors
4. Verify API endpoint: http://localhost:5000/api/health
