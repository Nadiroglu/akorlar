#!/bin/bash

# Git Auto-Push Script for Akorlar Project
# This script automates the git workflow: add, commit, and push

# Set default values
COMMIT_MESSAGE=${1:-"Update project files"}
BRANCH=${2:-"main"}

echo "🚀 Starting Git Auto-Push Process..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository!"
    exit 1
fi

# Check git status
echo "📊 Checking git status..."
git status --porcelain

# Add all changes
echo "➕ Adding all changes..."
git add -A

# Check if there are changes to commit
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ No changes to commit!"
    exit 0
fi

# Commit changes
echo "💾 Committing changes with message: '$COMMIT_MESSAGE'"
git commit -m "$COMMIT_MESSAGE"

if [ $? -eq 0 ]; then
    echo "✅ Commit successful!"
else
    echo "❌ Commit failed!"
    exit 1
fi

# Push to remote
echo "🚀 Pushing to origin/$BRANCH..."
git push origin "$BRANCH"

if [ $? -eq 0 ]; then
    echo "✅ Push successful! All changes are now on GitHub."
else
    echo "❌ Push failed!"
    exit 1
fi

echo "🎉 Git Auto-Push completed successfully!"
