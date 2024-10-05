#!/bin/bash

# Define the container name or ID
CONTAINER_NAME="9a5feda7135b"

# Define the check interval (in seconds)
CHECK_INTERVAL=10

# Loop to keep checking the container status
while true; do
    # Check if the container is running
    STATUS=$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME)

    if [ "$STATUS" == "false" ]; then
        echo "Container $CONTAINER_NAME has stopped. Restarting..."
        docker restart $CONTAINER_NAME
    else
        echo "Container $CONTAINER_NAME is running."
    fi

    # Sleep for a while before checking again
    sleep $CHECK_INTERVAL
done

