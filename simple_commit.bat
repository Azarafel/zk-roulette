@echo off
echo Starting Git sync to GitHub...
cd /d C:\Users\sserg\blockchain_roulette

echo Step 1: Initialize Git
git init

echo Step 2: Add remote origin
git remote remove origin 2>nul
git remote add origin https://github.com/Azarafel/zk-roulette.git

echo Step 3: Pull latest changes
git pull origin master

echo Step 4: Add all files
git add .

echo Step 5: Commit changes
git commit -m "Add DEMO roulette server and updated documentation"

echo Step 6: Push to GitHub
git push origin master

echo Done! Check GitHub: https://github.com/Azarafel/zk-roulette
pause 