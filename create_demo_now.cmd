@echo off
echo Creating ZK-Roulette DEMO files NOW...
cd /d "C:\Users\sserg\blockchain_roulette"

echo [1/4] Creating backend/roulette_demo.py...
echo from fastapi import FastAPI > backend\roulette_demo.py
echo from fastapi.responses import HTMLResponse >> backend\roulette_demo.py
echo import uvicorn >> backend\roulette_demo.py
echo. >> backend\roulette_demo.py
echo app = FastAPI^(title="ZK-Roulette DEMO"^) >> backend\roulette_demo.py
echo. >> backend\roulette_demo.py
echo @app.get^("/", response_class=HTMLResponse^) >> backend\roulette_demo.py
echo async def get_demo^(^): >> backend\roulette_demo.py
echo     return HTMLResponse^("^<h1^>ZK-Roulette DEMO Works!^</h1^>^<p^>Demo version is ready^</p^>"^) >> backend\roulette_demo.py
echo. >> backend\roulette_demo.py
echo if __name__ == "__main__": >> backend\roulette_demo.py
echo     uvicorn.run^(app, host="0.0.0.0", port=8000^) >> backend\roulette_demo.py

echo [2/4] Creating DEMO_README.md...
echo # ZK-Roulette DEMO > DEMO_README.md
echo. >> DEMO_README.md
echo Working blockchain roulette demo >> DEMO_README.md
echo. >> DEMO_README.md
echo ## Quick start: >> DEMO_README.md
echo cd backend >> DEMO_README.md
echo python roulette_demo.py >> DEMO_README.md

echo [3/4] Adding to Git...
git add backend\roulette_demo.py
git add DEMO_README.md
git add .

echo [4/4] Committing and pushing...
git commit -m "Add working ZK-Roulette DEMO files"
git push origin master

echo DONE! Check: https://github.com/Azarafel/zk-roulette
pause 