# Git Auto-Push Script for Akorlar Project
# This script automates the git workflow: add, commit, and push

param(
    [string]$CommitMessage = "Update project files",
    [string]$Branch = "main"
)

Write-Host "🚀 Starting Git Auto-Push Process..." -ForegroundColor Green

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "❌ Error: Not in a git repository!" -ForegroundColor Red
    exit 1
}

# Check git status
Write-Host "📊 Checking git status..." -ForegroundColor Yellow
git status --porcelain

# Add all changes
Write-Host "➕ Adding all changes..." -ForegroundColor Yellow
git add -A

# Check if there are changes to commit
$status = git status --porcelain
if ([string]::IsNullOrEmpty($status)) {
    Write-Host "✅ No changes to commit!" -ForegroundColor Green
    exit 0
}

# Commit changes
Write-Host "💾 Committing changes with message: '$CommitMessage'" -ForegroundColor Yellow
git commit -m $CommitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Commit successful!" -ForegroundColor Green
} else {
    Write-Host "❌ Commit failed!" -ForegroundColor Red
    exit 1
}

# Push to remote
Write-Host "🚀 Pushing to origin/$Branch..." -ForegroundColor Yellow
git push origin $Branch

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Push successful! All changes are now on GitHub." -ForegroundColor Green
} else {
    Write-Host "❌ Push failed!" -ForegroundColor Red
    exit 1
}

Write-Host "🎉 Git Auto-Push completed successfully!" -ForegroundColor Green
