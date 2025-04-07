#!/bin/bash

# Check if the device ID is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <new_device_id>"
    echo "If a device with this id already exists, it will just print the connection-string"
    exit 1
fi

# Resource Group and IoT Hub Details
RESOURCE_GROUP="package_theft"
IOT_HUB_NAME="package-theft-hub"
NEW_DEVICE_ID="$1"  # Get device ID from the first script argument
LOG_FILE="iot_device_creation.log"

# Logging function to handle both terminal and log file output
log() {
    echo "$1" | tee -a "$LOG_FILE"
}

# Add a timestamp with the current date and time
log "====================================="
log "Script executed at: $(date)"
log "====================================="

# Script Description
log "Creating IoT Device: $NEW_DEVICE_ID"
log "Resource Group: $RESOURCE_GROUP"
log "IoT Hub: $IOT_HUB_NAME"
log "====================================="

# Register a new device
log "Registering device..."
az iot hub device-identity create \
    --device-id "$NEW_DEVICE_ID" \
    --hub-name "$IOT_HUB_NAME" >> "$LOG_FILE" 2>&1

log "Fetching connection string..."
az iot hub device-identity connection-string show \
    --device-id "$NEW_DEVICE_ID" \
    --hub-name "$IOT_HUB_NAME" \
    --output table

log "====================================="
log "Device Registration Completed!"
log "====================================="

log "Use the following command to listen for events:"
log "az iot hub monitor-events --hub-name $IOT_HUB_NAME"

# Add extra newlines after script completion
log ""
log ""

