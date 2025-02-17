@echo off
chcp 65001
echo ====== Start uploading to GitHub ======

:: Add all files
echo 1. Adding files to staging area...
git add .

:: Get commit message
set /p commit_msg=Enter commit message (default is "Update code"): 
if "%commit_msg%"=="" set commit_msg=Update code

:: Create commit
echo 2. Creating commit...
git commit -m "%commit_msg%"

:: Push to GitHub
echo 3. Pushing to GitHub...
git push origin main

echo ====== Completed ======
pause 