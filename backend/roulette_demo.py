from fastapi import FastAPI 
from fastapi.responses import HTMLResponse 
import uvicorn 
 
app = FastAPI(title="ZK-Roulette DEMO") 
 
@app.get("/", response_class=HTMLResponse) 
async def get_demo(): 
    return HTMLResponse("^<h1^>ZK-Roulette DEMO Works!^</h1^>^<p^>Demo version is ready^</p^>") 
 
if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8000) 
