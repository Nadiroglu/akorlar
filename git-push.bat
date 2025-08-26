@echo off
REM Git Auto-Push Script for Akorlar Project
REM This script automates the git workflow: add, commit, and push

setlocal enabledelayedexpansion

REM Set default values
set "COMMIT_MESSAGE=%~1"
if "%COMMIT_MESSAGE%"=="" set "COMMIT_MESSAGE=Update project files"
set "BRANCH=%~2"
if "%BRANCH%"=="" set "BRANCH=main"

echo 🚀 Starting Git Auto-Push Process...

REM Check if we're in a git repository
if not exist ".git" (
    echo ❌ Error: Not in a git repository!
    exit /b 1
)

REM Check git status
echo 📊 Checking git status...
git status --porcelain

REM Add all changes
echo ➕ Adding all changes...
git add -A

REM Check if there are changes to commit
git status --porcelain > temp_status.txt
set /p STATUS=<temp_status.txt
del temp_status.txt

if "%STATUS%"=="" (
    echo ✅ No changes to commit!
    exit /b 0
)

REM Commit changes
echo 💾 Committing changes with message: '%COMMIT_MESSAGE%'
git commit -m "%COMMIT_MESSAGE%"

if %ERRORLEVEL% EQU 0 (
    echo ✅ Commit successful!
) else (
    echo ❌ Commit failed!
    exit /b 1
)

REM Push to remote
echo 🚀 Pushing to origin/%BRANCH%...
git push origin %BRANCH%

if %ERRORLEVEL% EQU 0 (
    echo ✅ Push successful! All changes are now on GitHub.
) else (
    echo ❌ Push failed!
    exit /b 1
)

echo 🎉 Git Auto-Push completed successfully!
