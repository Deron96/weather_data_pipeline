#!/bin/bash

# Navigate to the project directory
cd /home/dlester1996/weather_pipeline

# Load environment variables (if needed)
# source .env  # Uncomment if you're relying on env vars for git behavior

# Stage all changes
git add .

# Commit with a timestamp
git commit -m "Auto-push: $(date '+%Y-%m-%d %H:%M:%S')"

# Push to GitHub
git push
