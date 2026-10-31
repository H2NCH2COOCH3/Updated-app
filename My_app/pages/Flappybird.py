
import json
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Flappy Bird",
    page_icon="🐤",
    layout="centered"
)

st.title("🐤 Flappy Bird: Skin Edition")
st.write("Choose your bird, then play!")

# =========================
# BIRD SKINS
# =========================

SKINS = {
    "🐤 Classic": {
        "body": "#FFD43B",
        "wing": "#FFAD24",
        "beak": "#FF7043",
        "eye": "#263746",
        "special": "classic"
    },
    "🔵 Blue Bird": {
        "body": "#42A5F5",
        "wing": "#1976D2",
        "beak": "#FFB74D",
        "eye": "#102A43",
        "special": "classic"
    },
    "🔥 Fire Bird": {
        "body": "#FF5722",
        "wing": "#FF9800",
        "beak": "#FFEB3B",
        "eye": "#351008",
        "special": "fire"
    },
    "💜 Purple Bird": {
        "body": "#AB47BC",
        "wing": "#7B1FA2",
        "beak": "#FFD54F",
        "eye": "#211027",
        "special": "classic"
    },
    "💚 Slime Bird": {
        "body": "#76FF03",
        "wing": "#4CAF50",
        "beak": "#FF9800",
        "eye": "#17330A",
        "special": "slime"
    },
    "🥷 Ninja Bird": {
        "body": "#30343B",
        "wing": "#111318",
        "beak": "#FF5252",
        "eye": "#FFFFFF",
        "special": "ninja"
    },
    "🤖 Robot Bird": {
        "body": "#B0BEC5",
        "wing": "#607D8B",
        "beak": "#FF9800",
        "eye": "#00E5FF",
        "special": "robot"
    },
    "🌈 Rainbow Bird": {
        "body": "#FF4DA6",
        "wing": "#7C4DFF",
        "beak": "#FFEB3B",
        "eye": "#263746",
        "special": "rainbow"
    },
}

selected_skin = st.selectbox(
    "🎨 Choose your bird skin",
    list(SKINS.keys())
)

selected_colors = SKINS[selected_skin]

# Optional difficulty setting
difficulty = st.select_slider(
    "⚡ Difficulty",
    options=["Easy", "Normal", "Hard"],
    value="Normal"
)

difficulty_settings = {
    "Easy": {"speed": 2.2, "gap": 195, "gravity": 0.28, "jump": -6.2},
    "Normal": {"speed": 2.7, "gap": 168, "gravity": 0.34, "jump": -6.5},
    "Hard": {"speed": 3.4, "gap": 145, "gravity": 0.40, "jump": -7.0},
}

settings = difficulty_settings[difficulty]

st.caption(
    f"Selected: {selected_skin} | Difficulty: {difficulty}"
)

# =========================
# GAME HTML
# =========================

GAME_HTML = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: transparent;
}

.wrap {
    width: 100%;
    max-width: 520px;
    margin: auto;
}

.hud {
    display: flex;
    justify-content: space-between;
    gap: 5px;
    padding: 12px 8px;
    margin-bottom: 8px;
    background: #eaf7ff;
    border-radius: 12px;
    font-weight: bold;
    color: #17324d;
    font-size: 14px;
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    border: 3px solid #29465b;
    border-radius: 12px;
    background: #87d8f5;
    touch-action: manipulation;
    cursor: pointer;
}

.buttons {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 10px;
}

button {
    padding: 12px 16px;
    border: none;
    border-radius: 10px;
    background: #ffcc4d;
    color: #263746;
    font-weight: bold;
    font-size: 15px;
    cursor: pointer;
}

button:hover {
    background: #ffb92e;
}

.hint {
    text-align: center;
    color: #526b7a;
    font-size: 13px;
    margin-top: 8px;
}
</style>
</head>

<body>
<div class="wrap">

    <div class="hud">
        <span>⭐ <span id="score">0</span></span>
        <span>🏆 Best: <span id="best">0</span></span>
        <span id="status">Ready!</span>
    </div>

    <canvas id="game" width="480" height="640"></canvas>

    <div class="buttons">
        <button id="restart">▶ Restart</button>
        <button id="flap">🐤 FLAP!</button>
    </div>

    <div class="hint">
        SPACE / ↑ / click / tap to fly
    </div>
</div>

<script>
const SKIN = __SKIN_JSON__;
const SETTINGS = __SETTINGS_JSON__;

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;
const GROUND = 58;

let bird, pipes;
let score = 0;
let best = 0;
let running = false;
let started = false;
let groundOffset = 0;
let animationId = null;
let frame = 0;

const GRAVITY = SETTINGS.gravity;
const JUMP = SETTINGS.jump;
const PIPE_WIDTH = 76;
const PIPE_GAP = SETTINGS.gap;
const PIPE_SPEED = SETTINGS.speed;

function reset() {
    if (animationId !== null) {
        cancelAnimationFrame(animationId);
    }

    animationId = null;
    bird = {
        x: 115,
        y: 280,
        vy: 0,
        radius: 16
    };

    pipes = [];
    score = 0;
    groundOffset = 0;
    frame = 0;
    running = false;
    started = false;

    document.getElementById("score").textContent = "0";
    document.getElementById("status").textContent = "Ready!";

    addPipe(W + 30);
    draw();
}

function addPipe(x) {
    const min = 115;
    const max = H - GROUND - 115;

    pipes.push({
        x: x,
        center: min + Math.random() * (max - min),
        passed: false
    });
}

function drawBackground() {
    const gradient = ctx.createLinearGradient(0, 0, 0, H);
    gradient.addColorStop(0, "#70d4f4");
    gradient.addColorStop(1, "#e1f9ff");

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, W, H);

    // Clouds
    ctx.fillStyle = "rgba(255,255,255,0.8)";

    const cloudOffset = (frame * 0.15) % 560;

    for (const c of [
        {x: 70 - cloudOffset, y: 105},
        {x: 310 - cloudOffset, y: 160},
        {x: 520 - cloudOffset, y: 80}
    ]) {
        ctx.beginPath();
        ctx.arc(c.x, c.y, 18, 0, Math.PI * 2);
        ctx.arc(c.x + 22, c.y - 8, 23, 0, Math.PI * 2);
        ctx.arc(c.x + 44, c.y, 17, 0, Math.PI * 2);
        ctx.fill();
    }

    // Hills
    ctx.fillStyle = "#a8e6a0";
    ctx.beginPath();
    ctx.moveTo(0, 500);

    for (let x = 0; x <= W; x += 20) {
        ctx.lineTo(x, 485 + Math.sin(x / 45) * 15);
    }

    ctx.lineTo(W, H);
    ctx.lineTo(0, H);
    ctx.fill();
}

function drawPipe(pipe) {
    const topHeight = pipe.center - PIPE_GAP / 2;
    const bottomY = pipe.center + PIPE_GAP / 2;
    const bottomHeight = H - GROUND - bottomY;

    const green = "#38b84a";
    const dark = "#21833a";
    const light = "#75e56c";

    // Upper pipe
    ctx.fillStyle = green;
    ctx.fillRect(pipe.x, 0, PIPE_WIDTH, topHeight);

    ctx.fillStyle = light;
    ctx.fillRect(pipe.x + 8, 0, 10, topHeight);

    ctx.fillStyle = dark;
    ctx.fillRect(pipe.x + PIPE_WIDTH - 9, 0, 9, topHeight);

    ctx.fillStyle = green;
    ctx.fillRect(pipe.x - 6, topHeight - 25, PIPE_WIDTH + 12, 25);

    ctx.strokeStyle = dark;
    ctx.lineWidth = 3;
    ctx.strokeRect(pipe.x - 6, topHeight - 25, PIPE_WIDTH + 12, 25);

    // Lower pipe
    ctx.fillStyle = green;
    ctx.fillRect(pipe.x, bottomY, PIPE_WIDTH, bottomHeight);

    ctx.fillStyle = light;
    ctx.fillRect(pipe.x + 8, bottomY, 10, bottomHeight);

    ctx.fillStyle = dark;
    ctx.fillRect(pipe.x + PIPE_WIDTH - 9, bottomY, 9, bottomHeight);

    ctx.fillStyle = green;
    ctx.fillRect(pipe.x - 6, bottomY, PIPE_WIDTH + 12, 25);

    ctx.strokeStyle = dark;
    ctx.strokeRect(pipe.x - 6, bottomY, PIPE_WIDTH + 12, 25);
}

function drawBird() {
    ctx.save();

    ctx.translate(bird.x, bird.y);
    ctx.rotate(Math.max(-0.45, Math.min(0.85, bird.vy / 9)));

    // Tail
    ctx.fillStyle = SKIN.wing;
    ctx.beginPath();
    ctx.moveTo(-13, 2);
    ctx.lineTo(-27, -5);
    ctx.lineTo(-24, 8);
    ctx.closePath();
    ctx.fill();

    // Body
    if (SKIN.special === "rainbow") {
        const rainbow = ctx.createLinearGradient(-15, -15, 15, 15);
        rainbow.addColorStop(0, "#ff1744");
        rainbow.addColorStop(0.25, "#ff9100");
        rainbow.addColorStop(0.5, "#ffea00");
        rainbow.addColorStop(0.75, "#00e676");
        rainbow.addColorStop(1, "#2979ff");
        ctx.fillStyle = rainbow;
    } else {
        ctx.fillStyle = SKIN.body;
    }

    ctx.strokeStyle = "#35434c";
    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.ellipse(0, 0, 18, 15, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    // Robot details
    if (SKIN.special === "robot") {
        ctx.fillStyle = "#455a64";
        ctx.fillRect(-10, -4, 20, 11);

        ctx.fillStyle = SKIN.eye;
        ctx.fillRect(-7, -2, 5, 4);
        ctx.fillRect(3, -2, 5, 4);

        ctx.fillStyle = "#90a4ae";
        ctx.fillRect(-7, 9, 14, 3);
    } else {
        // Wing
        ctx.fillStyle = SKIN.wing;

        ctx.beginPath();
        ctx.ellipse(-4, 5, 9, 6, -0.35, 0, Math.PI * 2);
        ctx.fill();

        // Eye
        ctx.fillStyle = "white";
        ctx.beginPath();
        ctx.arc(8, -6, 6, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = SKIN.eye;
        ctx.beginPath();
        ctx.arc(10, -6, 2.5, 0, Math.PI * 2);
        ctx.fill();
    }

    // Ninja headband
    if (SKIN.special === "ninja") {
        ctx.fillStyle = "#e53935";
        ctx.fillRect(-14, -10, 27, 5);

        ctx.beginPath();
        ctx.moveTo(10, -8);
        ctx.lineTo(23, -13);
        ctx.lineTo(18, -5);
        ctx.closePath();
        ctx.fill();
    }

    // Slime shine
    if (SKIN.special === "slime") {
        ctx.fillStyle = "rgba(255,255,255,0.65)";
        ctx.beginPath();
        ctx.ellipse(-7, -7, 5, 2.5, -0.5, 0, Math.PI * 2);
        ctx.fill();
    }

    // Fire decoration
    if (SKIN.special === "fire") {
        ctx.fillStyle = "#ffeb3b";
        ctx.beginPath();
        ctx.moveTo(-5, -12);
        ctx.lineTo(1, -23);
        ctx.lineTo(5, -12);
        ctx.closePath();
        ctx.fill();
    }

    // Beak
    ctx.fillStyle = SKIN.beak;
    ctx.beginPath();
    ctx.moveTo(14, 0);
    ctx.lineTo(27, 4);
    ctx.lineTo(14, 8);
    ctx.closePath();
    ctx.fill();

    ctx.restore();
}

function drawGround() {
    ctx.fillStyle = "#e8ca78";
    ctx.fillRect(0, H - GROUND, W, GROUND);

    ctx.fillStyle = "#78cf4b";
    ctx.fillRect(0, H - GROUND, W, 12);

    ctx.fillStyle = "#c3a55b";

    for (
        let x = -20 + (groundOffset % 32);
        x < W;
        x += 32
    ) {
        ctx.beginPath();
        ctx.moveTo(x, H - 35);
        ctx.lineTo(x + 14, H - 35);
        ctx.lineTo(x + 4, H - 29);
        ctx.closePath();
        ctx.fill();
    }
}

function drawMessage(title, subtitle) {
    ctx.fillStyle = "rgba(255,255,255,0.92)";
    ctx.fillRect(55, 245, 370, 105);

    ctx.textAlign = "center";
    ctx.fillStyle = "#17324d";
    ctx.font = "bold 27px Arial";
    ctx.fillText(title, W / 2, 286);

    ctx.font = "16px Arial";
    ctx.fillText(subtitle, W / 2, 320);
}

function draw() {
    drawBackground();
    pipes.forEach(drawPipe);
    drawGround();
    drawBird();

    if (!started) {
        drawMessage("Flappy Bird!", "Tap or press SPACE to start");
    }
}

function collision() {
    if (bird.y - bird.radius <= 0) return true;
    if (bird.y + bird.radius >= H - GROUND) return true;

    for (const pipe of pipes) {
        const topHeight = pipe.center - PIPE_GAP / 2;
        const bottomY = pipe.center + PIPE_GAP / 2;

        const overlapsX =
            bird.x + bird.radius > pipe.x - 5 &&
            bird.x - bird.radius < pipe.x + PIPE_WIDTH + 5;

        if (overlapsX) {
            if (
                bird.y - bird.radius < topHeight ||
                bird.y + bird.radius > bottomY
            ) {
                return true;
            }
        }
    }

    return false;
}

function gameOver() {
    running = false;
    animationId = null;

    best = Math.max(best, score);
    document.getElementById("best").textContent = best;
    document.getElementById("status").textContent = "Game over";

    draw();

    ctx.fillStyle = "rgba(15,35,55,0.68)";
    ctx.fillRect(0, 0, W, H);

    ctx.textAlign = "center";
    ctx.fillStyle = "white";

    ctx.font = "bold 38px Arial";
    ctx.fillText("GAME OVER", W / 2, H / 2 - 30);

    ctx.font = "bold 24px Arial";
    ctx.fillText("Score: " + score, W / 2, H / 2 + 10);

    ctx.font = "16px Arial";
    ctx.fillText("Press FLAP or Restart", W / 2, H / 2 + 48);
}

function tick() {
    if (!running) return;

    frame++;

    bird.vy += GRAVITY;
    bird.y += bird.vy;

    groundOffset += PIPE_SPEED;

    for (const pipe of pipes) {
        pipe.x -= PIPE_SPEED;

        if (!pipe.passed && pipe.x + PIPE_WIDTH < bird.x) {
            pipe.passed = true;
            score++;

            document.getElementById("score").textContent = score;
        }
    }

    pipes = pipes.filter(pipe => pipe.x + PIPE_WIDTH > -20);

    if (
        pipes.length === 0 ||
        pipes[pipes.length - 1].x < W - 225
    ) {
        addPipe(W + 15);
    }

    draw();

    if (collision()) {
        gameOver();
        return;
    }

    animationId = requestAnimationFrame(tick);
}

function startGame() {
    reset();

    started = true;
    running = true;
    bird.vy = JUMP;

    document.getElementById("status").textContent = "Flying!";

    animationId = requestAnimationFrame(tick);
}

function flap() {
    if (!running) {
        startGame();
    } else {
        bird.vy = JUMP;
    }
}

canvas.addEventListener("pointerdown", function(event) {
    event.preventDefault();
    flap();
});

document.getElementById("flap").addEventListener("click", flap);
document.getElementById("restart").addEventListener("click", startGame);

window.addEventListener("keydown", function(event) {
    if (event.code === "Space" || event.code === "ArrowUp") {
        event.preventDefault();
        flap();
    }
});

reset();
</script>
</body>
</html>
"""

# Safely insert the selected skin and difficulty into the game.
GAME_HTML = GAME_HTML.replace(
    "__SKIN_JSON__",
    json.dumps(selected_colors)
)

GAME_HTML = GAME_HTML.replace(
    "__SETTINGS_JSON__",
    json.dumps(settings)
)

components.html(
    GAME_HTML,
    height=790,
    scrolling=False
)

with st.expander("🎮 How to play"):
    st.markdown("""
    - **SPACE / UP ARROW:** Fly up.
    - **Click or tap:** Fly up.
    - Avoid the pipes, ceiling, and ground.
    - Earn one point for each pipe you pass.
    - Use **Start / Restart** to begin a new run.
    - Choose another skin or difficulty from the menu above.
    """)