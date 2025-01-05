#!/bin/bash

# Script: /usr/local/bin/update-server.sh
# Purpose: Update and upgrade the system, logging output to /tmp/update-server.log

LOG_FILE="/tmp/update-server.log"

# Perform update and upgrade
{
    echo "==== Update and Upgrade Started: $(date) ===="
    sudo apt update && sudo apt upgrade -y
    echo "==== Update and Upgrade Completed: $(date) ===="
} &> "$LOG_FILE"