#!/bin/bash
# Launch Galaga in the background
cd "$(dirname "$0")"
python galaga.py &
echo "Galaga launched! PID: $!"
echo "The game is now running in a separate window."