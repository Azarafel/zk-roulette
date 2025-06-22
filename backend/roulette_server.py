from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="ZK-Roulette DEMO")

ROULETTE_HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title> ZK-Roulette DEMO</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; margin: 0; padding: 20px; min-height: 100vh; text-align: center; }
        h1 { font-size: 3em; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
        .wheel { width: 200px; height: 200px; border: 5px solid gold; border-radius: 50%; margin: 20px auto; background: conic-gradient(red 0deg 180deg, black 180deg 350deg, green 350deg 360deg); display: flex; align-items: center; justify-content: center; transition: transform 3s; }
        .center { width: 40px; height: 40px; background: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: black; font-weight: bold; }
        input { margin: 10px; padding: 15px; font-size: 16px; border: none; border-radius: 10px; text-align: center; }
        button { background: linear-gradient(45deg, #ff6b6b, #ee5a24); color: white; border: none; padding: 20px 40px; font-size: 18px; border-radius: 25px; cursor: pointer; margin: 10px; }
        button:hover { transform: translateY(-2px); }
        .result { margin: 20px 0; padding: 20px; background: rgba(0,0,0,0.3); border-radius: 10px; font-size: 20px; }
        .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 30px 0; }
        .stat { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; }
        .red { color: #ff4757; }
        .black { color: #2f3542; }
        .green { color: #2ed573; }
    </style>
</head>
<body>
    <h1> ZK-Roulette DEMO </h1>
    <div class="wheel" id="wheel"><div class="center" id="center"></div></div>
    <div>
        <input type="number" id="betNumber" placeholder="Число (0-36)" min="0" max="36">
        <input type="number" id="betAmount" placeholder="Ставка" min="1" value="10">
        <br><button onclick="spin()"> КРУТИТЬ РУЛЕТКУ</button>
    </div>
    <div class="result" id="result">Сделайте ставку!</div>
    <div class="stats">
        <div class="stat"> Игр: <div id="games">0</div></div>
        <div class="stat"> Выигрыши: <div id="wins">0</div></div>
        <div class="stat"> Баланс: <div id="balance">1000</div></div>
        <div class="stat"> Последнее: <div id="last">-</div></div>
    </div>
    <script>
        let balance=1000,games=0,wins=0,spinning=false;
        function update(){document.getElementById('games').textContent=games;document.getElementById('wins').textContent=wins;document.getElementById('balance').textContent=balance;}
        function color(n){if(n===0)return 'green';return[1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36].includes(n)?'red':'black';}
        function spin(){if(spinning)return;const num=parseInt(document.getElementById('betNumber').value);const amt=parseInt(document.getElementById('betAmount').value);if(isNaN(num)||num<0||num>36){alert('Число 0-36!');return;}if(isNaN(amt)||amt<=0||amt>balance){alert('Неверная ставка!');return;}spinning=true;balance-=amt;const wheel=document.getElementById('wheel');wheel.style.transform='rotate('+(1440+Math.random()*1440)+'deg)';const win=Math.floor(Math.random()*37);document.getElementById('result').innerHTML=' Крутится...';setTimeout(()=>{games++;const c=color(win);document.getElementById('center').textContent=win;document.getElementById('last').innerHTML='<span class="'+c+'">'+win+'</span>';if(win===num){const prize=amt*35;balance+=prize;wins++;document.getElementById('result').innerHTML=' ВЫИГРЫШ! Число: <span class="'+c+'">'+win+'</span>, Приз: '+prize;}else{document.getElementById('result').innerHTML=' Выпало: <span class="'+c+'">'+win+'</span>. Еще раз!';}update();spinning=false;setTimeout(()=>{wheel.style.transition='none';wheel.style.transform='rotate(0deg)';setTimeout(()=>wheel.style.transition='transform 3s',100)},1000)},3000);}
        update();
    </script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
async def get_roulette():
    return HTMLResponse(content=ROULETTE_HTML, status_code=200)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "demo": True}

if __name__ == "__main__":
    print(" Запуск ZK-Roulette DEMO...")
    print(" http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
