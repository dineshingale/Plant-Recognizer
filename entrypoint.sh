#!/bin/bash
set -e

echo "🚀 [entrypoint.sh] Starting Pipeline Environment..."

# 1. Start React App (Vite) in Background
# We MUST use --host to expose it to the container network, 
# and --port 3000 to match the test expectations.
echo "🔄 Starting Vite Server on 0.0.0.0:3000..."
cd Client
# 'nohup' prevents the process from being tied to the shell, ensuring it runs
nohup npm run dev -- --host --port 3000 > ../frontend_logs.txt 2>&1 &
FRONTEND_PID=$!
cd ..

# 2. Wait for Port 3000 to be Ready
echo "⏳ Waiting for frontend to launch on localhost:3000..."
START_TIME=$(date +%s)
TIMEOUT=120 # 2 minutes timeout

while ! nc -z localhost 3000; do
  CURRENT_TIME=$(date +%s)
  ELAPSED=$((CURRENT_TIME - START_TIME))
  
  if [ $ELAPSED -ge $TIMEOUT ]; then
    echo "❌ Timeout waiting for Frontend!"
    cat frontend_logs.txt
    kill $FRONTEND_PID
    exit 1
  fi
  sleep 2
done

echo "✅ Frontend is UP! (PID: $FRONTEND_PID)"

# 3. Run Selenium Tests
echo "🧪 Running Selenium E2E Tests..."
export BASE_URL="http://localhost:3000"

# Running pytests
# Write to /tmp first to avoid permission crashes on mounted volumes
echo "Running pytest..."
python -m pytest tests/test_app.py -v --junitxml=/tmp/test-results.xml
TEST_EXIT_CODE=$?

# Attempt to save results back to host (Safe Move)
echo "Attempting to save test results..."
cp /tmp/test-results.xml ./test-results.xml || echo "⚠️ Warning: Could not save test-results.xml to host (Permission Issue). Build will proceed."

# 4. Cleanup & Exit
echo "🛑 Stopping Frontend..."
kill $FRONTEND_PID

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "🎉 Tests Passed!"
    exit 0
else
    echo "❌ Tests Failed! (Exit Code: $TEST_EXIT_CODE)"
    exit $TEST_EXIT_CODE
fi
