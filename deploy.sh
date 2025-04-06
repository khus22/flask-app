#!/bin/bash
set -e

LOG_FILE="/home/ec2-user/flask-app/deploy.log"
exec >> "$LOG_FILE" 2>&1
echo "----- Deployment started at $(date) -----"

cd /home/ec2-user/flask-app || { echo "❌ Failed to cd into project directory"; exit 1; }

echo "✅ Pulling the latest code from GitHub..."
git pull origin main || { echo "❌ Git pull failed"; exit 1; }

echo "🔁 Restarting Gunicorn service..."
sudo systemctl restart gunicorn || { echo "❌ Failed to restart Gunicorn"; exit 1; }

echo "✅ Deployment completed at $(date)"
echo "------------------------------------------"

