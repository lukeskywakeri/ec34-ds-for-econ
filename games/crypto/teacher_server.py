import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import time
import socket
from datetime import datetime

# --- CONFIGURATION ---
GOAL_AMOUNT = 100_000_000  # $100 Million Target
PORT = 8000

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- STATE ---
state = {
    "money_stolen": 0,
    "logs": [],
    "start_time": time.time(),
}

# --- 90s HACKER DASHBOARD ---
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>OPERATION: BLACK ICE</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

        body { 
            background-color: #000000; 
            color: #00ff00; 
            font-family: 'VT323', monospace; 
            padding: 2rem; 
            overflow: hidden; 
            text-shadow: 0 0 5px #003300;
        }
        
        .container { max-width: 900px; margin: 0 auto; position: relative; z-index: 10; }
        
        h1 { 
            text-align: center; 
            font-size: 4rem; 
            margin-bottom: 0;
            border-bottom: 2px solid #00ff00;
            line-height: 1;
        }
        
        .subtitle { text-align: center; margin-bottom: 2rem; color: #008800; font-size: 1.5rem; }

        .progress-container {
            width: 100%;
            background-color: #111;
            border: 2px solid #00ff00;
            height: 60px;
            margin: 2rem 0;
            position: relative;
        }
        
        .progress-bar {
            height: 100%;
            background: repeating-linear-gradient(
                45deg,
                #003300,
                #003300 10px,
                #00ff00 10px,
                #00ff00 20px
            );
            width: 0%;
            transition: width 0.5s ease-out;
            box-shadow: 0 0 20px #00ff00;
        }

        .stats { 
            display: flex; 
            justify-content: space-between; 
            font-size: 2rem; 
            margin-bottom: 0.5rem; 
        }

        .log-box {
            background-color: #050505;
            border: 1px dashed #00ff00;
            height: 350px;
            overflow-y: hidden; /* Auto-scroll handled by JS */
            padding: 1rem;
            font-size: 1.2rem;
            font-family: 'Courier New', monospace;
        }
        
        .log-entry { margin-bottom: 5px; }
        .success { color: #ccffcc; }
        .timestamp { color: #008800; margin-right: 15px; }
        
        /* MATRIX ANIMATION */
        canvas {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            z-index: 1;
        }
        
        .win-message {
            display: none;
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            font-size: 6rem;
            color: #000;
            background-color: #00ff00;
            z-index: 20;
            padding: 2rem 4rem;
            border: 5px solid #fff;
            text-align: center;
            box-shadow: 0 0 50px #00ff00;
            font-weight: bold;
        }
        
        .blink { animation: blinker 1s linear infinite; }
        @keyframes blinker { 50% { opacity: 0; } }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    
    <div id="win-msg" class="win-message">
        ACCESS GRANTED<br>
        <span style="font-size: 2rem; color: #000;">TRANSFER COMPLETE: $""" + "{:,}".format(GOAL_AMOUNT) + """</span>
    </div>

    <div class="container" id="main-ui">
        <h1>TARGET: CORPO_BANK_MAINFRAME</h1>
        <div class="subtitle">/// OPERATION: BLACK ICE /// CONNECTION SECURE</div>
        
        <div class="stats">
            <span id="money-display">$0</span>
            <span id="status" class="blink">INJECTING PAYLOADS...</span>
        </div>

        <div class="progress-container">
            <div id="bar" class="progress-bar"></div>
        </div>

        <h3>>> SYSTEM_LOGS</h3>
        <div id="logs" class="log-box"></div>
    </div>

    <script>
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        let hacked = false;
        const goalAmount = """ + str(GOAL_AMOUNT) + """;

        // Matrix Rain Logic
        function startMatrix() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            canvas.style.display = 'block';
            
            const chars = '01XYZ$#@&%';
            const fontSize = 16;
            const columns = canvas.width / fontSize;
            const rainDrops = Array.from({ length: columns }).fill(1);

            const draw = () => {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#0F0';
                ctx.font = fontSize + 'px monospace';

                for (let i = 0; i < rainDrops.length; i++) {
                    const text = chars.charAt(Math.floor(Math.random() * chars.length));
                    ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);
                    
                    if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                        rainDrops[i] = 0;
                    }
                    rainDrops[i]++;
                }
            };
            setInterval(draw, 30);
        }

        async function updateDashboard() {
            try {
                const response = await fetch('/stats');
                const data = await response.json();
                
                // Update Money Text
                document.getElementById('money-display').innerText = 
                    '$' + data.money_stolen.toLocaleString('en-US');

                // Check Win
                if (!hacked && data.money_stolen >= goalAmount) {
                    hacked = true;
                    document.getElementById('win-msg').style.display = 'block';
                    document.getElementById('status').innerText = 'SYSTEM COMPROMISED';
                    document.getElementById('status').style.color = '#fff';
                    startMatrix();
                }

                if (!hacked) {
                    const pct = Math.min(100, (data.money_stolen / goalAmount) * 100);
                    document.getElementById('bar').style.width = pct + '%';
                }
                
                // Logs (Newest at top)
                const logDiv = document.getElementById('logs');
                logDiv.innerHTML = data.logs.map(l => 
                    `<div class="log-entry"><span class="timestamp">[${l.time}]</span> <span class="success">>> ${l.msg}</span></div>`
                ).join('');
                
            } catch (e) { console.error(e); }
        }
        
        setInterval(updateDashboard, 1000);
        updateDashboard();
    </script>
</body>
</html>
"""

class HackAttempt(BaseModel):
    hacker_alias: str
    problem_id: int
    answer: float

# --- QUESTIONS (Python & Numpy Basics) ---
PROBLEMS = [
    # PYTHON BASICS
    {"id": 1, "q": "DECRYPT: 2 to the power of 8", "a": 256},
    {"id": 2, "q": "SLICE: Sum of last 2 items in [10, 20, 30, 40, 50]", "a": 90},
    {"id": 3, "q": "KEYGEN: Value of key 'b' in {'a': 10, 'b': 20}", "a": 20},
    {"id": 4, "q": "LOOP: Sum of squares of [1, 2, 3]", "a": 14},
    {"id": 5, "q": "STRING: Length of 'Data' * 5", "a": 20},
    
    # NUMPY MATRIX MATH
    {"id": 6, "q": "MATRIX: Mean of np.array([10, 20, 30, 40])", "a": 25},
    {"id": 7, "q": "VECTOR: Dot Product of [1, 2] and [3, 4]", "a": 11},
    {"id": 8, "q": "BROADCAST: Sum of np.array([1, 2]) + 10", "a": 23},
    {"id": 9, "q": "ARGMAX: Index of max value in [1, 5, 2, 4]", "a": 1},
    {"id": 10, "q": "SHAPE: Columns in array reshaped to (2, 5)", "a": 5},

    # --- NEW DIFFICULT QUESTIONS ---
    {"id": 11, "q": "FILTER: Sum of numbers divisible by 3 in range(1, 20)", "a": 63}, # 3+6+9+12+15+18 = 63
    {"id": 12, "q": "MASK: Sum of all items > 5 in np.array([2, 8, 1, 10, 5, 7])", "a": 25}, # 8+10+7 = 25
    {"id": 13, "q": "2D-SLICE: Sum of the last row of np.arange(9).reshape(3,3)", "a": 21}, # 6+7+8 = 21
]

@app.get("/")
async def dashboard():
    return HTMLResponse(content=html_template)

@app.get("/stats")
async def get_stats():
    return {"money_stolen": state["money_stolen"], "logs": state["logs"][:12]}

@app.get("/get_target")
async def get_target():
    prob = random.choice(PROBLEMS)
    return {"problem_id": prob["id"], "question": prob["q"]}

@app.post("/inject")
async def inject_payload(attempt: HackAttempt):
    if state["money_stolen"] >= GOAL_AMOUNT:
        return {"status": "done", "message": "Mainframe already drained."}

    problem = next((p for p in PROBLEMS if p["id"] == attempt.problem_id), None)
    
    if not problem:
        raise HTTPException(status_code=400, detail="Invalid Target ID")

    if abs(attempt.answer - problem["a"]) < 0.1:
        # Dynamic reward between $50k and $150k
        steal_amount = random.randint(50000, 150000)
        state["money_stolen"] += steal_amount
        
        log_msg = f"USER '{attempt.hacker_alias}' BYPASSED FIREWALL {problem['id']}: TRANSFERRED ${steal_amount:,}"
        print(log_msg)
        state["logs"].insert(0, {"time": datetime.now().strftime("%H:%M:%S"), "msg": log_msg})
        
        return {"status": "accepted", "message": f"Access Granted. ${steal_amount:,} transferred."}
    else:
        return JSONResponse(status_code=418, content={"status": "rejected", "message": "Access Denied. Incorrect Key."})

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    ip = get_lan_ip()
    print("\n" + "="*60)
    print(f" 💀 HACKER C&C SERVER RUNNING")
    print(f" 📡 TARGET URL: http://{ip}:{PORT}")
    print(f" 💰 TARGET LOOT: ${GOAL_AMOUNT:,}")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=PORT)