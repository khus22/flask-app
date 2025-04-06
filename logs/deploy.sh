#!/bin/bash

# Log file path
LOG_FILE="/home/ec2-user/flask-app/logs/deploy.log"

# Start logging
{
    echo "------ DEPLOYMENT STARTED AT $(date) ------"

    # Navigate to the Flask app directory
    cd /home/ec2-user/flask-app || { echo "ERROR: Cannot access project directory"; exit 1; }

    # Pull the latest changes from GitHub (main branch)
    echo "Pulling the latest code from GitHub..."
    git pull origin main

    # Restart Gunicorn to apply changes
    echo "Restarting Gunicorn..."
    sudo systemctl restart gunicorn

    # Check Gunicorn status
    echo "Gunicorn status:"
    sudo systemctl status gunicorn --no-pager

    echo "Deployment completed successfully!"
    echo "------ DEPLOYMENT FINISHED AT $(date) ------"
    echo ""
} >> "$LOG_FILE" 2>&1
