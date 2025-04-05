#!/bin/bash

# Navigate to the Flask app directory
cd /home/ec2-user/flask-app

# Pull the latest changes from GitHub (main branch)
echo "Pulling the latest code from GitHub..."
git pull origin main

# Restart Gunicorn to apply changes
echo "Restarting Gunicorn..."
sudo systemctl restart gunicorn

echo "Deployment completed successfully!"
