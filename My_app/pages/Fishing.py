
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="River Fishing", page_icon="🎣", layout="centered")

GAME = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box}
body{margin:0;background:#0a171e;color:#f3eee0;font-family:Arial,sans-serif}
#game{max-width:1050px;margin:auto;background:#102832;border:2px solid #79552f;border-radius:13px;overflow:hidden;box-shadow:0 8px 35px #0008}
header{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;padding:11px 14px;background:linear-gradient(100deg,#251c16,#17333a);border-bottom:2px solid #80603a}
.logo{font-weight:1000;font-style:italic;font-size:clamp(19px,3vw,27px);letter-spacing:1px}
.stats{display:flex;gap:5px;flex-wrap:wrap}
.stat{font-size:12px;background:#09252f;border:1px solid #426b74;padding:8px 9px;border-radius:8px}
#stage{position:relative;width:100%;background:#285a61}
canvas{display:block;width:100%;height:auto;aspect-ratio:1000/570}
#hint{position:absolute;left:12px;top:12px;background:#052530dd;border:1px solid #61808a;border-radius:8px;padding:10px 12px;font-size:12px;max-width:235px;line-height:1.4;pointer-events:none}
#fightbar{display:none;position:absolute;left:15%;width:70%;bottom:15px;height:20px;background:#12252c;border:2px solid #b5c8b9;border-radius:8px;overflow:hidden}
#target{position:absolute;top:0;bottom:0;background:#5ccf8b88;border-left:2px solid #8affb1;border-right:2px solid #8affb1}
#marker{position:absolute;top:0;bottom:0;width:4px;background:#ffdc6b;box-shadow:0 0 7px #ffdc6b}
#progresswrap{display:none;position:absolute;left:25%;width:50%;bottom:43px;height:8px;border-radius:9px;background:#07171c;border:1px solid #71969b;overflow:hidden}
#progress{height:100%;width:0;background:#5fda91;transition:width .12s}
#controls{padding:12px;background:linear-gradient(#30271e,#191510);border-top:3px solid #765334}
.buttons{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px}
button{border:1px solid #56747a;border-radius:8px;background:linear-gradient(#193d49,#0b2731);color:#f5f1e6;font-weight:bold;cursor:pointer;padding:11px 5px;min-height:49px;font-size:12px}
button:hover{filter:brightness(1.2)}
button:disabled{opacity:.35;cursor:not-allowed}
.green{background:linear-gradient(#39a969,#08613c);border-color:#8de5a8}
.gold{background:linear-gradient(#eab24d,#925815);border-color:#ffda89}
#status{background:#07232d;border:1px solid #365c64;border-radius:8px;padding:10px;margin-top:9px;font-size:12px;min-height:36px}
#panel{display:none;padding:13px;background:#0d242c;border-top:1px solid #426872}
#panel h3{margin:0 0 12px}
.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.card{border:1px solid #3e626b;background:#18333b;border-radius:9px;padding:10px;font-size:12px}
.card p{margin:7px 0;color:#c6d8d6}
.card button{width:100%;margin-top:5px}
#modal{display:none;position:absolute;inset:0;z-index:5;background:#00121cc9;align-items:center;justify-content:center;padding:12px}
#catchbox{width:min(570px,96%);max-height:98%;overflow:auto;background:linear-gradient(145deg,#103c49,#061d28);border:2px solid #91a9a2;border-radius:15px;padding:13px;text-align:center;box-shadow:0 8px 35px #000b}
#catchtitle{font-size:clamp(22px,4vw,32px);font-weight:1000;font-style:italic;margin:0 0 10px}
.catchstats{display:flex;justify-content:space-between;gap:10px;text-align:left;font-size:13px}
#heldscene{width:100%;height:auto;display:block;max-height:230px;margin:5px auto;border:1px solid #2c6470;border-radius:9px;background:#092d3b}
.actions{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}
.actions button{font-size:12px;min-height:55px}
.store{background:linear-gradient(#35a968,#08613d);border-color:#90e2a5}
.sell{background:linear-gradient(#e7ad40,#925510);border-color:#ffda83}
.cancel{background:linear-gradient(#435b68,#172a35);border-color:#8ca0aa}
@media(max-width:600px){
 .buttons{grid-template-columns:repeat(3,minmax(0,1fr))}
 .stat{font-size:10px;padding:6px}
 #hint{max-width:165px;font-size:10px;padding:7px}
 #controls{padding:8px}
 .actions button{font-size:10px;padding:5px}
}
</style>
</head>
<body>
<div id="game">
<header>
 <div class="logo">🎣 RIVER FISHING</div>
 <div class="stats">
  <div class="stat">🪙 $<b id="money">120</b></div>
  <div class="stat">🎒 <b id="count">0</b>/12</div>
  <div class="stat">🎣 <b id="rodname">Wood Rod</b></div>
  <div class="stat">🪱 <b id="baitname">Worm</b></div>
 </div>
</header>
<div id="stage">
 <canvas id="world" width="1000" height="570"></canvas>
 <div id="hint">🎣 Cast your line into the river.</div>
 <div id="progresswrap"><div id="progress"></div></div>
 <div id="fightbar"><div id="target"></div><div id="marker"></div></div>
 <div id="modal">
  <div id="catchbox">
   <div id="catchtitle">YOU CAUGHT A FISH!</div>
   <div class="catchstats">
    <div><b id="catchname">Goonch Catfish</b><br><span id="catchrarity">★ RARE</span></div>
    <div style="text-align:right">Weight: <b id="catchweight">2.5 kg</b><br>Value: <b id="catchvalue">$100</b></div>
   </div>
   <canvas id="heldscene" width="650" height="250"></canvas>
   <div style="font-size:11px;color:#c5d9d8;margin:5px 0 9px">What would you like to do with your catch?</div>
   <div class="actions">
    <button class="store" id="store">▣ STORE<br><small>Keep in inventory</small></button>
    <button class="sell" id="sellcatch">＄ SELL<br><small>Get the money</small></button>
    <button class="cancel" id="nevermind">✕ NEVERMIND<br><small>Keep holding it</small></button>
   </div>
  </div>
 </div>
</div>
<div id="controls">
 <div class="buttons">
  <button class="green" id="cast">🎣<br>CAST LINE</button>
  <button class="gold" id="reel" disabled>🌀<br>REEL IN</button>
  <button id="hold">✋<br>HOLD / PUT AWAY</button>
  <button id="bag">🎒<br>INVENTORY</button>
  <button id="shop">🛒<br>SHOP</button>
  <button id="sellall">＄<br>SELL ALL</button>
 </div>
 <div id="status">● Ready to fish.</div>
</div>
<div id="panel"><h3 id="ptitle">Inventory</h3><div id="pbody"></div><button style="width:100%;margin-top:10px" id="close">CLOSE</button></div>
</div>
<script>
"use strict";
const $=id=>document.getElementById(id);
const c=$("world"),ctx=c.getContext("2d");
const hc=$("heldscene"),hctx=hc.getContext("2d");
const W=1000,H=570;
const rods=[
 {name:"Wood Rod",price:0,power:1},
 {name:"River Rod",price:120,power:1.5},
 {name:"Carbon Rod",price:320,power:2},
 {name:"Deepwater Rod",price:700,power:3}
];
const baits=[
 {name:"Worm",price:0,luck:0},
 {name:"Fish Pieces",price:35,luck:.12},
 {name:"Premium Bait",price:100,luck:.3}
];
const types=[
 {name:"Brown Bullhead",weight:25,value:15,min:.4,max:1.8,rarity:"COMMON",color:"#8b7b5b",len:125},
 {name:"Channel Catfish",weight:25,value:25,min:.7,max:3,rarity:"COMMON",color:"#78877b",len:150},
 {name:"Blue Catfish",weight:18,value:42,min:1,max:4,rarity:"UNCOMMON",color:"#657e8d",len:165},
 {name:"Flathead Catfish",weight:13,value:50,min:1,max:5,rarity:"UNCOMMON",color:"#938461",len:160},
 {name:"Redtail Catfish",weight:8,value:90,min:1.5,max:7,rarity:"RARE",color:"#a2684d",len:170},
 {name:"Goonch Catfish",weight:16,value:100,min:1.5,max:6,rarity:"RARE",color:"#65725f",len:185},
 {name:"Giant Goonch",weight:5,value:260,min:4,max:12,rarity:"EPIC",color:"#525e50",len:205},
 {name:"Golden Catfish",weight:3,value:380,min:2,max:8,rarity:"EPIC",color:"#bd984e",len:170},
 {name:"Ancient Goonch",weight:1,value:850,min:6,max:18,rarity:"LEGENDARY",color:"#6e6179",len:220}
];
let money=120,rod=0,bait=0,bag=[],held=null,pending=null;
let phase="idle",fish=null,progress=0,marker=.1,markerDir=1,target=.5,targetW=.3;
let time=0,last=performance.now(),bob={x:720,y:390},fishPos={x:720,y:480};
let fishAngle=0,biteFlash=0,hooked=false,hookPoint={x:0,y:0};
let panelOpen=false;

function say(s){$("status").textContent="● "+s;$("hint").textContent=s}
function updateUI(){
 $("money").textContent=money;$("count").textContent=bag.length;
 $("rodname").textContent=rods[rod].name;$("baitname").textContent=baits[bait].name;
 $("cast").disabled=["waiting","approach","fight","caught"].includes(phase)||!!pending;
 $("reel").disabled=phase!=="fight";
 $("fightbar").style.display=phase==="fight"?"block":"none";
 $("progresswrap").style.display=phase==="fight"?"block":"none";
 $("progress").style.width=(progress*100)+"%";
 $("target").style.left=((target-targetW/2)*100)+"%";
 $("target").style.width=(targetW*100)+"%";
 $("marker").style.left=(marker*100)+"%";
}
function chooseFish(){
 let list=types.map(f=>({f,w:f.weight*(f.name.includes("Goonch")?1.4:1)*(1+baits[bait].luck)}));
 let n=Math.random()*list.reduce((a,x)=>a+x.w,0);
 for(const x of list){n-=x.w;if(n<=0)return x.f}
 return types[1]
}
function ellipse(x,y,rx,ry,fill,stroke=null){
 ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,Math.PI*2);
 ctx.fillStyle=fill;ctx.fill();if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=2;ctx.stroke()}
}
function path(points,fill,stroke=null,width=1){
 ctx.beginPath();ctx.moveTo(points[0][0],points[0][1]);
 for(let i=1;i<points.length;i++)ctx.lineTo(points[i][0],points[i][1]);
 ctx.closePath();ctx.fillStyle=fill;ctx.fill();
 if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=width;ctx.stroke()}
}
function drawBackground(){
 let g=ctx.createLinearGradient(0,0,0,570);
 g.addColorStop(0,"#a4c8c5");g.addColorStop(.55,"#d9d9b8");g.addColorStop(1,"#427e7c");
 ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
 ellipse(850,78,34,34,"#fff0ba");
 path([[0,260],[100,150],[175,205],[305,78],[420,192],[550,105],[680,220],[820,95],[940,195],[1000,160],[1000,380],[0,380]],"#7e9f91");
 path([[0,300],[120,210],[230,270],[370,145],[475,252],[610,172],[755,285],[875,170],[1000,255],[1000,395],[0,395]],"#4c7969");
 path([[0,345],[120,310],[230,330],[380,285],[510,342],[680,300],[820,344],[1000,290],[1000,405],[0,405]],"#315b48");
 for(let i=0;i<21;i++){
  let x=i*52;
  path([[x-20,405],[x+4,300-(i%3)*18],[x+28,405]],i%2?"#214b3b":"#2e5c43");
 }
 let water=ctx.createLinearGradient(0,385,0,570);
 water.addColorStop(0,"#52949a");water.addColorStop(.5,"#27717e");water.addColorStop(1,"#0d3b4e");
 ctx.fillStyle=water;ctx.fillRect(0,385,1000,185);
 ctx.strokeStyle="#c0ded0";ctx.lineWidth=3;ctx.beginPath();
 ctx.moveTo(0,385);ctx.quadraticCurveTo(220,371,400,388);ctx.quadraticCurveTo(650,400,1000,382);ctx.stroke();
 for(let i=0;i<16;i++){
  const x=((i*87+time*18)%1120)-60;
  const y=414+(i*23)%142;
  ctx.globalAlpha=.12+(i%3)*.05;ctx.strokeStyle="#d6f0dc";ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+30+(i%4)*8,y);ctx.stroke();
 }
 ctx.globalAlpha=1;
 // foreground banks
 path([[0,570],[0,520],[45,500],[85,525],[132,515],[165,570]],"#273f32");
 path([[1000,570],[1000,514],[951,498],[914,522],[872,510],[830,570]],"#273f32");
}
function drawPerson(){
 // A small angler on the left bank.
 path([[35,387],[45,331],[68,310],[100,320],[119,387]],"#34483b");
 path([[53,329],[48,296],[65,273],[92,277],[106,302],[94,330]],"#9e7758");
 path([[47,300],[43,277],[61,257],[91,262],[108,282],[98,293],[70,282]],"#393329");
 path([[36,279],[65,260],[103,275],[104,283],[44,288]],"#b19b5f");
 path([[65,334],[104,320],[129,343],[119,365],[90,355]],"#6c805c");
 // One rod only.
 const tip={x:430,y:198};
 ctx.lineCap="round";
 ctx.strokeStyle="#392b1d";ctx.lineWidth=9;ctx.beginPath();ctx.moveTo(106,339);ctx.lineTo(tip.x,tip.y);ctx.stroke();
 ctx.strokeStyle="#b38a52";ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(106,339);ctx.lineTo(tip.x,tip.y);ctx.stroke();
 ctx.strokeStyle="#f0dcb7";ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(106,339);ctx.lineTo(tip.x,tip.y);ctx.stroke();
 return tip;
}
function drawFish(x,y,len,color,angle=0,scaleY=1){
 ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.scale(1,scaleY);
 const L=len,body=L*.34,head=L*.13;
 // Tail: narrow, forked and attached to body.
 path([[-body*.9,-2],[-L*.48,-L*.17],[-L*.44,0],[-L*.49,L*.13],[-body*.9,5]],shade(color,-18),"#263b34",1.5);
 // Dorsal fin
 path([[-L*.20,-L*.10],[-L*.08,-L*.24],[L*.04,-L*.11]],shade(color,-12),"#2d4138",1.2);
 // Anal fin
 path([[-L*.10,L*.10],[L*.05,L*.21],[L*.14,L*.09]],shade(color,-7),"#2d4138",1.2);
 // Long, slim body with tapering tail and slightly broad head.
 ctx.beginPath();
 ctx.moveTo(-L*.39,0);
 ctx.bezierCurveTo(-L*.32,-L*.105,-L*.10,-L*.13,L*.11,-L*.09);
 ctx.quadraticCurveTo(L*.28,-L*.06,L*.39,-L*.015);
 ctx.lineTo(L*.43,L*.015);
 ctx.quadraticCurveTo(L*.29,L*.075,L*.12,L*.095);
 ctx.bezierCurveTo(-L*.10,L*.12,-L*.31,L*.075,-L*.39,0);
 let grad=ctx.createLinearGradient(0,-L*.13,0,L*.13);
 grad.addColorStop(0,shade(color,26));grad.addColorStop(.42,color);
 grad.addColorStop(.78,shade(color,-3));grad.addColorStop(1,"#c8c2a7");
 ctx.fillStyle=grad;ctx.fill();ctx.strokeStyle="#293e34";ctx.lineWidth=1.8;ctx.stroke();
 // Pale belly.
 ctx.beginPath();ctx.moveTo(-L*.28,L*.045);
 ctx.quadraticCurveTo(0,L*.13,L*.32,L*.035);
 ctx.quadraticCurveTo(L*.17,L*.11,-L*.15,L*.075);ctx.fillStyle="#c7c3aa";ctx.fill();
 // Natural mottled markings.
 for(let i=0;i<9;i++){
  let xx=-L*.23+i*L*.055;
  ellipse(xx,Math.sin(i*2.2)*L*.025,L*.016,L*.009,i%2?"#344b3d88":"#d0c9a366");
 }
 // Gill plate.
 ctx.strokeStyle="#33473a";ctx.lineWidth=1.4;ctx.beginPath();
 ctx.ellipse(L*.24,0,L*.035,L*.06,.12,0,Math.PI*2);ctx.stroke();
 // Eye and mouth.
 ellipse(L*.355,-L*.025,L*.012,L*.012,"#16241e");
 ellipse(L*.359,-L*.029,L*.004,L*.004,"#fff0d0");
 ctx.strokeStyle="#263a30";ctx.lineWidth=1.4;ctx.beginPath();
 ctx.moveTo(L*.39,L*.01);ctx.lineTo(L*.435,L*.016);ctx.stroke();
 // Four whiskers emerging at the mouth, bending forward.
 ctx.strokeStyle="#d5d0b8";ctx.lineWidth=1.25;ctx.lineCap="round";
 for(let i=0;i<4;i++){
  const sy=(i-1.5)*L*.018;
  ctx.beginPath();ctx.moveTo(L*.39,sy);
  ctx.quadraticCurveTo(L*.46,sy+(i%2?L*.045:-L*.035),L*(.51+(i%2)*.025),sy+(i%2?L*.07:-L*.065));
  ctx.stroke();
 }
 // Pectoral fin.
 path([[L*.16,L*.04],[L*.05,L*.14],[L*.25,L*.075]],shade(color,-15),"#35493d",1);
 ctx.restore();
}
function shade(hex,amt){
 let h=hex.replace("#","");if(h.length!==6)return hex;
 let n=parseInt(h,16),r=Math.max(0,Math.min(255,(n>>16)+amt)),
 g=Math.max(0,Math.min(255,((n>>8)&255)+amt)),
 b=Math.max(0,Math.min(255,(n&255)+amt));
 return "#"+[r,g,b].map(v=>Math.round(v).toString(16).padStart(2,"0")).join("");
}
function drawBobber(){
 // A small taut line from rod tip to the bobber: the endpoint is the bobber centre.
 const tip={x:430,y:198};
 ctx.strokeStyle="#f4e8cf";ctx.lineWidth=1.4;
 ctx.beginPath();ctx.moveTo(tip.x,tip.y);
 if(phase==="idle"){
  ctx.quadraticCurveTo(470,290,tip.x+18,385);
 }else{
  ctx.quadraticCurveTo((tip.x+bob.x)/2-28,(tip.y+bob.y)/2+25,bob.x,bob.y);
 }
 ctx.stroke();
 if(!["waiting","approach","fight"].includes(phase))return;
 // Bobber floats at the actual endpoint of the fishing line.
 ellipse(bob.x,bob.y+4,10,3,"#0a3138aa");
 ctx.beginPath();ctx.ellipse(bob.x,bob.y,6,8,0,0,Math.PI*2);
 ctx.fillStyle="#f4e6c6";ctx.fill();ctx.strokeStyle="#f6f1d9";ctx.lineWidth=1;ctx.stroke();
 ctx.fillStyle="#d95c3e";ctx.fillRect(bob.x-5,bob.y-5,10,4);
 // Hook below bobber, visible in the water.
 ctx.strokeStyle="#d6d1b8";ctx.lineWidth=1.4;ctx.beginPath();
 ctx.moveTo(bob.x,bob.y+8);ctx.lineTo(bob.x,bob.y+17);
 ctx.quadraticCurveTo(bob.x+9,bob.y+23,bob.x+7,bob.y+13);ctx.stroke();
}
function drawWaterFish(){
 if(phase==="idle"||phase==="waiting"){
  const x=fishPos.x+Math.sin(time*.7)*18;
  const y=fishPos.y+Math.sin(time*1.4)*4;
  ctx.globalAlpha=.72;drawFish(x,y,fish?fish.len:150,fish?fish.color:"#687c70",0,1);ctx.globalAlpha=1;
  return;
 }
 if(!fish)return;
 if(phase==="approach"){
  const x=fishPos.x,y=fishPos.y;
  drawFish(x,y,fish.len,fish.color,Math.sin(time*5)*.025,1);
  return;
 }
 if(phase==="fight"){
  // The mouth is drawn very close to the bobber/hook, not elsewhere on the lake.
  const x=fishPos.x,y=fishPos.y;
  const dx=bob.x-x,dy=bob.y-y;
  const angle=Math.atan2(dy,dx);
  drawFish(x,y,fish.len,fish.color,angle,1+Math.sin(time*17)*.025);
  // Hook connection visibly reaches the fish mouth.
  const mouthX=x+Math.cos(angle)*fish.len*.43;
  const mouthY=y+Math.sin(angle)*fish.len*.43;
  ctx.strokeStyle="#fff0ce";ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(bob.x,bob.y+17);ctx.lineTo(mouthX,mouthY);ctx.stroke();
  hookPoint={x:mouthX,y:mouthY};
 }
}
function draw(){
 ctx.clearRect(0,0,W,H);
 drawBackground();
 const tip=drawPerson();
 drawWaterFish();
 drawBobber();
 if(phase==="caught"||held){
  drawFish(620,465,(held||pending||fish).len,(held||pending||fish).color,0,1);
 }
}
function cast(){
 if(!["idle"].includes(phase)||pending)return;
 phase="waiting";fish=null;hooked=false;progress=0;
 bob={x:690+Math.random()*140,y:400+Math.random()*45};
 fishPos={x:bob.x-90,y:485};
 say("Your bait is in the water. Watch for a fish approaching...");
 updateUI();
 setTimeout(()=>{
  if(phase!=="waiting")return;
  fish=chooseFish();phase="approach";biteFlash=0;
  say("A "+fish.name+" is approaching the bait...");
  updateUI();
  const start=performance.now();
  function approachStep(now){
   if(phase!=="approach")return;
   const t=Math.min(1,(now-start)/1600);
   fishPos.x=(bob.x-fish.len*.40-20)*(1-t)+(bob.x-fish.len*.40-20)*t;
   fishPos.y=(485*(1-t)+(bob.y+30)*t);
   if(t<1)requestAnimationFrame(approachStep);
   else{
    phase="fight";hooked=true;targetW=fish.name.includes("Goonch")?.43:.27;
    target=.5;marker=.08;markerDir=1;progress=0;
    say("BITE! The hook is attached to the fish's mouth. Click REEL IN when the marker is in the green zone.");
    updateUI()
   }
  }
  requestAnimationFrame(approachStep)
 },1800+Math.random()*1200)
}
function reel(){
 if(phase!=="fight"||!fish)return;
 const good=Math.abs(marker-target)<targetW/2;
 progress=Math.max(0,Math.min(1,progress+(good?.20:(fish.name.includes("Goonch")?-.01:-.04))));
 if(progress>=1){
  phase="caught";
  let weight=+(fish.min+Math.random()*(fish.max-fish.min)).toFixed(1);
  let mutation=Math.random()<.07?"Shimmering":null;
  pending={...fish,weight,mutation,value:Math.round(fish.value*weight*(mutation?3:1))};
  $("catchname").textContent=pending.name;
  $("catchrarity").textContent="★ "+pending.rarity+(mutation?" · "+mutation:"");
  $("catchweight").textContent=weight+" kg";
  $("catchvalue").textContent="$"+pending.value;
  drawHeldFish(pending);
  $("modal").style.display="flex";
  say("Catch secured! Store it, sell it, or keep holding it.");
  updateUI()
 }else{
  say(good?"Nice! You are reeling the fish in.":"Missed the green zone — try again.")
 }
 updateUI()
}
function drawHeldFish(f){
 const x=hctx;
 x.clearRect(0,0,650,250);
 const g=x.createLinearGradient(0,0,0,250);
 g.addColorStop(0,"#1a5964");g.addColorStop(1,"#092d3b");
 x.fillStyle=g;x.fillRect(0,0,650,250);
 for(let i=0;i<7;i++){
  x.strokeStyle="#c5e4dc30";x.lineWidth=2;
  x.beginPath();x.moveTo(i*95,40+i%3*25);x.lineTo(i*95+45,40+i%3*25);x.stroke()
 }
 // Two forearms/hands beneath the fish.
 function hand(px,flip){
  x.save();x.translate(px,0);x.scale(flip?-1:1,1);
  x.fillStyle="#6b4d38";x.beginPath();x.moveTo(0,250);x.lineTo(12,195);
  x.quadraticCurveTo(25,177,58,167);x.lineTo(108,155);
  x.quadraticCurveTo(128,154,131,174);x.lineTo(103,193);
  x.lineTo(77,205);x.lineTo(65,250);x.closePath();x.fill();
  x.fillStyle="#bc8a67";x.beginPath();x.moveTo(4,250);x.lineTo(18,199);
  x.quadraticCurveTo(26,184,57,178);x.lineTo(100,165);
  x.quadraticCurveTo(118,165,119,177);x.lineTo(91,194);
  x.lineTo(70,210);x.lineTo(65,250);x.closePath();x.fill();
  x.restore()
 }
 hand(72,false);hand(578,true);
 // Slim fish lies across the palms; tail on the left, head and whiskers on the right.
 x.save();x.translate(325,116);x.scale(1.8,1.8);
 drawFishCanvas(x,f,205);
 x.restore();
}
function drawFishCanvas(x,f,L){
 // Canvas version of the same slender fish shape for the caught-fish scene.
 x.save();
 x.fillStyle=shade(f.color,-18);x.beginPath();
 x.moveTo(-L*.37,0);x.lineTo(-L*.49,-L*.16);x.lineTo(-L*.45,0);x.lineTo(-L*.49,L*.13);x.lineTo(-L*.37,L*.035);x.fill();
 x.fillStyle=shade(f.color,-12);x.beginPath();
 x.moveTo(-L*.2,-L*.07);x.lineTo(-L*.08,-L*.21);x.lineTo(L*.03,-L*.08);x.fill();
 x.beginPath();x.moveTo(-L*.1,L*.07);x.lineTo(L*.02,L*.19);x.lineTo(L*.13,L*.06);x.fill();
 const gr=x.createLinearGradient(0,-L*.12,0,L*.12);
 gr.addColorStop(0,shade(f.color,25));gr.addColorStop(.5,f.color);gr.addColorStop(1,"#c6c0a8");
 x.beginPath();x.moveTo(-L*.39,0);
 x.bezierCurveTo(-L*.3,-L*.1,-L*.08,-L*.13,L*.14,-L*.08);
 x.quadraticCurveTo(L*.3,-L*.04,L*.4,0);
 x.quadraticCurveTo(L*.28,L*.08,L*.12,L*.09);
 x.bezierCurveTo(-L*.1,L*.12,-L*.31,L*.07,-L*.39,0);
 x.fillStyle=gr;x.fill();x.strokeStyle="#2a3b31";x.lineWidth=1.3;x.stroke();
 x.fillStyle="#c8c2ab";x.beginPath();x.moveTo(-L*.25,L*.045);
 x.quadraticCurveTo(0,L*.105,L*.34,L*.025);x.quadraticCurveTo(0,L*.13,-L*.25,L*.045);x.fill();
 for(let i=0;i<8;i++){
  x.fillStyle="#30463888";x.beginPath();x.ellipse(-L*.22+i*L*.07,Math.sin(i*2)*L*.025,L*.013,L*.008,0,0,Math.PI*2);x.fill()
 }
 x.strokeStyle="#304638";x.lineWidth=1.4;x.beginPath();x.ellipse(L*.25,0,L*.032,L*.055,0,0,Math.PI*2);x.stroke();
 x.fillStyle="#17241d";x.beginPath();x.arc(L*.355,-L*.025,L*.012,0,Math.PI*2);x.fill();
 x.fillStyle="#fff1d1";x.beginPath();x.arc(L*.359,-L*.029,L*.004,0,Math.PI*2);x.fill();
 x.strokeStyle="#d2cbb4";x.lineWidth=1.1;
 for(let i=0;i<4;i++){
  let sy=(i-1.5)*L*.017;x.beginPath();x.moveTo(L*.39,sy);
  x.quadraticCurveTo(L*.46,sy+(i%2?L*.04:-L*.03),L*.51,sy+(i%2?L*.06:-L*.06));x.stroke()
 }
 x.restore()
}
function storeCatch(){
 if(!pending)return;
 if(bag.length>=12){say("Inventory full! Sell some fish first.");return}
 bag.push(pending);pending=null;phase="idle";$("modal").style.display="none";
 updateUI();say("Fish stored in your inventory.")
}
function sellCatch(){
 if(!pending)return;
 money+=pending.value;let n=pending.name,v=pending.value;
 pending=null;phase="idle";$("modal").style.display="none";
 updateUI();say("Sold "+n+" for $"+v+".")
}
function nevermind(){
 if(!pending)return;
 held=pending;pending=null;phase="idle";$("modal").style.display="none";
 updateUI();say("You're holding the fish. Press HOLD / PUT AWAY to store it.")
}
function holdFish(){
 if(held){
  if(bag.length>=12){say("Inventory full! Sell some fish first.");return}
  bag.push(held);held=null;updateUI();say("Fish put away in your inventory.")
 }else if(bag.length){
  held=bag.pop();updateUI();say("You're holding "+held.name+".")
 }else say("Catch a fish first.")
}
function openPanel(title,html){
 $("ptitle").textContent=title;$("pbody").innerHTML=html;
 $("panel").style.display="block";panelOpen=true
}
function closePanel(){$("panel").style.display="none";panelOpen=false}
function showBag(){
 let html=bag.length?'<div class="cards">':"<p>Your inventory is empty.</p>";
 bag.forEach((f,i)=>{
  html+=`<div class="card"><b>${f.name}</b><p>${f.weight} kg · ${f.rarity}</p><p>Value: $${f.value}</p><button onclick="takeFish(${i})">HOLD FISH</button></div>`
 });
 if(bag.length)html+="</div>";
 openPanel("🎒 Inventory",html)
}
function takeFish(i){
 if(held){say("Put away the fish you're holding first.");return}
 held=bag.splice(i,1)[0];closePanel();updateUI();say("Holding "+held.name+".")
}
function showShop(){
 let html="<h3>Fishing rods</h3><div class='cards'>";
 rods.forEach((r,i)=>{
  html+=`<div class="card"><b>${r.name}</b><p>Power ${r.power} · $${r.price}</p><button ${i<=rod?"disabled":""} onclick="buyRod(${i})">${i===rod?"EQUIPPED":i<rod?"OWNED":"BUY"}</button></div>`
 });
 html+="</div><h3 style='margin-top:15px'>Bait</h3><div class='cards'>";
 baits.forEach((b,i)=>{
  html+=`<div class="card"><b>${b.name}</b><p>$${b.price} · Improves rare-fish odds</p><button onclick="buyBait(${i})">${bait===i?"SELECTED":"SELECT / BUY"}</button></div>`
 });
 html+="</div>";
 openPanel("🛒 Tackle shop",html)
}
function buyRod(i){
 if(i!==rod+1){say("Buy the previous rod first.");return}
 if(money<rods[i].price){say("Not enough money.");return}
 money-=rods[i].price;rod=i;updateUI();showShop();say("Equipped "+rods[i].name+".")
}
function buyBait(i){
 if(i!==0&&money<baits[i].price){say("Not enough money.");return}
 if(i!==0)money-=baits[i].price;
 bait=i;updateUI();showShop();say("Selected "+baits[i].name+".")
}
function sellAll(){
 if(!bag.length){say("No stored fish to sell.");return}
 let total=bag.reduce((s,f)=>s+f.value,0),n=bag.length;
 bag=[];money+=total;updateUI();say("Sold "+n+" fish for $"+total+".")
}
$("cast").onclick=cast;$("reel").onclick=reel;$("hold").onclick=holdFish;
$("bag").onclick=showBag;$("shop").onclick=showShop;$("sellall").onclick=sellAll;
$("store").onclick=storeCatch;$("sellcatch").onclick=sellCatch;$("nevermind").onclick=nevermind;
$("close").onclick=closePanel;

function animate(now){
 const dt=Math.min(.05,(now-last)/1000);last=now;time+=dt;
 if(phase==="fight"){
  marker+=markerDir*dt*(fish&&fish.name.includes("Goonch")?.25:.40);
  if(marker>.99){marker=.99;markerDir=-1}
  if(marker<.01){marker=.01;markerDir=1}
  $("marker").style.left=(marker*100)+"%";
 }
 if(phase==="waiting"){
  bob.y=405+Math.sin(time*3)*2;
 }
 if(phase==="approach"){
  // Fish noses toward the bait; body stays behind its mouth.
  fishPos.x=bob.x-fish.len*.43;
  fishPos.y+=(bob.y+27-fishPos.y)*Math.min(1,dt*2.5);
 }
 if(phase==="fight"&&fish){
  fishPos.x+=(bob.x-fish.len*.43-fishPos.x)*Math.min(1,dt*4);
  fishPos.y+=(bob.y+20-fishPos.y)*Math.min(1,dt*4);
 }
 draw();
 requestAnimationFrame(animate)
}
updateUI();requestAnimationFrame(animate);
</script>
</body>
</html>
"""

components.html(GAME, height=900, scrolling=True)
