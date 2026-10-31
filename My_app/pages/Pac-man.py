
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Pac-Man Chase", page_icon="👻", layout="wide")

st.title("👻 Pac-Man Chase")
st.caption("Collect the dots, avoid the ghosts, and use power pellets to turn the tables!")

GAME = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* { box-sizing: border-box; }
body {
  margin: 0; background: #080818; color: white;
  font-family: Arial, sans-serif; text-align: center;
  user-select: none;
}
#hud {
  display:flex; justify-content:center; gap:24px;
  flex-wrap:wrap; padding:12px; font-size:18px;
}
#game {
  width:min(94vw, 630px); height:auto; display:block;
  margin:0 auto; background:#05050f;
  border:2px solid #292967; border-radius:8px;
}
#message { min-height:28px; margin:8px; color:#ffe66d; font-weight:bold; }
.controls {
  display:grid; grid-template-columns:repeat(3,60px);
  gap:6px; justify-content:center; margin:12px auto;
}
button {
  background:#222253; color:white; border:1px solid #5555aa;
  border-radius:10px; padding:12px; font-size:20px;
  cursor:pointer; touch-action:manipulation;
}
button:active { background:#4949a0; }
#restart { font-size:16px; margin-bottom:12px; }
.help { color:#aaaacc; font-size:13px; padding:0 8px 12px; }
</style>
</head>
<body>
<div id="hud">
  <span>⭐ Score: <b id="score">0</b></span>
  <span>❤️ Lives: <b id="lives">3</b></span>
  <span>⚡ Power: <b id="power">Off</b></span>
</div>
<canvas id="game" width="630" height="630"></canvas>
<div id="message">Use WASD or arrow keys to move!</div>
<div class="controls">
  <span></span><button data-dir="up">⬆️</button><span></span>
  <button data-dir="left">⬅️</button>
  <button data-dir="down">⬇️</button>
  <button data-dir="right">➡️</button>
</div>
<button id="restart">🔄 Restart game</button>
<div class="help">Arrow keys / WASD to move · R to restart · Collect ⚡ to scare ghosts</div>

<script>
(() => {
  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d");
  const COLS = 21, ROWS = 21, TILE = 30;
  const DIRS = [
    {x:0,y:-1,name:"up"},
    {x:0,y:1,name:"down"},
    {x:-1,y:0,name:"left"},
    {x:1,y:0,name:"right"}
  ];

  let map, pac, ghosts, score, lives, powerTime, running;
  let wantedDir, lastMove, messageTimer;

  function makeMap() {
    const m = Array.from({length:ROWS}, (_,y) =>
      Array.from({length:COLS}, (_,x) =>
        (x===0 || y===0 || x===COLS-1 || y===ROWS-1) ? "#" : "."
      )
    );

    // Short wall sections leave multiple routes through the maze.
    const horizontalWalls = [
      [3, 3, 7], [3, 13, 17],
      [6, 2, 5], [6, 15, 18],
      [9, 3, 7], [9, 13, 17],
      [12, 2, 5], [12, 15, 18],
      [15, 3, 7], [15, 13, 17],
      [18, 6, 9], [18, 11, 14]
    ];

    horizontalWalls.forEach(([y, a, b]) => {
      for (let x=a; x<=b; x++) m[y][x] = "#";
    });

    const verticalWalls = [
      [5, 4, 6], [5, 14, 16],
      [9, 4, 6], [9, 14, 16],
      [11, 3, 5], [11, 15, 17],
      [15, 4, 6], [15, 14, 16]
    ];

    verticalWalls.forEach(([x, a, b]) => {
      for (let y=a; y<=b; y++) m[y][x] = "#";
    });

    // Keep all starting positions clear.
    [[1,1],[1,2],[2,1],[10,9],[9,10],[10,10],[11,10],[10,11]]
      .forEach(([x,y]) => m[y][x] = ".");

    // Power pellets in four separated areas.
    [[1,1],[19,1],[1,19],[19,19]].forEach(([x,y]) => m[y][x] = "o");

    return m;
  }

  function reset() {
    map = makeMap();
    pac = {x:1, y:1, dir:{x:0,y:0}};
    wantedDir = {x:0,y:0};
    ghosts = [
      {x:10,y:9,color:"#ff4b65",homeX:10,homeY:9},
      {x:9,y:10,color:"#40e7ff",homeX:9,homeY:10},
      {x:11,y:10,color:"#ff9de2",homeX:11,homeY:10},
      {x:10,y:11,color:"#ffae42",homeX:10,homeY:11}
    ];
    score = 0;
    lives = 3;
    powerTime = 0;
    running = true;
    lastMove = 0;
    messageTimer = 0;
    document.getElementById("message").textContent =
      "Collect dots and stay away from the ghosts!";
    updateHUD();
    draw();
  }

  function isWall(x,y) {
    return x<0 || y<0 || x>=COLS || y>=ROWS || map[y][x]==="#";
  }

  function legalMoves(x,y) {
    return DIRS.filter(d => !isWall(x+d.x,y+d.y));
  }

  // BFS: find the shortest route to the target through walkable tiles.
  function findPath(sx,sy,tx,ty) {
    const queue = [{x:sx,y:sy,first:null}];
    const visited = new Set([sx+","+sy]);
    let head = 0;

    while (head < queue.length) {
      const cur = queue[head++];
      if (cur.x===tx && cur.y===ty) return cur.first;

      for (const d of DIRS) {
        const nx = cur.x+d.x, ny = cur.y+d.y;
        const key = nx+","+ny;
        if (isWall(nx,ny) || visited.has(key)) continue;
        visited.add(key);
        queue.push({
          x:nx, y:ny,
          first:cur.first || d
        });
      }
    }
    return null;
  }

  // Calculate distances from Pac-Man so powered ghosts can flee intelligently.
  function distanceMapFromPac() {
    const distances = new Map();
    const queue = [{x:pac.x,y:pac.y,d:0}];
    distances.set(pac.x+","+pac.y, 0);
    let head = 0;

    while (head < queue.length) {
      const c = queue[head++];
      for (const dir of DIRS) {
        const nx=c.x+dir.x, ny=c.y+dir.y;
        const key=nx+","+ny;
        if (isWall(nx,ny) || distances.has(key)) continue;
        distances.set(key,c.d+1);
        queue.push({x:nx,y:ny,d:c.d+1});
      }
    }
    return distances;
  }

  function movePac() {
    const nx = pac.x + wantedDir.x;
    const ny = pac.y + wantedDir.y;

    if (!isWall(nx,ny)) pac.dir = wantedDir;
    const fx = pac.x + pac.dir.x;
    const fy = pac.y + pac.dir.y;

    if (!isWall(fx,fy)) {
      pac.x = fx;
      pac.y = fy;
    }

    const tile = map[pac.y][pac.x];
    if (tile === ".") {
      score += 10;
      map[pac.y][pac.x] = " ";
    } else if (tile === "o") {
      score += 50;
      powerTime = 70;
      map[pac.y][pac.x] = " ";
      document.getElementById("message").textContent =
        "POWER MODE! The ghosts are scared!";
    }

    if (powerTime > 0) powerTime--;
    updateHUD();
    checkGhostCollision();
  }

  function moveGhosts() {
    const distances = powerTime > 0 ? distanceMapFromPac() : null;

    for (const ghost of ghosts) {
      // Always use a path through the maze, never move through walls.
      const options = legalMoves(ghost.x,ghost.y);
      if (!options.length) continue;

      let chosen = null;

      if (powerTime > 0) {
        // Choose the reachable next tile farthest from Pac-Man.
        let bestDistance = -1;
        for (const d of options) {
          const key=(ghost.x+d.x)+","+(ghost.y+d.y);
          const distance=distances.get(key);
          const safeDistance=distance===undefined ? -1 : distance;
          if (safeDistance > bestDistance) {
            bestDistance = safeDistance;
            chosen = d;
          }
        }
      } else {
        // Recompute the shortest path every turn to actively chase Pac-Man.
        chosen = findPath(ghost.x,ghost.y,pac.x,pac.y);
      }

      if (chosen) {
        ghost.x += chosen.x;
        ghost.y += chosen.y;
      }
    }
    checkGhostCollision();
  }

  function checkGhostCollision() {
    for (const ghost of ghosts) {
      if (ghost.x===pac.x && ghost.y===pac.y) {
        if (powerTime > 0) {
          score += 200;
          ghost.x = ghost.homeX;
          ghost.y = ghost.homeY;
          document.getElementById("message").textContent =
            "Ghost caught! +200 points";
        } else {
          lives--;
          updateHUD();
          if (lives <= 0) {
            running = false;
            document.getElementById("message").textContent =
              "Game over! Press Restart to play again.";
          } else {
            pac.x=1; pac.y=1;
            pac.dir={x:0,y:0};
            wantedDir={x:0,y:0};
            ghosts.forEach(g => {g.x=g.homeX; g.y=g.homeY;});
            powerTime=0;
            document.getElementById("message").textContent =
              "Caught! Be careful — you have "+lives+" lives left.";
          }
          updateHUD();
        }
        break;
      }
    }
  }

  function updateHUD() {
    document.getElementById("score").textContent=score;
    document.getElementById("lives").textContent="❤️".repeat(Math.max(0,lives));
    document.getElementById("power").textContent=powerTime>0 ? "⚡ ON" : "Off";
  }

  function draw() {
    ctx.fillStyle="#05050f";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    for (let y=0;y<ROWS;y++) {
      for (let x=0;x<COLS;x++) {
        const px=x*TILE, py=y*TILE;
        if (map[y][x]==="#") {
          ctx.fillStyle="#111a63";
          ctx.fillRect(px+1,py+1,TILE-2,TILE-2);
          ctx.strokeStyle="#354cff";
          ctx.lineWidth=1;
          ctx.strokeRect(px+3,py+3,TILE-6,TILE-6);
        } else if (map[y][x]===".") {
          ctx.fillStyle="#ffe6a1";
          ctx.beginPath();
          ctx.arc(px+TILE/2,py+TILE/2,3,0,Math.PI*2);
          ctx.fill();
        } else if (map[y][x]==="o") {
          ctx.fillStyle="#ffffff";
          ctx.shadowColor="#7df9ff";
          ctx.shadowBlur=14;
          ctx.beginPath();
          ctx.arc(px+TILE/2,py+TILE/2,7,0,Math.PI*2);
          ctx.fill();
          ctx.shadowBlur=0;
        }
      }
    }

    // Pac-Man
    const cx=pac.x*TILE+TILE/2, cy=pac.y*TILE+TILE/2;
    const angle=Math.atan2(pac.dir.y,pac.dir.x);
    const mouth=0.22;
    ctx.fillStyle="#ffe500";
    ctx.beginPath();
    ctx.moveTo(cx,cy);
    ctx.arc(cx,cy,12,angle+mouth,angle+Math.PI*2-mouth);
    ctx.closePath();
    ctx.fill();

    // Ghosts
    for (const g of ghosts) {
      const gx=g.x*TILE+TILE/2, gy=g.y*TILE+TILE/2;
      ctx.fillStyle=powerTime>0 ? "#477bff" : g.color;
      ctx.beginPath();
      ctx.arc(gx,gy-2,11,Math.PI,0);
      ctx.lineTo(gx+11,gy+10);
      ctx.lineTo(gx+5,gy+6);
      ctx.lineTo(gx,gy+10);
      ctx.lineTo(gx-5,gy+6);
      ctx.lineTo(gx-11,gy+10);
      ctx.closePath();
      ctx.fill();

      ctx.fillStyle="white";
      ctx.beginPath();
      ctx.arc(gx-4,gy-2,4,0,Math.PI*2);
      ctx.arc(gx+4,gy-2,4,0,Math.PI*2);
      ctx.fill();
      ctx.fillStyle="#15152c";
      ctx.beginPath();
      ctx.arc(gx-3,gy-2,2,0,Math.PI*2);
      ctx.arc(gx+5,gy-2,2,0,Math.PI*2);
      ctx.fill();
    }
  }

  function gameLoop(timestamp) {
    if (running && timestamp-lastMove >= 125) {
      movePac();
      if (running) moveGhosts();
      lastMove=timestamp;
      updateHUD();
    }
    draw();
    requestAnimationFrame(gameLoop);
  }

  function setDirection(name) {
    const d=DIRS.find(v=>v.name===name);
    if (d) wantedDir={x:d.x,y:d.y};
  }

  document.addEventListener("keydown", e => {
    const key=e.key.toLowerCase();
    const keys={
      arrowup:"up", w:"up",
      arrowdown:"down", s:"down",
      arrowleft:"left", a:"left",
      arrowright:"right", d:"right"
    };
    if (keys[key]) {
      e.preventDefault();
      setDirection(keys[key]);
    }
    if (key==="r") reset();
  });

  document.querySelectorAll("[data-dir]").forEach(button => {
    button.addEventListener("pointerdown", e => {
      e.preventDefault();
      setDirection(button.dataset.dir);
    });
  });

  document.getElementById("restart").addEventListener("click", reset);

  reset();
  requestAnimationFrame(gameLoop);
})();
</script>
</body>
</html>
"""

components.html(GAME, height=850, scrolling=False)