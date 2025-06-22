@echo off
echo === ZK-Roulette Git Fix and Push ===
cd /d "C:\Users\sserg\blockchain_roulette"

echo.
echo [DIAGNOSTIC] Current directory:
cd

echo.
echo [DIAGNOSTIC] Files in directory:
dir /b

echo.
echo [DIAGNOSTIC] Git status:
git status

echo.
echo [DIAGNOSTIC] Git ignored files:
git status --ignored

echo.
echo [1/8] Creating demo files if missing...
echo from fastapi import FastAPI > backend\demo_check.py
echo import uvicorn >> backend\demo_check.py
echo app = FastAPI() >> backend\demo_check.py

echo.
echo [2/8] Force adding ALL files including hidden...
git add . --force
git add backend\* --force
git add *.md --force

echo.
echo [3/8] Checking what will be committed:
git status

echo.
echo [4/8] Force commit with timestamp:
git commit -m "FORCE ADD: All DEMO files and documentation - %date% %time%"

echo.
echo [5/8] Checking if commit worked:
git log --oneline -n 3

echo.
echo [6/8] Pushing to GitHub:
git push origin master

echo.
echo [7/8] Final status check:
git status

echo.
echo [8/8] DONE! Check: https://github.com/Azarafel/zk-roulette
echo.
pause 