#!/bin/bash
# Stop any running mlx_lm.server instances

echo "Stopping MLX server instances..."

# Find and kill all mlx_lm.server processes
if pgrep -f "mlx_lm.server" > /dev/null; then
    pkill -f "mlx_lm.server"
    echo "✓ Stopped running server(s)"
    sleep 1

    # Verify they're stopped
    if pgrep -f "mlx_lm.server" > /dev/null; then
        echo "⚠ Some processes still running, forcing..."
        pkill -9 -f "mlx_lm.server"
        sleep 1
    fi
else
    echo "ℹ No running servers found"
fi

# Check ports
echo ""
echo "Port status:"
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "  Port 8000: IN USE (PID: $(lsof -Pi :8000 -sTCP:LISTEN -t))"
else
    echo "  Port 8000: Available"
fi

if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "  Port 8080: IN USE (PID: $(lsof -Pi :8080 -sTCP:LISTEN -t))"
else
    echo "  Port 8080: Available"
fi

echo ""
echo "Done!"
