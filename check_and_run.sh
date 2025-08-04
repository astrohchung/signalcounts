#!/bin/bash

# Define the process to check
PROCESS_NAME="server.port 8533"
TARGET_DIR="/home4/astrohch/signalcounts"

# Check if the process is running
if ps aux | grep "$PROCESS_NAME" | grep -v "grep" > /dev/null; then
    echo "Streamlit instance is already running."
else
    echo "Streamlit instance is not running. Starting it now..."
    cd "$TARGET_DIR" || { echo "Failed to change directory to $TARGET_DIR. Exiting."; exit 1; }

    sh "$TARGET_DIR/startup.sh" &
fi
