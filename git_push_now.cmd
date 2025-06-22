@echo off
echo === ZK-Roulette Git Push ===
cd /d "C:\Users\sserg\blockchain_roulette"

echo [1/7] Initializing Git...
git init

echo [2/7] Adding remote origin...
git remote remove origin 2>nul
git remote add origin https://github.com/Azarafel/zk-roulette.git

echo [3/7] Checking remote...
git remote -v

echo [4/7] Pulling latest changes...
git pull origin master --allow-unrelated-histories

echo [5/7] Adding all files...
git add .

echo [6/7] Committing changes...
git commit -m "Add DEMO roulette server with FastAPI and updated docs"

echo [7/7] Pushing to GitHub...
git push origin master

echo === SUCCESS! Check: https://github.com/Azarafel/zk-roulette ===
pause 