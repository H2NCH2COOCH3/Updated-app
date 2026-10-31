import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Paper Minecraft",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GAME = r'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

<style>
*{
    box-sizing:border-box;
}

html,
body{
    margin:0;
    padding:0;
    width:100%;
    height:100%;
    overflow:hidden;
    background:#111827;
    color:#f3f4f6;
    font-family:Arial,Helvetica,sans-serif;
}

#root{
    width:100%;
    height:100vh;
    min-height:650px;
    display:flex;
    flex-direction:column;
}

#topbar{
    display:flex;
    gap:7px;
    padding:7px 9px;
    background:#1f2937;
    border-bottom:1px solid #374151;
    flex-wrap:wrap;
}

button{
    border:1px solid #4b5563;
    background:#374151;
    color:#fff;
    border-radius:7px;
    padding:8px 11px;
    cursor:pointer;
    font-size:13px;
}

button:hover{
    background:#4b5563;
}

button:active{
    transform:translateY(1px);
}

#stats{
    display:flex;
    gap:8px;
    padding:6px 9px;
    background:#111827;
    border-bottom:1px solid #1f2937;
    flex-wrap:wrap;
    font-size:13px;
}

.stat{
    background:#1f2937;
    border:1px solid #374151;
    border-radius:6px;
    padding:4px 7px;
}

#gameWrap{
    position:relative;
    flex:1;
    min-height:0;
    overflow:hidden;
}

#game{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    display:block;
    image-rendering:pixelated;
    image-rendering:crisp-edges;
    cursor:crosshair;
}

#terrainBadge,
#obbyBadge{
    position:absolute;
    left:50%;
    transform:translateX(-50%);
    z-index:5;
    padding:5px 10px;
    border-radius:6px;
    background:rgba(0,0,0,.5);
    font-size:12px;
    pointer-events:none;
}

#terrainBadge{
    top:9px;
}

#obbyBadge{
    top:40px;
    display:none;
}

#status{
    position:absolute;
    right:9px;
    bottom:9px;
    z-index:7;
    padding:6px 9px;
    border-radius:6px;
    background:rgba(0,0,0,.5);
    font-size:12px;
    pointer-events:none;
}

#hint{
    position:absolute;
    left:9px;
    bottom:9px;
    z-index:5;
    max-width:calc(100% - 18px);
    padding:7px 9px;
    border-radius:6px;
    background:rgba(0,0,0,.55);
    font-size:12px;
    pointer-events:none;
}

#hotbar{
    position:absolute;
    left:50%;
    bottom:8px;
    transform:translateX(-50%);
    z-index:8;
    display:flex;
    gap:4px;
    pointer-events:none;
}

.slot{
    width:48px;
    height:48px;
    position:relative;
    display:flex;
    align-items:center;
    justify-content:center;
    background:rgba(25,25,25,.78);
    border:2px solid rgba(255,255,255,.35);
    border-radius:6px;
}

.slot.sel{
    border-color:#fff;
}

.slotIcon{
    font-size:20px;
}

.slotCount{
    position:absolute;
    right:3px;
    bottom:2px;
    font-size:10px;
}

#panel{
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    width:min(920px,92vw);
    max-height:90%;
    overflow:auto;
    z-index:30;
    padding:14px;
    border:1px solid #4b5563;
    border-radius:12px;
    background:#111827;
    box-shadow:0 16px 50px rgba(0,0,0,.5);
    display:none;
}

#panelTitle{
    font-size:20px;
    font-weight:700;
    margin-bottom:12px;
}

#panelGrid{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(155px,1fr));
    gap:8px;
}

.card{
    padding:9px;
    border:1px solid #374151;
    border-radius:8px;
    background:#1f2937;
}

.card small{
    display:block;
    color:#9ca3af;
    margin-top:4px;
}

.itemRow{
    display:flex;
    justify-content:space-between;
    gap:8px;
}

.equip{
    display:grid;
    grid-template-columns:repeat(9,48px);
    gap:5px;
    margin:10px 0;
}

.eSlot{
    width:48px;
    height:48px;
    position:relative;
    display:flex;
    align-items:center;
    justify-content:center;
    border:1px solid #4b5563;
    border-radius:6px;
    background:#0f172a;
}

.eSlot small{
    position:absolute;
    right:2px;
    bottom:2px;
    font-size:9px;
}

.eSlot button{
    position:absolute;
    right:-7px;
    top:-7px;
    padding:0 5px;
    line-height:16px;
    border-radius:50%;
}

.recipe{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:10px;
    margin-bottom:7px;
    padding:9px;
    border:1px solid #374151;
    border-radius:8px;
    background:#1f2937;
}

.recipeTitle{
    font-weight:700;
}

.recipeMats{
    font-size:12px;
    color:#cbd5e1;
    margin-top:3px;
}

.terrainGrid{
    display:grid;
    grid-template-columns:repeat(4,minmax(120px,1fr));
    gap:9px;
}

.terrainButton{
    min-height:84px;
}

.terrainButton small{
    display:block;
    color:#d1d5db;
    font-size:11px;
    margin-top:4px;
}

.obbyBox{
    padding:14px;
    border:1px solid #374151;
    border-radius:9px;
    background:#1f2937;
}

.obbyStats{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:8px;
    margin:10px 0;
}

.obbyStat{
    padding:9px;
    text-align:center;
    border:1px solid #374151;
    border-radius:7px;
    background:#0f172a;
}

.tiny{
    color:#9ca3af;
    font-size:11px;
    margin-top:3px;
}

#avatarLayout{
    display:flex;
    gap:18px;
    align-items:flex-start;
    flex-wrap:wrap;
}

#avatarEditor{
    width:480px;
    height:960px;
    flex:none;
    image-rendering:pixelated;
    touch-action:none;
    cursor:crosshair;
}

#avatarTools{
    display:flex;
    flex-wrap:wrap;
    gap:6px;
    margin-bottom:10px;
}

#avatarTools button.active{
    outline:2px solid #fff;
}

#palette{
    display:grid;
    grid-template-columns:repeat(5,34px);
    gap:6px;
    max-height:320px;
    overflow:auto;
}

.sw{
    width:34px;
    height:34px;
    padding:0;
    border:2px solid #e5e7eb;
    border-radius:5px;
}

#avatarNote{
    max-width:300px;
    color:#9ca3af;
    font-size:12px;
    margin-bottom:10px;
}

@media(max-width:720px){

    .slot{
        width:39px;
        height:39px;
    }

    .equip{
        grid-template-columns:repeat(9,40px);
    }

    .eSlot{
        width:40px;
        height:40px;
    }

    .terrainGrid{
        grid-template-columns:repeat(2,1fr);
    }

    .obbyStats{
        grid-template-columns:repeat(2,1fr);
    }

    #avatarEditor{
        width:360px;
        height:720px;
    }
}
</style>
</head>

<body>

<div id="root">

    <div id="topbar">

        <button id="invBtn">Inventory (E)</button>
        <button id="craftBtn">Craft (C)</button>
        <button id="avatarBtn">Avatar</button>
        <button id="terrainBtn">Terrain</button>
        <button id="obbyBtn">Mini Games</button>
        <button id="viewBtn">View: 3rd person (V)</button>
        <button id="resetBtn">New World</button>

    </div>


    <div id="stats">

        <div class="stat">
            ❤️ Health:
            <span id="healthText">100</span>/100
        </div>

        <div class="stat">
            🍗 Hunger:
            <span id="hungerText">100</span>/100
        </div>

        <div class="stat">
            Selected:
            <span id="selectedText">empty</span>
        </div>

        <div class="stat">
            Tool:
            <span id="toolText">fist</span>
        </div>

        <div class="stat">
            Terrain:
            <span id="terrainText">Plain</span>
        </div>

    </div>


    <div id="gameWrap">

        <canvas id="game"></canvas>

        <div id="terrainBadge">Plain</div>
        <div id="obbyBadge">OBBY</div>

        <div id="hotbar"></div>

        <div id="hint">
            A/D move • W/Space jump/swim •
            Left click mine/attack/eat •
            Right click place/use •
            1–9 hotbar • E inventory •
            C crafting • V view
        </div>

        <div id="status"></div>

        <div id="panel">

            <div id="panelTitle"></div>

            <div id="panelBody"></div>

        </div>

    </div>

</div>


<script>
(() => {

"use strict";


/* =========================================================
   CANVAS
   ========================================================= */

const canvas =
    document.getElementById("game");

const ctx =
    canvas.getContext("2d");

const buffer =
    document.createElement("canvas");

const bctx =
    buffer.getContext("2d");

ctx.imageSmoothingEnabled=false;
bctx.imageSmoothingEnabled=false;


/* =========================================================
   CONSTANTS
   ========================================================= */

const WORLD_W=220;
const WORLD_H=65;
const TILE=44;

const AIR=0;
const GRASS=1;
const DIRT=2;
const SAND=3;
const LEAVES=4;
const WOOD=5;
const STONE=6;
const GOLD=7;
const DIAMOND=8;
const WATER=9;
const COAL=10;
const TORCH=11;
const LADDER=12;
const SNOW=13;


/* =========================================================
   BLOCK DATA
   ========================================================= */

const BLOCK_HARDNESS={

    [GRASS]:250,
    [DIRT]:280,
    [SAND]:220,
    [LEAVES]:100,
    [WOOD]:700,
    [COAL]:850,
    [STONE]:1100,
    [GOLD]:1500,
    [DIAMOND]:1900,
    [TORCH]:80,
    [LADDER]:80

};


const TOOL_SPEED={

    wood_pickaxe:1.9,
    stone_pickaxe:2.6,
    gold_pickaxe:3.1,
    diamond_pickaxe:3.8

};


const PLACE_BLOCK={

    dirt:DIRT,
    stone:STONE,
    sand:SAND,
    wood:WOOD,
    leaves:LEAVES,
    coal:COAL,
    gold:GOLD,
    diamond:DIAMOND,
    torch:TORCH,
    ladder:LADDER

};


const DROP_ITEM={

    [GRASS]:"dirt",
    [DIRT]:"dirt",
    [SAND]:"sand",
    [LEAVES]:"leaves",
    [WOOD]:"wood",
    [STONE]:"stone",
    [COAL]:"coal",
    [GOLD]:"gold",
    [DIAMOND]:"diamond",
    [TORCH]:"torch",
    [LADDER]:"ladder"

};


/* =========================================================
   INVENTORY
   ========================================================= */

const inv={

    dirt:40,
    stone:10,
    sand:20,
    wood:10,

    leaves:0,
    gold:0,
    diamond:0,
    coal:4,

    ladder:0,

    bucket:1,
    water_bucket:0,

    torch:0,

    apple:0,
    golden_apple:0,
    pork:0,

    wool:0,
    leather:0,
    feather:0,

    wood_pickaxe:1,
    stone_pickaxe:0,
    gold_pickaxe:0,
    diamond_pickaxe:0,

    wood_sword:1,
    stone_sword:0,
    diamond_sword:0

};


const hotbar =
    Array(9).fill(null);


const ITEM_ICONS={

    dirt:"🟫",
    stone:"⬜",
    sand:"🟨",
    wood:"🪵",
    leaves:"🌿",
    gold:"🟨",
    diamond:"🔷",
    coal:"⚫",

    ladder:"🪜",
    bucket:"🪣",
    water_bucket:"💧",
    torch:"🔦",

    apple:"🍎",
    golden_apple:"🍏",
    pork:"🥩",

    wool:"⬜",
    leather:"🟤",
    feather:"🪶",

    wood_pickaxe:"⛏️",
    stone_pickaxe:"⛏️",
    gold_pickaxe:"⛏️",
    diamond_pickaxe:"⛏️",

    wood_sword:"🗡️",
    stone_sword:"🗡️",
    diamond_sword:"🗡️"

};


/* =========================================================
   RECIPES
   ========================================================= */

const recipes=[

    {
        item:"wood_pickaxe",
        count:1,
        mats:{wood:3},
        name:"Wood Pickaxe"
    },

    {
        item:"stone_pickaxe",
        count:1,
        mats:{
            wood:1,
            stone:3
        },
        name:"Stone Pickaxe"
    },

    {
        item:"gold_pickaxe",
        count:1,
        mats:{
            wood:1,
            gold:3
        },
        name:"Gold Pickaxe"
    },

    {
        item:"diamond_pickaxe",
        count:1,
        mats:{
            wood:1,
            diamond:3
        },
        name:"Diamond Pickaxe"
    },

    {
        item:"wood_sword",
        count:1,
        mats:{wood:2},
        name:"Wood Sword"
    },

    {
        item:"stone_sword",
        count:1,
        mats:{
            wood:1,
            stone:2
        },
        name:"Stone Sword"
    },

    {
        item:"diamond_sword",
        count:1,
        mats:{
            wood:1,
            diamond:2
        },
        name:"Diamond Sword"
    },

    {
        item:"ladder",
        count:3,
        mats:{wood:3},
        name:"Ladder ×3"
    },

    {
        item:"torch",
        count:4,
        mats:{
            coal:1,
            wood:1
        },
        name:"Torch ×4"
    }

];


/* =========================================================
   PLAYER
   ========================================================= */

const player={

    x:12,
    y:20,

    vx:0,
    vy:0,

    w:.72,
    h:1.82,

    onGround:false,

    health:100,
    hunger:100,

    facing:1,

    anim:0

};


/* =========================================================
   WORLD STATE
   ========================================================= */

let world=[];
let waterLevel=[];
let waterSources=new Set();

let animals=[];
let particles=[];
let confetti=[];

let terrainType="plain";
let worldSeed=Date.now();

let cameraX=14;
let cameraY=28;

let selectedSlot=0;

let viewFirst=false;

let breaking=null;

let attackReadyAt=0;

let panelMode="";

let animationTime=0;
let lastTime=performance.now();

let hungerTimer=0;
let waterTimer=0;

let keys={};


/* =========================================================
   AVATAR STATE
   ========================================================= */

let avatarGrid=[];
let avatarColor="#d79b72";

let avatarEditing=false;

let avatarTool="pencil";

let avatarHistory=[];
let avatarRedo=[];

let avatarDrawing=false;
let avatarStrokeSaved=false;


/* =========================================================
   OBBY STATE
   ========================================================= */

let obbyActive=false;
let obbyWon=false;

let obbyDeaths=0;
let obbyCoinCount=0;

let obbyCheckpoint=0;

let obbySpeedTimer=0;
let obbyBounceTimer=0;


/* =========================================================
   OBBY COURSE
   ========================================================= */

const obbyPlatforms=[

    {x:2,y:30,w:9},
    {x:12,y:29,w:8},
    {x:22,y:27,w:8},
    {x:32,y:29,w:9},
    {x:43,y:27,w:8},
    {x:53,y:25,w:9},
    {x:64,y:27,w:8},
    {x:74,y:24,w:9},
    {x:85,y:26,w:9},
    {x:96,y:23,w:9},
    {x:107,y:21,w:11}

];


const obbyFinish={

    x:119,
    y:19,
    w:10

};


const obbyCoinItems=[

    {x:15,y:26.3,collected:false},
    {x:25,y:24.3,collected:false},
    {x:36,y:26.3,collected:false},
    {x:47,y:24.3,collected:false},
    {x:57,y:22.3,collected:false},
    {x:68,y:24.3,collected:false},
    {x:78,y:21.3,collected:false},
    {x:89,y:23.3,collected:false},
    {x:100,y:20.3,collected:false},
    {x:111,y:18.3,collected:false}

];


const obbyCheckpoints=[

    {
        x:41,
        y:27.3,
        activated:false
    },

    {
        x:75,
        y:23.3,
        activated:false
    },

    {
        x:108,
        y:20.3,
        activated:false
    }

];


const obbyBouncePads=[

    {x:27,y:26.7},
    {x:57,y:24.7},
    {x:89,y:25.7}

];


const obbySpeedPads=[

    {x:47,y:26.7},
    {x:101,y:22.7}

];


const obbyMysteryBlocks=[

    {x:19,y:28,used:false},
    {x:70,y:26,used:false},
    {x:101,y:20,used:false}

];


/* =========================================================
   HELPERS
   ========================================================= */

function clamp(
    value,
    min,
    max
){

    return Math.max(
        min,
        Math.min(max,value)
    );

}


function inBounds(
    x,
    y
){

    return (
        x>=0 &&
        x<WORLD_W &&
        y>=0 &&
        y<WORLD_H
    );

}


function gridKey(
    x,
    y
){

    return x+","+y;

}


function getBlock(
    x,
    y
){

    if(
        !inBounds(x,y)
    ){

        return STONE;

    }

    return world[y][x] || AIR;

}


function setBlock(
    x,
    y,
    block
){

    if(
        inBounds(x,y)
    ){

        world[y][x]=block;

    }

}


function isSolidBlock(
    block
){

    return (
        block!==AIR &&
        block!==WATER &&
        block!==TORCH &&
        block!==LADDER
    );

}


function rectHitsSolid(
    x,
    y,
    w,
    h
){

    const left=
        Math.floor(x);

    const right=
        Math.floor(
            x+w-.001
        );

    const top=
        Math.floor(y);

    const bottom=
        Math.floor(
            y+h-.001
        );


    for(
        let yy=top;
        yy<=bottom;
        yy++
    ){

        for(
            let xx=left;
            xx<=right;
            xx++
        ){

            if(
                isSolidBlock(
                    getBlock(
                        xx,
                        yy
                    )
                )
            ){

                return true;

            }

        }

    }


    return false;

}


function worldToScreenX(
    x
){

    return (
        x-
        cameraX
    )*
    TILE+
    canvas.width/2;

}


function worldToScreenY(
    y
){

    return (
        y-
        cameraY
    )*
    TILE+
    canvas.height/2;

}


function countItem(
    item
){

    return inv[item] || 0;

}


function selectedItem(){

    return hotbar[
        selectedSlot
    ] || null;

}


function selectedTool(){

    const item=
        selectedItem();


    return (
        item &&
        TOOL_SPEED[item]
    )
    ?item
    :"fist";

}


function showStatus(
    text
){

    const element=
        document.getElementById(
            "status"
        );


    element.textContent=
        text;


    clearTimeout(
        showStatus.timer
    );


    showStatus.timer=
        setTimeout(
            () => {

                element.textContent="";

            },
            1900
        );

}


/* =========================================================
   TERRAIN
   ========================================================= */

function terrainName(){

    if(
        terrainType==="snow"
    ){

        return "Snow";

    }


    if(
        terrainType==="mountain"
    ){

        return "Mountain";

    }


    if(
        terrainType==="abyss"
    ){

        return "Abyss";

    }


    return "Plain";

}


function surfaceY(
    x
){

    if(
        terrainType==="mountain"
    ){

        const a=
            Math.abs(
                Math.sin(
                    x*.065
                )
            );


        const b=
            Math.abs(
                Math.sin(
                    x*.021+1.2
                )
            );


        return clamp(
            Math.floor(
                31-
                Math.pow(
                    a,
                    1.7
                )*
                15-
                b*
                7
            ),
            8,
            31
        );

    }


    if(
        terrainType==="snow"
    ){

        return clamp(
            Math.floor(
                27+
                Math.sin(x*.07)*2+
                Math.sin(x*.024)*3
            ),
            21,
            31
        );

    }


    if(
        terrainType==="abyss"
    ){

        return Math.floor(
            29+
            Math.sin(x*.08)*2.5
        );

    }


    return Math.floor(
        27+
        Math.sin(x*.10)*1.5+
        Math.sin(x*.032)*2.1
    );

}


function findGroundY(
    x
){

    x=
        Math.floor(x);


    for(
        let y=0;
        y<WORLD_H;
        y++
    ){

        if(
            isSolidBlock(
                getBlock(x,y)
            )
        ){

            return y;

        }

    }


    return WORLD_H-1;

}


/* =========================================================
   RNG
   ========================================================= */

function mulberry32(
    seed
){

    return function(){

        let t=
            seed+=
            0x6D2B79F5;


        t=
            Math.imul(
                t^t>>>15,
                t|1
            );


        t^=
            t+
            Math.imul(
                t^t>>>7,
                t|61
            );


        return (
            (t^t>>>14)>>>0
        )/
        4294967296;

    };

}


/* =========================================================
   WORLD GENERATION
   ========================================================= */

function clearWorld(){

    world=
        Array.from(
            {
                length:WORLD_H
            },
            () =>
                Array(
                    WORLD_W
                ).fill(AIR)
        );


    waterLevel=
        Array.from(
            {
                length:WORLD_H
            },
            () =>
                Array(
                    WORLD_W
                ).fill(0)
        );


    waterSources.clear();

    animals=[];

    particles=[];

    breaking=null;

}


function addWaterPool(
    left,
    right,
    top
){

    for(
        let x=left;
        x<=right;
        x++
    ){

        for(
            let y=top;
            y<top+5;
            y++
        ){

            if(
                inBounds(x,y) &&
                getBlock(x,y)===AIR
            ){

                setBlock(
                    x,
                    y,
                    WATER
                );


                waterLevel[y][x]=8;


                waterSources.add(
                    gridKey(x,y)
                );

            }

        }

    }

}


function addTree(
    x
){

    const ground=
        findGroundY(x);


    if(
        ground<7
    ){

        return;

    }


    for(
        let i=1;
        i<=4;
        i++
    ){

        setBlock(
            x,
            ground-i,
            WOOD
        );

    }


    for(
        let dx=-2;
        dx<=2;
        dx++
    ){

        for(
            let dy=-2;
            dy<=2;
            dy++
        ){

            if(
                Math.abs(dx)+
                Math.abs(dy)<=3 &&
                getBlock(
                    x+dx,
                    ground-4+dy
                )===AIR
            ){

                setBlock(
                    x+dx,
                    ground-4+dy,
                    LEAVES
                );

            }

        }

    }

}


function generateWorld(){

    clearWorld();


    const rnd=
        mulberry32(
            worldSeed>>>0
        );


    for(
        let x=0;
        x<WORLD_W;
        x++
    ){

        const ground=
            surfaceY(x);


        for(
            let y=ground;
            y<WORLD_H;
            y++
        ){

            if(
                terrainType==="mountain"
            ){

                world[y][x]=
                    (
                        y===ground &&
                        ground<=16
                    )
                    ?SNOW
                    :STONE;

            }

            else if(
                terrainType==="snow"
            ){

                world[y][x]=
                    y===ground
                    ?SNOW
                    :(
                        y<ground+4
                        ?DIRT
                        :STONE
                    );

            }

            else{

                world[y][x]=
                    y===ground
                    ?(
                        terrainType==="abyss"
                        ?STONE
                        :GRASS
                    )
                    :(
                        y<ground+4
                        ?DIRT
                        :STONE
                    );

            }

        }

    }


    if(
        terrainType==="abyss"
    ){

        const gaps=[

            [20,28],
            [47,55],
            [77,85],
            [108,118],
            [140,148],
            [171,180],
            [199,208]

        ];


        for(
            const gap of gaps
        ){

            for(
                let x=gap[0];
                x<=gap[1];
                x++
            ){

                const ground=
                    surfaceY(x);


                for(
                    let y=ground;
                    y<WORLD_H;
                    y++
                ){

                    world[y][x]=AIR;

                }

            }

        }

    }


    if(
        terrainType!=="abyss"
    ){

        addWaterPool(
            100,
            129,
            24
        );


        addWaterPool(
            51,
            57,
            25
        );


        addWaterPool(
            149,
            156,
            25
        );

    }


    if(
        terrainType==="plain" ||
        terrainType==="snow"
    ){

        [
            18,
            39,
            66,
            93,
            121,
            160,
            181,
            204
        ].forEach(
            addTree
        );

    }


    if(
        terrainType==="mountain"
    ){

        for(
            let x=0;
            x<WORLD_W;
            x++
        ){

            const ground=
                surfaceY(x);


            if(
                ground<20
            ){

                for(
                    let y=ground+1;
                    y<
                        Math.min(
                            ground+5,
                            WORLD_H
                        );
                    y++
                ){

                    world[y][x]=STONE;

                }

            }

        }

    }


    for(
        let y=32;
        y<WORLD_H-2;
        y++
    ){

        for(
            let x=1;
            x<WORLD_W-1;
            x++
        ){

            if(
                getBlock(x,y)!==STONE
            ){

                continue;

            }


            const r=
                rnd();


            if(
                r<.020
            ){

                world[y][x]=COAL;

            }

            else if(
                r<.026
            ){

                world[y][x]=GOLD;

            }

            else if(
                r<.029
            ){

                world[y][x]=DIAMOND;

            }

        }

    }


    player.x=12;


    player.y=
        findGroundY(12)-
        player.h;


    player.vx=0;
    player.vy=0;

    player.onGround=true;


    player.health=100;
    player.hunger=100;


    cameraX=
        player.x+
        player.w/2;


    cameraY=
        player.y+
        player.h/2;


    spawnAnimals();


    updateTerrainUI();

    renderStats();

    renderHotbar();

}


/* =========================================================
   ANIMALS
   ========================================================= */

function makeAnimal(
    type,
    x,
    y
){

    const size=
        type==="chicken"
        ?{
            w:.65,
            h:.72
        }
        :{
            w:.86,
            h:.86
        };


    return {

        type,

        x,
        y,

        w:size.w,
        h:size.h,

        vx:0,
        vy:0,

        dir:
            Math.random()<.5
            ?-1
            :1,

        wander:
            1+
            Math.random()*2,

        anim:
            Math.random()*
            Math.PI*2,

        health:30

    };

}


function spawnAnimals(){

    animals=[];


    const types=[
        "pig",
        "sheep",
        "cow",
        "chicken"
    ];


    for(
        let i=0;
        i<18;
        i++
    ){

        const x=
            7+
            Math.floor(
                Math.random()*
                (WORLD_W-14)
            );


        const ground=
            findGroundY(x);


        const type=
            types[
                i%4
            ];


        const height=
            type==="chicken"
            ?.72
            :.86;


        if(
            ground>4 &&
            getBlock(
                x,
                ground-1
            )===AIR &&
            Math.abs(
                x-player.x
            )>4
        ){

            animals.push(
                makeAnimal(
                    type,
                    x+.05,
                    ground-height
                )
            );

        }

    }

}


function moveEntity(
    entity,
    dt,
    gravity
){

    entity.onGround=false;


    const nx=
        entity.x+
        entity.vx*
        dt;


    if(
        !rectHitsSolid(
            nx,
            entity.y,
            entity.w,
            entity.h
        )
    ){

        entity.x=nx;

    }

    else{

        entity.vx=0;

    }


    entity.vy+=
        gravity*
        dt;


    const ny=
        entity.y+
        entity.vy*
        dt;


    if(
        !rectHitsSolid(
            entity.x,
            ny,
            entity.w,
            entity.h
        )
    ){

        entity.y=ny;

    }

    else{

        if(
            entity.vy>0
        ){

            const floor=
                Math.floor(
                    ny+
                    entity.h
                );


            entity.y=
                floor-
                entity.h;


            entity.onGround=true;

        }

        else if(
            entity.vy<0
        ){

            const ceiling=
                Math.floor(ny);


            entity.y=
                ceiling+
                1;

        }


        entity.vy=0;

    }


    entity.x=
        clamp(
            entity.x,
            .1,
            WORLD_W-
            entity.w-
            .1
        );

}


function animalInWater(
    animal
){

    return (
        getBlock(
            Math.floor(
                animal.x+
                animal.w/2
            ),
            Math.floor(
                animal.y+
                animal.h*.55
            )
        )===WATER
    );

}


function updateAnimals(
    dt
){

    if(
        obbyActive
    ){

        return;

    }


    for(
        const animal of animals
    ){

        try{

            const swimming=
                animalInWater(
                    animal
                );


            if(
                swimming
            ){

                animal.vy+=
                    (
                        -1-
                        animal.vy
                    )*.10;


                animal.vx+=
                    (
                        animal.dir*.35-
                        animal.vx
                    )*.06;

            }

            else{

                animal.wander-=dt;


                if(
                    animal.wander<=0
                ){

                    animal.wander=
                        1+
                        Math.random()*2;


                    animal.dir=
                        Math.random()<.5
                        ?-1
                        :1;

                }


                animal.vx+=
                    (
                        animal.dir*.65-
                        animal.vx
                    )*.08;

            }


            animal.vx=
                clamp(
                    animal.vx,
                    -1.2,
                    1.2
                );


            moveEntity(
                animal,
                dt,
                swimming
                ?2.2
                :13
            );


            animal.anim+=
                dt*
                (
                    Math.abs(
                        animal.vx
                    )>.04
                    ?10
                    :2
                );

        }

        catch(_){

            animal.vx=0;


            const ground=
                findGroundY(
                    animal.x
                );


            if(
                animal.y>
                ground-
                animal.h
            ){

                animal.y=
                    ground-
                    animal.h;

            }


            animal.vy=0;

        }

    }

}


/* =========================================================
   PLAYER MOVEMENT
   ========================================================= */

function playerInWater(){

    return (
        getBlock(
            Math.floor(
                player.x+
                player.w/2
            ),
            Math.floor(
                player.y+
                player.h*.55
            )
        )===WATER
    );

}


function updatePlayer(
    dt
){

    if(
        obbyActive
    ){

        updateObby(
            dt
        );


        return;

    }


    const direction=
        (
            keys.a
            ?-1
            :0
        )+
        (
            keys.d
            ?1
            :0
        );


    const swimming=
        playerInWater();


    const target=
        direction*
        5.2;


    player.vx+=
        (
            target-
            player.vx
        )*
        (
            swimming
            ?.9
            :.22
        )*
        dt;


    if(
        direction===0
    ){

        player.vx*=
            swimming
            ?.97
            :.80;

    }


    if(
        direction!==0
    ){

        player.facing=
            direction;

    }


    if(
        swimming
    ){

        player.vy+=
            5.5*
            dt;


        if(
            keys.w ||
            keys[" "]
        ){

            player.vy=
                -4.4;

        }


        const nx=
            player.x+
            player.vx*
            dt;


        if(
            !rectHitsSolid(
                nx,
                player.y,
                player.w,
                player.h
            )
        ){

            player.x=nx;

        }


        const ny=
            player.y+
            player.vy*
            dt;


        if(
            !rectHitsSolid(
                player.x,
                ny,
                player.w,
                player.h
            )
        ){

            player.y=ny;

        }

    }

    else{

        if(
            (
                keys.w ||
                keys[" "]
            ) &&
            player.onGround
        ){

            player.vy=
                -7.2;


            player.onGround=false;

        }


        moveEntity(
            player,
            dt,
            16
        );

    }


    player.anim+=
        dt*
        (
            Math.abs(
                player.vx
            )>.08
            ?10
            :2
        );


    if(
        player.y>
        WORLD_H+2
    ){

        player.x=12;


        player.y=
            findGroundY(12)-
            player.h;


        player.vx=0;
        player.vy=0;

    }

}


/* =========================================================
   OBBY
   ========================================================= */

function resetObby(){

    obbyWon=false;
    obbyDeaths=0;
    obbyCoinCount=0;
    obbyCheckpoint=0;

    obbySpeedTimer=0;
    obbyBounceTimer=0;


    obbyCoinItems.forEach(
        coin =>
            coin.collected=false
    );


    obbyCheckpoints.forEach(
        point =>
            point.activated=false
    );


    obbyMysteryBlocks.forEach(
        block =>
            block.used=false
    );

}


function openObbyPanel(){

    panelMode="obby";


    showPanel(
        "Mini Games — Obby"
    );


    const body=
        document.getElementById(
            "panelBody"
        );


    body.innerHTML=
        `
        <div class="obbyBox">

            <b>
                Parkour Obby
            </b>

            <p>
                Jump across the platforms,
                collect coins, use checkpoints,
                hit bounce pads and discover
                mystery blocks.
            </p>

            <div class="obbyStats">

                <div class="obbyStat">
                    <b>${obbyDeaths}</b>
                    <div class="tiny">
                        Deaths
                    </div>
                </div>

                <div class="obbyStat">
                    <b>${obbyCoinCount}</b>
                    <div class="tiny">
                        Coins
                    </div>
                </div>

                <div class="obbyStat">
                    <b>${obbyCheckpoint}</b>
                    <div class="tiny">
                        Checkpoint
                    </div>
                </div>

                <div class="obbyStat">
                    <b>
                        ${
                            obbyWon
                            ?"DONE"
                            :"READY"
                        }
                    </b>
                    <div class="tiny">
                        Status
                    </div>
                </div>

            </div>

            <button id="joinObbyButton">
                ${
                    obbyActive
                    ?"Restart Obby"
                    :"Join Obby"
                }
            </button>

            ${
                obbyActive
                ?`
                    <button
                        id="leaveObbyButton"
                        style="margin-left:6px"
                    >
                        Leave Obby
                    </button>
                `
                :""
            }

        </div>
        `;


    document.getElementById(
        "joinObbyButton"
    ).onclick=
        () =>
            joinObby();


    const leave=
        document.getElementById(
            "leaveObbyButton"
        );


    if(
        leave
    ){

        leave.onclick=
            () => {

                leaveObby();

                hidePanel();

            };

    }

}


function joinObby(){

    resetObby();


    obbyActive=true;


    const start=
        obbyPlatforms[0];


    player.x=
        start.x+
        .7;


    player.y=
        start.y-
        player.h;


    player.vx=0;
    player.vy=0;


    player.onGround=true;


    cameraX=
        player.x+
        player.w/2;


    cameraY=
        player.y+
        player.h/2;


    document.getElementById(
        "obbyBadge"
    ).style.display=
        "block";


    document.getElementById(
        "terrainBadge"
    ).textContent=
        "OBBY";


    hidePanel();


    showStatus(
        "Obby started!"
    );

}


function respawnObby(){

    let base;


    if(
        obbyCheckpoint===0
    ){

        base=
            obbyPlatforms[0];

    }else if(
        obbyCheckpoint===1
    ){

        base=
            obbyPlatforms[3];

    }else if(
        obbyCheckpoint===2
    ){

        base=
            obbyPlatforms[6];

    }else{

        base=
            obbyPlatforms[9];

    }


    player.x=
        base.x+
        .6;


    player.y=
        base.y-
        player.h;


    player.vx=0;
    player.vy=0;


    player.onGround=true;


    cameraX=
        player.x+
        player.w/2;


    cameraY=
        player.y+
        player.h/2;


    showStatus(
        "Respawned at checkpoint"
    );

}


function leaveObby(){

    obbyActive=false;
    obbyWon=false;


    document.getElementById(
        "obbyBadge"
    ).style.display=
        "none";


    player.x=12;


    player.y=
        findGroundY(12)-
        player.h;


    player.vx=0;
    player.vy=0;


    player.onGround=true;


    cameraX=
        player.x+
        player.w/2;


    cameraY=
        player.y+
        player.h/2;


    updateTerrainUI();

}


function updateObby(
    dt
){

    if(
        obbySpeedTimer>0
    ){

        obbySpeedTimer-=dt;

    }


    if(
        obbyBounceTimer>0
    ){

        obbyBounceTimer-=dt;

    }


    const direction=
        (
            keys.a
            ?-1
            :0
        )+
        (
            keys.d
            ?1
            :0
        );


    const speed=
        obbySpeedTimer>0
        ?8.5
        :6.2;


    player.vx+=
        (
            direction*
            speed-
            player.vx
        )*.18;


    if(
        direction===0
    ){

        player.vx*=.82;

    }


    if(
        direction!==0
    ){

        player.facing=
            direction;

    }


    if(
        (
            keys.w ||
            keys[" "]
        ) &&
        player.onGround
    ){

        player.vy=
            obbyBounceTimer>0
            ?-11.5
            :-8.4;


        player.onGround=false;

    }


    player.vy+=
        18*
        dt;


    player.x+=
        player.vx*
        dt;


    player.x=
        clamp(
            player.x,
            1,
            obbyFinish.x+
            obbyFinish.w
        );


    const oldBottom=
        player.y+
        player.h;


    const nextY=
        player.y+
        player.vy*
        dt;


    const nextBottom=
        nextY+
        player.h;


    let landed=false;


    if(
        player.vy>=0
    ){

        for(
            const platform of
            obbyPlatforms
        ){

            if(
                nextBottom>=
                platform.y &&
                oldBottom<=
                platform.y &&
                player.x+
                player.w>
                platform.x &&
                player.x<
                platform.x+
                platform.w
            ){

                player.y=
                    platform.y-
                    player.h;


                player.vy=0;


                player.onGround=true;


                landed=true;


                break;

            }

        }


        if(
            !landed &&
            nextBottom>=
            obbyFinish.y &&
            oldBottom<=
            obbyFinish.y &&
            player.x+
            player.w>
            obbyFinish.x &&
            player.x<
            obbyFinish.x+
            obbyFinish.w
        ){

            player.y=
                obbyFinish.y-
                player.h;


            player.vy=0;

            player.onGround=true;

            landed=true;

        }

    }


    if(
        !landed
    ){

        player.y=
            nextY;


        player.onGround=false;

    }


    if(
        landed
    ){

        for(
            let i=0;
            i<obbyCheckpoints.length;
            i++
        ){

            const checkpoint=
                obbyCheckpoints[i];


            if(
                player.x+
                player.w>
                checkpoint.x &&
                player.x<
                checkpoint.x+
                2 &&
                Math.abs(
                    player.y-
                    (
                        checkpoint.y-
                        player.h
                    )
                )<
                1.5 &&
                !checkpoint.activated
            ){

                checkpoint.activated=true;


                obbyCheckpoint=
                    i+1;


                burstConfetti(
                    12,
                    false
                );


                showStatus(
                    "Checkpoint reached! ✅"
                );

            }

        }


        for(
            const pad of
            obbyBouncePads
        ){

            if(
                player.x+
                player.w>
                pad.x &&
                player.x<
                pad.x+
                1.3
            ){

                player.vy=
                    -11.5;


                player.onGround=false;


                obbyBounceTimer=.7;


                burstConfetti(
                    7,
                    false
                );


                showStatus(
                    "BOING! 🚀"
                );

            }

        }


        for(
            const pad of
            obbySpeedPads
        ){

            if(
                player.x+
                player.w>
                pad.x &&
                player.x<
                pad.x+
                1.5
            ){

                obbySpeedTimer=4;


                showStatus(
                    "SPEED BOOST! ⚡"
                );

            }

        }


        for(
            const block of
            obbyMysteryBlocks
        ){

            if(
                !block.used &&
                player.x+
                player.w>
                block.x &&
                player.x<
                block.x+
                1.2
            ){

                activateMystery(
                    block
                );

            }

        }

    }


    for(
        const coin of
        obbyCoinItems
    ){

        if(
            !coin.collected &&
            Math.hypot(
                player.x-
                coin.x,
                player.y-
                coin.y
            )<1.05
        ){

            coin.collected=true;


            obbyCoinCount++;


            burstConfetti(
                5,
                false
            );


            showStatus(
                "Coin collected! 🪙"
            );

        }

    }


    if(
        player.x+
        player.w*.65>
        obbyFinish.x &&
        player.x<
        obbyFinish.x+
        obbyFinish.w &&
        player.y+
        player.h>
        obbyFinish.y-
        .8
    ){

        winObby();

    }


    if(
        player.y>42
    ){

        obbyDeaths++;


        respawnObby();

    }


    player.anim+=
        dt*
        (
            Math.abs(
                player.vx
            )>.08
            ?10
            :2
        );


    cameraX+=
        (
            player.x+
            player.w/2-
            cameraX
        )*.16;


    cameraY+=
        (
            player.y+
            player.h/2-
            cameraY
        )*.16;


    cameraX=
        clamp(
            cameraX,
            6,
            100
        );


    cameraY=
        clamp(
            cameraY,
            12,
            31
        );

}


function activateMystery(
    block
){

    block.used=true;


    const result=
        Math.floor(
            Math.random()*4
        );


    if(
        result===0
    ){

        obbySpeedTimer=6;


        showStatus(
            "MYSTERY BOOST! ⚡"
        );


        burstConfetti(
            18,
            false
        );

    }

    else if(
        result===1
    ){

        player.vy=
            -12.5;


        obbyBounceTimer=1;


        showStatus(
            "MYSTERY SPRING! 🚀"
        );


        burstConfetti(
            18,
            false
        );

    }

    else if(
        result===2
    ){

        player.x=
            clamp(
                player.x+4,
                1,
                obbyFinish.x
            );


        showStatus(
            "SECRET WARP! ✨"
        );


        burstConfetti(
            22,
            false
        );

    }

    else{

        obbyCoinCount+=3;


        showStatus(
            "TREASURE BONUS! 🪙🪙🪙"
        );


        burstConfetti(
            28,
            false
        );

    }

}


function winObby(){

    if(
        obbyWon
    ){

        return;

    }


    obbyWon=true;


    document.getElementById(
        "obbyBadge"
    ).textContent=
        "OBBY COMPLETE! 🎉";


    burstConfetti(
        70,
        true
    );


    showStatus(
        "YOU FINISHED THE OBBY! 🎉"
    );

}


/* =========================================================
   AVATAR DEFAULT
   ========================================================= */

function makeDefaultAvatar(){

    const g=
        Array.from(
            {
                length:32
            },
            () =>
                Array(16).fill(null)
        );


    const skin="#d79b72";
    const dark="#b97854";
    const hair="#4a3427";
    const shirt="#3f7fca";
    const shirtDark="#2b5e9d";
    const pants="#303845";
    const shoe="#1f242b";
    const eye="#1b2026";
    const white="#ffffff";


    for(
        let y=0;
        y<8;
        y++
    ){

        for(
            let x=4;
            x<12;
            x++
        ){

            g[y][x]=skin;

        }

    }


    for(
        let x=4;
        x<12;
        x++
    ){

        g[0][x]=hair;
        g[1][x]=hair;

    }


    g[2][4]=hair;
    g[2][5]=hair;
    g[2][10]=hair;
    g[2][11]=hair;


    g[4][6]=white;
    g[4][7]=eye;
    g[4][9]=white;
    g[4][10]=eye;


    g[6][7]=dark;
    g[6][8]=dark;


    for(
        let y=8;
        y<20;
        y++
    ){

        for(
            let x=4;
            x<12;
            x++
        ){

            g[y][x]=shirt;

        }

    }


    for(
        let y=9;
        y<19;
        y++
    ){

        g[y][4]=shirtDark;

    }


    for(
        let x=6;
        x<10;
        x++
    ){

        g[8][x]=skin;

    }


    for(
        let y=8;
        y<20;
        y++
    ){

        for(
            let x=0;
            x<4;
            x++
        ){

            g[y][x]=shirt;

        }


        for(
            let x=12;
            x<16;
            x++
        ){

            g[y][x]=shirt;

        }

    }


    for(
        let y=17;
        y<20;
        y++
    ){

        for(
            let x=0;
            x<4;
            x++
        ){

            g[y][x]=skin;

        }


        for(
            let x=12;
            x<16;
            x++
        ){

            g[y][x]=skin;

        }

    }


    for(
        let y=20;
        y<30;
        y++
    ){

        for(
            let x=4;
            x<12;
            x++
        ){

            g[y][x]=pants;

        }

    }


    for(
        let y=30;
        y<32;
        y++
    ){

        for(
            let x=3;
            x<13;
            x++
        ){

            g[y][x]=shoe;

        }

    }


    return g;

}


function loadAvatar(){

    try{

        const raw=
            JSON.parse(
                localStorage.getItem(
                    "paperAvatar"
                ) ||
                "null"
            );


        if(
            !Array.isArray(raw) ||
            raw.length!==32 ||
            !raw.every(
                row =>
                    Array.isArray(row) &&
                    row.length===16
            )
        ){

            throw new Error();

        }


        avatarGrid=
            raw.map(
                row =>
                    row.map(
                        value =>
                            typeof value==="string" &&
                            /^#[0-9a-fA-F]{6}$/.test(value)
                            ?value
                            :null
                    )
            );


        if(
            avatarGrid.flat().filter(Boolean).length<8
        ){

            throw new Error();

        }

    }catch(_){

        avatarGrid=
            makeDefaultAvatar();

    }

}


function cloneAvatar(){

    return avatarGrid.map(
        row =>
            row.slice()
    );

}


function saveAvatarHistory(){

    avatarHistory.push(
        cloneAvatar()
    );


    if(
        avatarHistory.length>60
    ){

        avatarHistory.shift();

    }


    avatarRedo=[];

}


function undoAvatar(){

    if(
        avatarHistory.length===0
    ){

        showStatus(
            "Nothing to undo"
        );


        return;

    }


    avatarRedo.push(
        cloneAvatar()
    );


    avatarGrid=
        avatarHistory.pop();


    drawAvatarEditor();


    showStatus(
        "Undo"
    );

}


function redoAvatar(){

    if(
        avatarRedo.length===0
    ){

        showStatus(
            "Nothing to redo"
        );


        return;

    }


    avatarHistory.push(
        cloneAvatar()
    );


    avatarGrid=
        avatarRedo.pop();


    drawAvatarEditor();


    showStatus(
        "Redo"
    );

}


function normalizeAvatar(){

    const output=
        Array.from(
            {
                length:32
            },
            () =>
                Array(16).fill(null)
        );


    for(
        let y=0;
        y<32;
        y++
    ){

        for(
            let x=0;
            x<16;
            x++
        ){

            const value=
                avatarGrid?.[y]?.[x];


            if(
                typeof value==="string" &&
                /^#[0-9a-fA-F]{6}$/.test(value)
            ){

                output[y][x]=value;

            }

        }

    }


    return output;

}


/* =========================================================
   AVATAR EDITOR
   ========================================================= */

const avatarEditor=
    document.createElement(
        "canvas"
    );


avatarEditor.id=
    "avatarEditor";


avatarEditor.width=480;
avatarEditor.height=960;


function drawAvatarEditor(){

    if(
        !avatarEditing
    ){

        return;

    }


    const ac=
        avatarEditor.getContext(
            "2d"
        );


    ac.imageSmoothingEnabled=false;


    ac.fillStyle="#0b1220";


    ac.fillRect(
        0,
        0,
        480,
        960
    );


    const tileW=30;
    const tileH=30;


    for(
        let y=0;
        y<32;
        y++
    ){

        for(
            let x=0;
            x<16;
            x++
        ){

            ac.fillStyle=
                avatarGrid[y][x] ||
                "#202938";


            ac.fillRect(
                x*tileW,
                y*tileH,
                tileW,
                tileH
            );


            ac.strokeStyle=
                "rgba(255,255,255,.08)";


            ac.strokeRect(
                x*tileW,
                y*tileH,
                tileW,
                tileH
            );

        }

    }

}


function pixelFromPointer(
    event
){

    const rect=
        avatarEditor.getBoundingClientRect();


    return {

        x:
            clamp(
                Math.floor(
                    (
                        event.clientX-
                        rect.left
                    )/
                    (
                        rect.width/16
                    )
                ),
                0,
                15
            ),

        y:
            clamp(
                Math.floor(
                    (
                        event.clientY-
                        rect.top
                    )/
                    (
                        rect.height/32
                    )
                ),
                0,
                31
            )

    };

}


function paintAvatar(
    event
){

    if(
        !avatarEditing
    ){

        return;

    }


    const point=
        pixelFromPointer(
            event
        );


    if(
        avatarTool==="eraser"
    ){

        avatarGrid[
            point.y
        ][
            point.x
        ]=null;

    }else{

        avatarGrid[
            point.y
        ][
            point.x
        ]=
            avatarColor;

    }


    drawAvatarEditor();

}


avatarEditor.addEventListener(
    "pointerdown",
    event => {

        if(
            !avatarEditing
        ){

            return;

        }


        event.preventDefault();


        avatarDrawing=true;


        if(
            !avatarStrokeSaved
        ){

            saveAvatarHistory();

            avatarStrokeSaved=true;

        }


        avatarEditor.setPointerCapture?.(
            event.pointerId
        );


        paintAvatar(event);

    }
);


avatarEditor.addEventListener(
    "pointermove",
    event => {

        if(
            avatarDrawing
        ){

            paintAvatar(event);

        }

    }
);


function endAvatarStroke(){

    avatarDrawing=false;
    avatarStrokeSaved=false;

}


avatarEditor.addEventListener(
    "pointerup",
    endAvatarStroke
);


avatarEditor.addEventListener(
    "pointercancel",
    endAvatarStroke
);


function updateAvatarTools(){

    document
        .querySelectorAll(
            "#avatarTools button"
        )
        .forEach(
            button => {

                button.classList.toggle(
                    "active",
                    button.dataset.tool===
                    avatarTool
                );

            }
        );

}


function openAvatar(){

    panelMode="avatar";
    avatarEditing=true;


    showPanel(
        "Avatar Editor"
    );


    const body=
        document.getElementById(
            "panelBody"
        );


    body.innerHTML="";


    const layout=
        document.createElement(
            "div"
        );


    layout.id=
        "avatarLayout";


    layout.appendChild(
        avatarEditor
    );


    const side=
        document.createElement(
            "div"
        );


    const note=
        document.createElement(
            "div"
        );


    note.id="avatarNote";


    note.textContent=
        "Paint or erase pixels. Drag to draw. Undo and redo work by drawing stroke.";

    
    side.appendChild(
        note
    );


    const tools=
        document.createElement(
            "div"
        );


    tools.id=
        "avatarTools";


    const toolData=[

        {
            id:"pencil",
            text:"🖌️ Pencil"
        },

        {
            id:"eraser",
            text:"🧽 Eraser"
        },

        {
            id:"undo",
            text:"↩️ Undo"
        },

        {
            id:"redo",
            text:"↪️ Redo"
        }

    ];


    for(
        const tool of toolData
    ){

        const button=
            document.createElement(
                "button"
            );


        button.textContent=
            tool.text;


        button.dataset.tool=
            tool.id;


        button.addEventListener(
            "click",
            () => {

                if(
                    tool.id==="undo"
                ){

                    undoAvatar();

                }

                else if(
                    tool.id==="redo"
                ){

                    redoAvatar();

                }

                else{

                    avatarTool=
                        tool.id;


                    updateAvatarTools();

                }

            }
        );


        tools.appendChild(
            button
        );

    }


    side.appendChild(
        tools
    );


    const palette=
        document.createElement(
            "div"
        );


    palette.id=
        "palette";


    const colors=[

        "#ffffff",
        "#111827",
        "#1f2937",
        "#334155",
        "#94a3b8",

        "#d79b72",
        "#b97854",
        "#8d5524",
        "#4a3427",
        "#20242b",

        "#3f7fca",
        "#2b5e9d",
        "#5cb85c",
        "#3e8d4f",
        "#8a5b3a",

        "#d8c07b",
        "#f0c933",
        "#44d7e8",
        "#ff8a00",
        "#ef4444"

    ];


    colors.forEach(
        color => {

            const button=
                document.createElement(
                    "button"
                );


            button.className=
                "sw";


            button.style.background=
                color;


            button.addEventListener(
                "click",
                () => {

                    saveAvatarHistory();


                    avatarTool=
                        "pencil";


                    avatarColor=
                        color;


                    updateAvatarTools();

                }
            );


            palette.appendChild(
                button
            );

        }
    );


    side.appendChild(
        palette
    );


    const defaultButton=
        document.createElement(
            "button"
        );


    defaultButton.textContent=
        "Default";


    defaultButton.style.marginTop=
        "10px";


    defaultButton.addEventListener(
        "click",
        () => {

            saveAvatarHistory();


            avatarGrid=
                makeDefaultAvatar();


            drawAvatarEditor();

        }
    );


    side.appendChild(
        defaultButton
    );


    const clearButton=
        document.createElement(
            "button"
        );


    clearButton.textContent=
        "Clear";


    clearButton.style.marginLeft=
        "6px";


    clearButton.addEventListener(
        "click",
        () => {

            saveAvatarHistory();


            avatarGrid=
                Array.from(
                    {
                        length:32
                    },
                    () =>
                        Array(16).fill(null)
                );


            drawAvatarEditor();

        }
    );


    side.appendChild(
        clearButton
    );


    const saveButton=
        document.createElement(
            "button"
        );


    saveButton.textContent=
        "Save";


    saveButton.style.marginLeft=
        "6px";


    saveButton.addEventListener(
        "click",
        () => {

            localStorage.setItem(
                "paperAvatar",
                JSON.stringify(
                    normalizeAvatar()
                )
            );


            hidePanel();


            showStatus(
                "Avatar saved"
            );

        }
    );


    side.appendChild(
        saveButton
    );


    layout.appendChild(
        side
    );


    body.appendChild(
        layout
    );


    updateAvatarTools();


    drawAvatarEditor();

}


/* =========================================================
   PLAYER RENDER
   ========================================================= */

function drawHeldItem(
    c,
    item,
    x,
    y,
    facing,
    rotation,
    scale
){

    if(
        !item
    ){

        return;

    }


    c.save();


    c.translate(
        x,
        y
    );


    c.scale(
        facing*
        scale,
        scale
    );


    c.rotate(
        rotation
    );


    if(
        item.includes("pickaxe")
    ){

        let metal=
            "#a36b43";


        if(
            item.includes("stone")
        ){

            metal=
                "#bfc3c9";

        }

        if(
            item.includes("gold")
        ){

            metal=
                "#efc83c";

        }

        if(
            item.includes("diamond")
        ){

            metal=
                "#48d6e6";

        }


        c.strokeStyle=
            "#8f623e";


        c.lineWidth=5;


        c.beginPath();


        c.moveTo(
            0,
            0
        );


        c.lineTo(
            7,
            30
        );


        c.stroke();


        c.strokeStyle=
            metal;


        c.beginPath();


        c.moveTo(
            -4,
            4
        );


        c.lineTo(
            12,
            -2
        );


        c.stroke();

    }


    else if(
        item.includes("sword")
    ){

        let blade=
            "#b8794f";


        if(
            item.includes("stone")
        ){

            blade=
                "#c2c6cd";

        }


        if(
            item.includes("diamond")
        ){

            blade=
                "#45d6e5";

        }


        c.fillStyle=
            blade;


        c.fillRect(
            -2,
            0,
            7,
            29
        );


        c.fillStyle=
            "#7f5537";


        c.fillRect(
            -6,
            26,
            14,
            4
        );

    }


    else if(
        item==="torch"
    ){

        c.strokeStyle=
            "#66462e";


        c.lineWidth=4;


        c.beginPath();


        c.moveTo(
            0,
            21
        );


        c.lineTo(
            0,
            5
        );


        c.stroke();


        c.fillStyle=
            "#ff8500";


        c.fillRect(
            -6,
            0,
            12,
            10
        );


        c.fillStyle=
            "#ffd64d";


        c.fillRect(
            -3,
            -4,
            6,
            8
        );

    }


    c.restore();

}


function drawAvatarPixels(
    c,
    grid,
    left,
    top,
    scale,
    y1,
    y2,
    x1,
    x2,
    offsetX
){

    for(
        let y=y1;
        y<=y2;
        y++
    ){

        for(
            let x=x1;
            x<=x2;
            x++
        ){

            const color=
                grid[y]?.[x];


            if(
                !color
            ){

                continue;

            }


            c.fillStyle=
                color;


            c.fillRect(
                left+
                x*scale+
                offsetX,

                top+
                y*scale,

                scale,
                scale
            );

        }

    }

}


function drawPlayerThird(
    c
){

    const grid=
        normalizeAvatar();


    /*
       Scale avatar to player's actual
       collision height.
    */

    const scale=
        player.h*
        TILE/
        32;


    const spriteWidth=
        16*
        scale;


    const spriteHeight=
        32*
        scale;


    /*
       THE FEET COME DIRECTLY FROM
       player.y + player.h.
    */

    const feetX=
        player.x+
        player.w/2;


    const feetY=
        player.y+
        player.h;


    const screenX=
        worldToScreenX(
            feetX
        );


    const screenY=
        worldToScreenY(
            feetY
        );


    const left=
        screenX-
        spriteWidth/2;


    const top=
        screenY-
        spriteHeight;


    const moving=
        Math.abs(
            player.vx
        )>.08;


    const walk=
        moving
        ?Math.sin(
            player.anim
        )
        :0;


    const bob=
        moving
        ?Math.abs(walk)*
         1.2
        :0;


    /*
       Body.
    */

    drawAvatarPixels(
        c,
        grid,
        left,
        top-bob,
        scale,
        0,
        19,
        4,
        11,
        0
    );


    /*
       Arms stay attached.
       Only tiny horizontal motion.
    */

    drawAvatarPixels(
        c,
        grid,
        left,
        top-bob,
        scale,
        8,
        19,
        0,
        3,
        -walk*1.7
    );


    drawAvatarPixels(
        c,
        grid,
        left,
        top-bob,
        scale,
        8,
        19,
        12,
        15,
        walk*1.7
    );


    /*
       Legs.
    */

    drawAvatarPixels(
        c,
        grid,
        left,
        top,
        scale,
        20,
        31,
        4,
        7,
        -walk*1.4
    );


    drawAvatarPixels(
        c,
        grid,
        left,
        top,
        scale,
        20,
        31,
        8,
        11,
        walk*1.4
    );


    const item=
        selectedItem();


    if(
        item
    ){

        drawHeldItem(
            c,
            item,

            left+
            15*
            scale+
            walk*
            1.7,

            top+
            19*
            scale-
            bob,

            player.facing,

            -.15+
            walk*
            .02,

            .78
        );

    }

}


function drawPlayerFirst(
    c
){

    const moving=
        Math.abs(
            player.vx
        )>.08;


    const swing=
        moving
        ?Math.sin(
            player.anim
        )*4
        :0;


    const base=
        canvas.height-
        82;


    c.save();


    c.fillStyle=
        "#d79b72";


    c.fillRect(
        44,
        base+swing,
        18,
        56
    );


    c.fillRect(
        28,
        base+
        43+
        swing,
        24,
        13
    );


    c.fillRect(
        canvas.width-
        62,
        base-
        swing,
        18,
        56
    );


    c.fillRect(
        canvas.width-
        52,
        base+
        43-
        swing,
        24,
        13
    );


    const item=
        selectedItem();


    if(
        item
    ){

        drawHeldItem(
            c,
            item,
            canvas.width/2+38,
            base+8-swing,
            player.facing,
            -.28,
            1.55
        );

    }


    c.restore();

}


/* =========================================================
   ANIMALS — STABLE BLOCKY MODELS
   ========================================================= */

function drawAnimal(
    c,
    animal
){

    try{

        const sx=
            worldToScreenX(
                animal.x
            );


        const sy=
            worldToScreenY(
                animal.y
            );


        const walking=
            Math.abs(
                animal.vx
            )>.04;


        const walk=
            Math.sin(
                animal.anim+
                animal.x
            );


        const bob=
            walking
            ?Math.abs(walk)
            :0;


        c.save();


        c.translate(
            Math.round(sx),
            Math.round(
                sy+bob
            )
        );


        c.scale(
            animal.dir,
            1
        );


        if(
            animal.type==="pig"
        ){

            drawPig(
                c,
                walk
            );

        }


        else if(
            animal.type==="sheep"
        ){

            drawSheep(
                c,
                walk
            );

        }


        else if(
            animal.type==="cow"
        ){

            drawCow(
                c,
                walk
            );

        }


        else{

            drawChicken(
                c,
                walk
            );

        }


        c.restore();

    }catch(_){

    }

}


function drawPig(
    c,
    walk
){

    c.fillStyle=
        "#e39aa2";


    c.fillRect(
        8,
        10,
        35,
        22
    );


    c.fillRect(
        34,
        8,
        20,
        23
    );


    c.fillRect(
        35,
        5,
        7,
        7
    );


    c.fillRect(
        48,
        5,
        7,
        7
    );


    c.fillStyle=
        "#a96770";


    c.fillRect(
        14+
        walk*
        1.2,
        29,
        6,
        12
    );


    c.fillRect(
        34-
        walk*
        1.2,
        29,
        6,
        12
    );


    c.fillStyle=
        "#c8757e";


    c.fillRect(
        46,
        19,
        10,
        9
    );


    c.fillStyle=
        "#111";


    c.fillRect(
        45,
        14,
        3,
        3
    );

}


function drawSheep(
    c,
    walk
){

    c.fillStyle=
        "#ece9e0";


    c.fillRect(
        8,
        9,
        36,
        23
    );


    c.fillRect(
        5,
        13,
        9,
        11
    );


    c.fillRect(
        38,
        12,
        9,
        13
    );


    c.fillStyle=
        "#b7b0a5";


    c.fillRect(
        41,
        9,
        16,
        21
    );


    c.fillRect(
        39,
        9,
        6,
        5
    );


    c.fillRect(
        53,
        9,
        6,
        5
    );


    c.fillStyle=
        "#594437";


    c.fillRect(
        14+
        walk*
        1.1,
        30,
        6,
        12
    );


    c.fillRect(
        35-
        walk*
        1.1,
        30,
        6,
        12
    );


    c.fillStyle=
        "#111";


    c.fillRect(
        49,
        15,
        3,
        3
    );

}


function drawCow(
    c,
    walk
){

    c.fillStyle=
        "#80604b";


    c.fillRect(
        8,
        12,
        37,
        21
    );


    c.fillStyle=
        "#3f332c";


    c.fillRect(
        12,
        14,
        10,
        7
    );


    c.fillRect(
        29,
        24,
        9,
        7
    );


    c.fillStyle=
        "#5c4739";


    c.fillRect(
        39,
        8,
        18,
        23
    );


    c.fillStyle=
        "#eee8de";


    c.fillRect(
        40,
        5,
        6,
        5
    );


    c.fillRect(
        52,
        5,
        6,
        5
    );


    c.fillStyle=
        "#d0b39f";


    c.fillRect(
        48,
        19,
        10,
        8
    );


    c.fillStyle=
        "#514035";


    c.fillRect(
        14+
        walk*
        1.1,
        31,
        6,
        12
    );


    c.fillRect(
        34-
        walk*
        1.1,
        31,
        6,
        12
    );


    c.fillStyle=
        "#111";


    c.fillRect(
        48,
        14,
        3,
        3
    );

}


function drawChicken(
    c,
    walk
){

    c.fillStyle=
        "#f0ede4";


    c.fillRect(
        10,
        12,
        25,
        19
    );


    c.fillStyle=
        "#d5d0c8";


    c.fillRect(
        10,
        17+
        Math.sin(walk)*
        2,
        13,
        9
    );


    c.fillStyle=
        "#f0ede4";


    c.fillRect(
        30,
        7,
        18,
        21
    );


    c.fillStyle=
        "#d8aa28";


    c.fillRect(
        47,
        15,
        8,
        6
    );


    c.fillStyle=
        "#d94c4c";


    c.fillRect(
        33,
        4,
        5,
        5
    );


    c.fillRect(
        40,
        5,
        5,
        4
    );


    c.fillStyle=
        "#d3a52b";


    c.fillRect(
        17+
        walk,
        31,
        3,
        10
    );


    c.fillRect(
        29-
        walk,
        31,
        3,
        10
    );


    c.fillStyle=
        "#111";


    c.fillRect(
        41,
        12,
        3,
        3
    );

}


/* =========================================================
   BLOCKS
   ========================================================= */

function drawBlock(
    c,
    block,
    x,
    y
){

    if(
        block===AIR
    ){

        return;

    }


    const px=
        worldToScreenX(x);


    const py=
        worldToScreenY(y);


    if(
        block===GRASS
    ){

        c.fillStyle=
            terrainType==="snow"
            ?" #eaf3f6".trim()
            :"#61b95b";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );


        c.fillStyle=
            terrainType==="snow"
            ?" #d0d8dd".trim()
            :"#7c5235";


        c.fillRect(
            px,
            py+13,
            TILE,
            TILE-13
        );

    }


    else if(
        block===SNOW
    ){

        c.fillStyle=
            "#edf5f8";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );


        c.fillStyle=
            "#d0d8dd";


        c.fillRect(
            px,
            py+14,
            TILE,
            TILE-14
        );

    }


    else if(
        block===DIRT
    ){

        c.fillStyle=
            "#895b3b";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );

    }


    else if(
        block===SAND
    ){

        c.fillStyle=
            "#d7c078";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );

    }


    else if(
        block===LEAVES
    ){

        c.fillStyle=
            terrainType==="snow"
            ?" #76956f".trim()
            :"#3e8d4f";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );

    }


    else if(
        block===WOOD
    ){

        c.fillStyle=
            "#90613d";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );


        c.fillStyle=
            "#6c4a31";


        c.fillRect(
            px+8,
            py,
            6,
            TILE
        );


        c.fillRect(
            px+29,
            py,
            5,
            TILE
        );

    }


    else if(
        block===STONE
    ){

        c.fillStyle=
            terrainType==="mountain"
            ?" #707881".trim()
            :"#777e86";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );


        c.fillStyle=
            "rgba(0,0,0,.12)";


        c.fillRect(
            px+5,
            py+7,
            10,
            7
        );


        c.fillRect(
            px+28,
            py+29,
            10,
            7
        );


        c.fillRect(
            px+17,
            py+19,
            7,
            5
        );

    }


    else if(
        block===COAL
    ){

        c.fillStyle=
            "#777e85";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );


        c.fillStyle=
            "#2d3237";


        c.fillRect(
            px+7,
            py+7,
            10,
            8
        );


        c.fillRect(
            px+29,
            py+28,
            8,
            7
        );

    }


    else if(
        block===GOLD
    ){

        c.fillStyle=
            "#7d858b";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );


        c.fillStyle=
            "#efc83b";


        c.fillRect(
            px+9,
            py+9,
            12,
            9
        );


        c.fillRect(
            px+29,
            py+28,
            9,
            7
        );

    }


    else if(
        block===DIAMOND
    ){

        c.fillStyle=
            "#747d84";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );


        c.fillStyle=
            "#48d5e6";


        c.fillRect(
            px+9,
            py+8,
            10,
            10
        );


        c.fillRect(
            px+27,
            py+26,
            9,
            9
        );

    }


    else if(
        block===WATER
    ){

        const wave=
            Math.sin(
                animationTime*3+
                x*.4
            )*
            2;


        c.fillStyle=
            "rgba(51,137,220,.76)";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );


        c.fillStyle=
            "rgba(235,250,255,.72)";


        c.fillRect(
            px+5+wave,
            py+7,
            TILE-12,
            2
        );

    }


    else if(
        block===TORCH
    ){

        const flicker=
            Math.sin(
                animationTime*14+
                x
            )*
            2;


        c.strokeStyle=
            "#64442c";


        c.lineWidth=4;


        c.beginPath();


        c.moveTo(
            px+22,
            py+40
        );


        c.lineTo(
            px+22,
            py+16
        );


        c.stroke();


        c.fillStyle=
            "#ff8500";


        c.fillRect(
            px+15,
            py+7+flicker,
            14,
            12
        );


        c.fillStyle=
            "#ffd64d";


        c.fillRect(
            px+18,
            py+3+flicker,
            8,
            9
        );

    }


    else if(
        block===LADDER
    ){

        c.strokeStyle=
            "#b58152";


        c.lineWidth=5;


        c.beginPath();


        c.moveTo(
            px+12,
            py+2
        );


        c.lineTo(
            px+12,
            py+TILE-2
        );


        c.moveTo(
            px+32,
            py+2
        );


        c.lineTo(
            px+32,
            py+TILE-2
        );


        for(
            let yy=9;
            yy<44;
            yy+=10
        ){

            c.moveTo(
                px+12,
                py+yy
            );


            c.lineTo(
                px+32,
                py+yy
            );

        }


        c.stroke();

    }

}


/* =========================================================
   MOUNTAINS
   ========================================================= */

function drawMountainBackground(
    c
){

    const w=
        canvas.width;


    const h=
        canvas.height;


    c.fillStyle=
        terrainType==="snow"
        ?"rgba(127,151,165,.25)"
        :"rgba(71,87,103,.28)";


    c.beginPath();


    c.moveTo(
        0,
        h*.55
    );


    for(
        let x=0;
        x<=w+50;
        x+=35
    ){

        c.lineTo(
            x,
            h*.47-
            Math.abs(
                Math.sin(
                    x*.012
                )
            )*
            95
        );

    }


    c.lineTo(
        w,
        h
    );


    c.lineTo(
        0,
        h
    );


    c.closePath();


    c.fill();

}


/* =========================================================
   WORLD DRAW
   ========================================================= */

function drawWorld(
    c
){

    if(
        terrainType==="snow"
    ){

        c.fillStyle="#cee6f0";

    }

    else if(
        terrainType==="mountain"
    ){

        c.fillStyle="#96bdd4";

    }

    else if(
        terrainType==="abyss"
    ){

        c.fillStyle="#090d18";

    }

    else{

        c.fillStyle="#7fc9f3";

    }


    c.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    if(
        terrainType==="snow" ||
        terrainType==="mountain"
    ){

        drawMountainBackground(
            c
        );

    }


    const left=
        Math.floor(
            cameraX-
            canvas.width/TILE/2
        )-
        2;


    const right=
        Math.ceil(
            cameraX+
            canvas.width/TILE/2
        )+
        2;


    const top=
        Math.floor(
            cameraY-
            canvas.height/TILE/2
        )-
        2;


    const bottom=
        Math.ceil(
            cameraY+
            canvas.height/TILE/2
        )+
        2;


    for(
        let y=Math.max(
            0,
            top
        );
        y<
            Math.min(
                WORLD_H,
                bottom+1
            );
        y++
    ){

        for(
            let x=Math.max(
                0,
                left
            );
            x<
                Math.min(
                    WORLD_W,
                    right+1
                );
            x++
        ){

            drawBlock(
                c,
                getBlock(
                    x,
                    y
                ),
                x,
                y
            );

        }

    }


    for(
        const animal of animals
    ){

        drawAnimal(
            c,
            animal
        );

    }


    for(
        const particle of particles
    ){

        const px=
            worldToScreenX(
                particle.x
            );


        const py=
            worldToScreenY(
                particle.y
            );


        c.fillStyle=
            "#d2b286";


        c.fillRect(
            px,
            py,
            particle.size,
            particle.size
        );

    }


    if(
        breaking
    ){

        const px=
            worldToScreenX(
                breaking.x
            );


        const py=
            worldToScreenY(
                breaking.y
            );


        const progress=
            clamp(
                breaking.progress/
                breaking.need,
                0,
                1
            );


        c.strokeStyle=
            "rgba(0,0,0,.85)";


        c.lineWidth=3;


        c.strokeRect(
            px+2,
            py+2,
            TILE-4,
            TILE-4
        );


        c.fillStyle=
            "rgba(255,255,255,.38)";


        c.fillRect(
            px+2,
            py+TILE-8,
            (TILE-4)*
            progress,
            5
        );

    }


    if(
        viewFirst
    ){

        drawPlayerFirst(
            c
        );

    }

    else{

        drawPlayerThird(
            c
        );

    }

}


/* =========================================================
   OBBY DRAW
   ========================================================= */

function drawObbyCoin(
    c,
    coin
){

    if(
        coin.collected
    ){

        return;

    }


    const x=
        worldToScreenX(
            coin.x
        );


    const y=
        worldToScreenY(
            coin.y
        );


    const bob=
        Math.sin(
            animationTime*5+
            coin.x
        )*
        1.5;


    c.fillStyle=
        "#f5c84b";


    c.beginPath();


    c.arc(
        x,
        y+bob,
        8,
        0,
        Math.PI*2
    );


    c.fill();


    c.fillStyle=
        "#fff3a0";


    c.fillRect(
        x-2,
        y-5+bob,
        4,
        10
    );

}


function drawObby(
    c
){

    c.fillStyle=
        "#9fd7ed";


    c.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    c.fillStyle=
        "rgba(255,255,255,.22)";


    c.fillRect(
        80,
        70,
        110,
        18
    );


    c.fillRect(
        500,
        110,
        150,
        18
    );


    for(
        const platform of
        obbyPlatforms
    ){

        const px=
            worldToScreenX(
                platform.x
            );


        const py=
            worldToScreenY(
                platform.y
            );


        c.fillStyle=
            "#765039";


        c.fillRect(
            px,
            py,
            platform.w*
            TILE,
            TILE
        );


        c.fillStyle=
            "#57b95b";


        c.fillRect(
            px,
            py,
            platform.w*
            TILE,
            7
        );

    }


    /*
       Bounce pads.
    */

    for(
        const pad of
        obbyBouncePads
    ){

        const px=
            worldToScreenX(
                pad.x
            );


        const py=
            worldToScreenY(
                pad.y
            );


        c.fillStyle=
            "#a56bdb";


        c.fillRect(
            px,
            py,
            1.3*
            TILE,
            6
        );

    }


    /*
       Speed pads.
    */

    for(
        const pad of
        obbySpeedPads
    ){

        const px=
            worldToScreenX(
                pad.x
            );


        const py=
            worldToScreenY(
                pad.y
            );


        c.fillStyle=
            "#3d9ee8";


        c.fillRect(
            px,
            py,
            1.5*
            TILE,
            6
        );

    }


    /*
       Mystery blocks.
    */

    for(
        const block of
        obbyMysteryBlocks
    ){

        const px=
            worldToScreenX(
                block.x
            );


        const py=
            worldToScreenY(
                block.y
            );


        c.fillStyle=
            block.used
            ?" #777".trim()
            :"#b86bd0";


        c.fillRect(
            px,
            py,
            TILE,
            TILE
        );


        c.fillStyle=
            "#fff";


        c.font=
            "bold 22px Arial";


        c.fillText(
            "?",
            px+12,
            py+29
        );

    }


    /*
       Checkpoints.
    */

    for(
        const checkpoint of
        obbyCheckpoints
    ){

        const px=
            worldToScreenX(
                checkpoint.x
            );


        const py=
            worldToScreenY(
                checkpoint.y
            );


        c.strokeStyle=
            "#333";


        c.lineWidth=3;


        c.beginPath();


        c.moveTo(
            px,
            py
        );


        c.lineTo(
            px,
            py-55
        );


        c.stroke();


        c.fillStyle=
            checkpoint.activated
            ?" #56d96b".trim()
            :"#f0b94e";


        c.fillRect(
            px+2,
            py-54,
            25,
            16
        );

    }


    /*
       Coins.
    */

    for(
        const coin of
        obbyCoinItems
    ){

        drawObbyCoin(
            c,
            coin
        );

    }


    /*
       Finish.
    */

    const finishX=
        worldToScreenX(
            obbyFinish.x
        );


    const finishY=
        worldToScreenY(
            obbyFinish.y
        );


    c.fillStyle=
        "#3fc66b";


    c.fillRect(
        finishX,
        finishY,
        obbyFinish.w*
        TILE,
        TILE
    );


    c.strokeStyle=
        "#333";


    c.lineWidth=3;


    c.beginPath();


    c.moveTo(
        finishX+25,
        finishY
    );


    c.lineTo(
        finishX+25,
        finishY-80
    );


    c.stroke();


    c.fillStyle=
        "#ef5252";


    c.fillRect(
        finishX+26,
        finishY-79,
        48,
        24
    );


    c.fillStyle=
        "#fff";


    c.font=
        "bold 13px Arial";


    c.fillText(
        "FINISH",
        finishX+30,
        finishY-62
    );


    /*
       Confetti.
    */

    for(
        const item of
        confetti
    ){

        const px=
            item.screen
            ?item.x
            :worldToScreenX(
                item.x
            );


        const py=
            item.screen
            ?item.y
            :worldToScreenY(
                item.y
            );


        c.save();


        c.translate(
            px,
            py
        );


        c.rotate(
            item.rot
        );


        c.fillStyle=
            item.color;


        c.fillRect(
            -item.size/2,
            -item.size/2,
            item.size,
            item.size
        );


        c.restore();

    }


    drawPlayerThird(
        c
    );

}


/* =========================================================
   CONFETTI
   ========================================================= */

function burstConfetti(
    count,
    screen
){

    for(
        let i=0;
        i<count;
        i++
    ){

        confetti.push({

            x:
                screen
                ?canvas.width/2
                :player.x+
                 player.w/2,

            y:
                screen
                ?canvas.height/2
                :player.y,

            screen,

            vx:
                (
                    Math.random()-
                    .5
                )*
                (
                    screen
                    ?7
                    :3
                ),

            vy:
                -(
                    2+
                    Math.random()*
                    4
                ),

            life:
                1.2+
                Math.random()*
                .7,

            size:
                3+
                Math.random()*
                4,

            rot:
                Math.random()*6,

            color:[
                "#f2c94c",
                "#eb6b73",
                "#5da9e9",
                "#7ecf6a"
            ][
                Math.floor(
                    Math.random()*4
                )
            ]

        });

    }

}


function updateConfetti(
    dt
){

    confetti=
        confetti.filter(
            item => {

                item.life-=dt;


                item.vy+=
                    7*
                    dt;


                item.x+=
                    item.vx*
                    dt;


                item.y+=
                    item.vy*
                    dt;


                item.rot+=
                    8*
                    dt;


                return (
                    item.life>0
                );

            }
        );

}


function updateParticles(
    dt
){

    particles=
        particles.filter(
            item => {

                item.life-=dt;


                item.vy+=
                    5*
                    dt;


                item.x+=
                    item.vx*
                    dt;


                item.y+=
                    item.vy*
                    dt;


                return (
                    item.life>0
                );

            }
        );

}


/* =========================================================
   TERRAIN PANEL
   ========================================================= */

function updateTerrainUI(){

    document.getElementById(
        "terrainText"
    ).textContent=
        terrainName();


    if(
        !obbyActive
    ){

        document.getElementById(
            "terrainBadge"
        ).textContent=
            terrainName();

    }

}


function openTerrain(){

    panelMode="terrain";


    showPanel(
        "Change Terrain"
    );


    const body=
        document.getElementById(
            "panelBody"
        );


    body.innerHTML=
        `
        <div style="
            margin-bottom:10px;
            color:#cbd5e1
        ">
            Current:
            <b>${terrainName()}</b>
        </div>

        <div class="terrainGrid">

            <button
                class="terrainButton"
                data-terrain="plain"
            >
                🌱 Plain
                <small>
                    Normal world
                </small>
            </button>

            <button
                class="terrainButton"
                data-terrain="snow"
            >
                ❄️ Snow
                <small>
                    Snow world
                </small>
            </button>

            <button
                class="terrainButton"
                data-terrain="mountain"
            >
                ⛰️ Mountain
                <small>
                    Rocky peaks
                </small>
            </button>

            <button
                class="terrainButton"
                data-terrain="abyss"
            >
                🌑 Abyss
                <small>
                    Giant gaps
                </small>
            </button>

        </div>
        `;


    body
        .querySelectorAll(
            "[data-terrain]"
        )
        .forEach(
            button => {

                button.addEventListener(
                    "click",
                    () => {

                        terrainType=
                            button.dataset.terrain;


                        obbyActive=false;
                        obbyWon=false;


                        worldSeed=
                            Date.now();


                        generateWorld();


                        hidePanel();

                    }
                );

            }
        );

}


/* =========================================================
   INVENTORY
   ========================================================= */

function renderInventory(){

    panelMode="inventory";


    showPanel(
        "Inventory / Equipment"
    );


    const body=
        document.getElementById(
            "panelBody"
        );


    body.innerHTML=
        `
        <div>
            Collected items stay in the inventory.
            Equip them into hotbar slots 1–9.
        </div>
        `;


    const equip=
        document.createElement(
            "div"
        );


    equip.className=
        "equip";


    for(
        let i=0;
        i<9;
        i++
    ){

        const cell=
            document.createElement(
                "div"
            );


        cell.className=
            "eSlot";


        const item=
            hotbar[i];


        if(item){

            cell.innerHTML=
                `
                ${
                    ITEM_ICONS[item] ||
                    "⬜"
                }

                <small>
                    ${i+1}
                </small>
                `;


            const remove=
                document.createElement(
                    "button"
                );


            remove.textContent=
                "×";


            remove.onclick=
                () => {

                    hotbar[i]=null;

                    renderInventory();

                    renderHotbar();

                };


            cell.appendChild(
                remove
            );

        }

        else{

            cell.innerHTML=
                `
                <small>
                    ${i+1}
                </small>
                `;

        }


        equip.appendChild(
            cell
        );

    }


    body.appendChild(
        equip
    );


    const grid=
        document.createElement(
            "div"
        );


    grid.id=
        "panelGrid";


    Object.keys(inv)
        .filter(
            item =>
                countItem(item)>0
        )
        .forEach(
            item => {

                const card=
                    document.createElement(
                        "div"
                    );


                card.className=
                    "card";


                card.innerHTML=
                    `
                    <div class="itemRow">

                        <div>
                            ${
                                ITEM_ICONS[item] ||
                                "⬜"
                            }

                            <b>
                                ${item}
                            </b>
                        </div>

                        <b>
                            ${countItem(item)}
                        </b>

                    </div>

                    <small>
                        Equip:
                    </small>
                    `;


                for(
                    let i=0;
                    i<9;
                    i++
                ){

                    const button=
                        document.createElement(
                            "button"
                        );


                    button.textContent=
                        "Slot "+(i+1);


                    button.style.margin=
                        "4px 3px 0 0";


                    button.onclick=
                        () => {

                            hotbar[i]=
                                item;


                            renderInventory();

                            renderHotbar();

                        };


                    card.appendChild(
                        button
                    );

                }


                grid.appendChild(
                    card
                );

            }
        );


    body.appendChild(
        grid
    );

}


function renderInventoryMaybe(){

    if(
        panelMode==="inventory"
    ){

        renderInventory();

    }

}


/* =========================================================
   CRAFTING
   ========================================================= */

function craft(
    recipe
){

    for(
        const [name,count] of
        Object.entries(
            recipe.mats
        )
    ){

        if(
            countItem(name)<count
        ){

            showStatus(
                "Not enough materials"
            );


            return;

        }

    }


    for(
        const [name,count] of
        Object.entries(
            recipe.mats
        )
    ){

        removeItem(
            name,
            count
        );

    }


    addItem(
        recipe.item,
        recipe.count
    );


    showStatus(
        "Crafted "+recipe.name
    );

}


function renderCrafting(){

    panelMode="craft";


    showPanel(
        "Crafting"
    );


    const body=
        document.getElementById(
            "panelBody"
        );


    body.innerHTML="";


    recipes.forEach(
        recipe => {

            const row=
                document.createElement(
                    "div"
                );


            row.className=
                "recipe";


            const materials=
                Object.entries(
                    recipe.mats
                )
                .map(
                    ([name,count]) =>
                        `${name} ×${count}`
                )
                .join(", ");


            row.innerHTML=
                `
                <div>

                    <div class="recipeTitle">
                        ${recipe.name}
                    </div>

                    <div class="recipeMats">
                        ${materials}
                    </div>

                </div>
                `;


            const button=
                document.createElement(
                    "button"
                );


            button.textContent=
                "Craft";


            button.onclick=
                () =>
                    craft(
                        recipe
                    );


            row.appendChild(
                button
            );


            body.appendChild(
                row
            );

        }
    );

}


/* =========================================================
   PANEL
   ========================================================= */

function showPanel(
    title
){

    document.getElementById(
        "panel"
    ).style.display=
        "block";


    document.getElementById(
        "panelTitle"
    ).textContent=
        title;

}


function hidePanel(){

    panelMode="";

    avatarEditing=false;

    avatarDrawing=false;


    document.getElementById(
        "panel"
    ).style.display=
        "none";

}


/* =========================================================
   MINING
   ========================================================= */

function breakSpeed(
    block
){

    const item=
        selectedItem();


    if(
        block===STONE ||
        block===COAL ||
        block===GOLD ||
        block===DIAMOND
    ){

        return (
            item &&
            TOOL_SPEED[item]
        )
        ?TOOL_SPEED[item]
        :.18;

    }


    if(
        block===WOOD
    ){

        return (
            item &&
            TOOL_SPEED[item]
        )
        ?TOOL_SPEED[item]*.85
        :.55;

    }


    if(
        block===LEAVES
    ){

        return .9;

    }


    return .8;

}


function startBreak(
    wx,
    wy
){

    if(
        obbyActive
    ){

        return;

    }


    const x=
        Math.floor(wx);


    const y=
        Math.floor(wy);


    const block=
        getBlock(
            x,
            y
        );


    if(
        !inBounds(x,y) ||
        block===AIR ||
        block===WATER
    ){

        return;

    }


    const dx=
        x+.5-
        (
            player.x+
            player.w/2
        );


    const dy=
        y+.5-
        (
            player.y+
            player.h/2
        );


    if(
        Math.hypot(
            dx,
            dy
        )>
        5.25
    ){

        return;

    }


    breaking={

        x,
        y,
        block,

        progress:0,

        need:
            BLOCK_HARDNESS[block] ||
            300

    };

}


function updateBreaking(
    dt
){

    if(
        !breaking
    ){

        return;

    }


    if(
        getBlock(
            breaking.x,
            breaking.y
        )!==
        breaking.block
    ){

        breaking=null;

        return;

    }


    breaking.progress+=
        dt*
        1000*
        breakSpeed(
            breaking.block
        );


    if(
        breaking.progress>=
        breaking.need
    ){

        const block=
            breaking.block;


        setBlock(
            breaking.x,
            breaking.y,
            AIR
        );


        waterSources.delete(
            gridKey(
                breaking.x,
                breaking.y
            )
        );


        waterLevel[
            breaking.y
        ][
            breaking.x
        ]=0;


        const drop=
            DROP_ITEM[block];


        if(drop){

            addItem(
                drop,
                1
            );

        }


        if(
            block===LEAVES &&
            Math.random()<.22
        ){

            addItem(
                "apple",
                1
            );

        }


        for(
            let i=0;
            i<6;
            i++
        ){

            particles.push({

                x:
                    breaking.x+
                    .5,

                y:
                    breaking.y+
                    .5,

                vx:
                    (
                        Math.random()-
                        .5
                    )*
                    2,

                vy:
                    -Math.random()*
                    2,

                life:.45,

                size:
                    2+
                    Math.random()*
                    3

            });

        }


        breaking=null;

    }

}


/* =========================================================
   COMBAT / FOOD
   ========================================================= */

function attackDamage(){

    const item=
        selectedItem();


    if(
        item==="wood_sword"
    ){

        return 15;

    }


    if(
        item==="stone_sword"
    ){

        return 22;

    }


    if(
        item==="diamond_sword"
    ){

        return 35;

    }


    return 8;

}


function attackDelay(){

    const item=
        selectedItem();


    if(
        item==="wood_sword"
    ){

        return 260;

    }


    if(
        item==="stone_sword"
    ){

        return 210;

    }


    if(
        item==="diamond_sword"
    ){

        return 150;

    }


    return 400;

}


function attackAnimal(
    animal
){

    const now=
        performance.now();


    if(
        now<
        attackReadyAt
    ){

        return;

    }


    attackReadyAt=
        now+
        attackDelay();


    animal.health-=
        attackDamage();


    animal.vx+=
        player.facing*
        1.5;


    animal.vy=-2;


    if(
        animal.health<=0
    ){

        if(
            animal.type==="pig"
        ){

            addItem(
                "pork",
                1
            );

        }


        else if(
            animal.type==="sheep"
        ){

            addItem(
                "wool",
                1
            );

        }


        else if(
            animal.type==="cow"
        ){

            addItem(
                "leather",
                2
            );

        }


        else{

            addItem(
                "feather",
                1
            );

        }


        animals=
            animals.filter(
                item =>
                    item!==animal
            );

    }

}


function eatFood(
    item
){

    const values={

        apple:18,
        pork:30,
        golden_apple:50

    };


    const gain=
        values[item] ||
        0;


    if(
        gain<=0 ||
        countItem(item)<=0
    ){

        return;

    }


    removeItem(
        item,
        1
    );


    player.hunger=
        clamp(
            player.hunger+
            gain,
            0,
            100
        );


    renderStats();

}


/* =========================================================
   BUCKET
   ========================================================= */

function useBucket(
    wx,
    wy
){

    if(
        obbyActive
    ){

        return false;

    }


    const item=
        selectedItem();


    const x=
        Math.floor(wx);


    const y=
        Math.floor(wy);


    if(
        item==="water_bucket"
    ){

        if(
            inBounds(x,y) &&
            getBlock(x,y)===AIR
        ){

            setBlock(
                x,
                y,
                WATER
            );


            waterLevel[y][x]=8;


            waterSources.add(
                gridKey(
                    x,
                    y
                )
            );


            removeItem(
                "water_bucket",
                1
            );


            addItem(
                "bucket",
                1
            );

        }


        return true;

    }


    if(
        item==="bucket" &&
        getBlock(x,y)===WATER
    ){

        setBlock(
            x,
            y,
            AIR
        );


        waterLevel[y][x]=0;


        waterSources.delete(
            gridKey(
                x,
                y
            )
        );


        removeItem(
            "bucket",
            1
        );


        addItem(
            "water_bucket",
            1
        );


        return true;

    }


    return false;

}


/* =========================================================
   PLACEMENT
   ========================================================= */

function canPlace(
    x,
    y,
    item
){

    if(
        obbyActive ||
        !inBounds(x,y) ||
        getBlock(x,y)!==AIR ||
        !PLACE_BLOCK[item]
    ){

        return false;

    }


    if(
        x+1>player.x &&
        x<
            player.x+
            player.w &&
        y+1>player.y &&
        y<
            player.y+
            player.h
    ){

        return false;

    }


    const distance=
        Math.hypot(
            x+.5-
            (
                player.x+
                player.w/2
            ),
            y+.5-
            (
                player.y+
                player.h/2
            )
        );


    if(
        distance>
        5.25
    ){

        return false;

    }


    if(
        item==="ladder"
    ){

        return (
            isSolidBlock(
                getBlock(
                    x-1,
                    y
                )
            ) ||
            isSolidBlock(
                getBlock(
                    x+1,
                    y
                )
            )
        );

    }


    return (
        isSolidBlock(
            getBlock(x-1,y)
        ) ||
        isSolidBlock(
            getBlock(x+1,y)
        ) ||
        isSolidBlock(
            getBlock(x,y-1)
        ) ||
        isSolidBlock(
            getBlock(x,y+1)
        )
    );

}


function placeSelected(
    wx,
    wy
){

    if(
        obbyActive
    ){

        return;

    }


    const item=
        selectedItem();


    if(
        !item ||
        countItem(item)<=0
    ){

        return;

    }


    if(
        useBucket(
            wx,
            wy
        )
    ){

        return;

    }


    const bx=
        Math.floor(wx);


    const by=
        Math.floor(wy);


    let best=null;


    for(
        let dy=-2;
        dy<=2;
        dy++
    ){

        for(
            let dx=-2;
            dx<=2;
            dx++
        ){

            const x=
                bx+dx;


            const y=
                by+dy;


            if(
                canPlace(
                    x,
                    y,
                    item
                )
            ){

                const d=
                    Math.hypot(
                        dx,
                        dy
                    );


                if(
                    !best ||
                    d<best.distance
                ){

                    best={
                        x,
                        y,
                        distance:d
                    };

                }

            }

        }

    }


    if(
        !best
    ){

        showStatus(
            "Cannot place here"
        );


        return;

    }


    setBlock(
        best.x,
        best.y,
        PLACE_BLOCK[item]
    );


    removeItem(
        item,
        1
    );

}


/* =========================================================
   MOUSE
   ========================================================= */

function mouseWorld(
    event
){

    const rect=
        canvas.getBoundingClientRect();


    return {

        x:
            (
                event.clientX-
                rect.left-
                canvas.width/2
            )/
            TILE+
            cameraX,

        y:
            (
                event.clientY-
                rect.top-
                canvas.height/2
            )/
            TILE+
            cameraY

    };

}


canvas.addEventListener(
    "mousedown",
    event => {

        if(
            panelMode ||
            obbyActive
        ){

            return;

        }


        const p=
            mouseWorld(
                event
            );


        if(
            event.button===0
        ){

            const animal=
                animals.find(
                    a =>
                        p.x>=a.x-.3 &&
                        p.x<=
                            a.x+
                            a.w+
                            .3 &&
                        p.y>=a.y-.3 &&
                        p.y<=
                            a.y+
                            a.h+
                            .3
                );


            if(
                animal
            ){

                attackAnimal(
                    animal
                );

            }

            else{

                const item=
                    selectedItem();


                if(
                    item==="apple" ||
                    item==="pork" ||
                    item==="golden_apple"
                ){

                    eatFood(
                        item
                    );

                }

                else{

                    startBreak(
                        p.x,
                        p.y
                    );

                }

            }

        }


        else if(
            event.button===2
        ){

            placeSelected(
                p.x,
                p.y
            );

        }

    }
);


canvas.addEventListener(
    "contextmenu",
    event => {

        event.preventDefault();

    }
);


canvas.addEventListener(
    "mousemove",
    event => {

        if(
            event.buttons===1 &&
            !panelMode &&
            !obbyActive &&
            !breaking
        ){

            const p=
                mouseWorld(
                    event
                );


            startBreak(
                p.x,
                p.y
            );

        }

    }
);


window.addEventListener(
    "mouseup",
    () => {

        breaking=null;

    }
);


/* =========================================================
   KEYBOARD
   ========================================================= */

window.addEventListener(
    "keydown",
    event => {

        const key=
            event.key.toLowerCase();


        keys[key]=true;


        if(
            event.key>="1" &&
            event.key<="9"
        ){

            const slot=
                Number(
                    event.key
                )-
                1;


            if(
                hotbar[slot]
            ){

                selectedSlot=
                    slot;


                renderHotbar();

            }

        }


        if(
            key==="e"
        ){

            event.preventDefault();


            if(
                panelMode==="inventory"
            ){

                hidePanel();

            }

            else{

                renderInventory();

            }

        }


        if(
            key==="c"
        ){

            event.preventDefault();


            if(
                panelMode==="craft"
            ){

                hidePanel();

            }

            else{

                renderCrafting();

            }

        }


        if(
            key==="v"
        ){

            event.preventDefault();


            viewFirst=
                !viewFirst;


            document.getElementById(
                "viewBtn"
            ).textContent=
                viewFirst
                ?"View: 1st person (V)"
                :"View: 3rd person (V)";

        }


        if(
            key==="escape"
        ){

            hidePanel();

        }

    }
);


window.addEventListener(
    "keyup",
    event => {

        keys[
            event.key.toLowerCase()
        ]=false;

    }
);


/* =========================================================
   STATS / HOTBAR
   ========================================================= */

function renderStats(){

    document.getElementById(
        "healthText"
    ).textContent=
        Math.round(
            player.health
        );


    document.getElementById(
        "hungerText"
    ).textContent=
        Math.round(
            player.hunger
        );


    document.getElementById(
        "selectedText"
    ).textContent=
        selectedItem() ||
        "empty";


    document.getElementById(
        "toolText"
    ).textContent=
        selectedTool();

}


function addItem(
    item,
    amount=1
){

    if(
        !item
    ){

        return;

    }


    inv[item]=
        (inv[item]||0)+
        amount;


    renderHotbar();

    renderStats();

    renderInventoryMaybe();

}


function removeItem(
    item,
    amount=1
){

    inv[item]=
        Math.max(
            0,
            (inv[item]||0)-
            amount
        );


    renderHotbar();

    renderStats();

    renderInventoryMaybe();

}


function renderHotbar(){

    const bar=
        document.getElementById(
            "hotbar"
        );


    bar.innerHTML="";


    for(
        let i=0;
        i<9;
        i++
    ){

        const slot=
            document.createElement(
                "div"
            );


        slot.className=
            "slot"+
            (
                i===
                selectedSlot
                ?" sel"
                :""
            );


        const item=
            hotbar[i];


        if(item){

            slot.innerHTML=
                `
                <div class="slotIcon">
                    ${
                        ITEM_ICONS[item] ||
                        "⬜"
                    }
                </div>

                <div class="slotCount">
                    ${i+1} ·
                    ${countItem(item)}
                </div>
                `;

        }

        else{

            slot.innerHTML=
                `
                <div class="slotCount">
                    ${i+1}
                </div>
                `;

        }


        bar.appendChild(
            slot
        );

    }


    renderStats();

}


/* =========================================================
   HUNGER
   ========================================================= */

function updateHunger(
    dt
){

    if(
        obbyActive
    ){

        return;

    }


    hungerTimer+=dt;


    if(
        hungerTimer>=6
    ){

        hungerTimer=0;


        if(
            player.hunger>0
        ){

            player.hunger=
                Math.max(
                    0,
                    player.hunger-1
                );

        }

        else{

            player.health=
                Math.max(
                    0,
                    player.health-1
                );

        }


        if(
            player.health<=0
        ){

            player.health=100;
            player.hunger=100;


            player.x=12;


            player.y=
                findGroundY(12)-
                player.h;


            player.vx=0;
            player.vy=0;

        }


        renderStats();

    }

}


/* =========================================================
   GAME LOOP
   ========================================================= */

function resize(){

    const rect=
        document
            .getElementById(
                "gameWrap"
            )
            .getBoundingClientRect();


    const width=
        Math.max(
            520,
            Math.floor(
                rect.width
            )
        );


    const height=
        Math.max(
            420,
            Math.floor(
                rect.height
            )
        );


    if(
        canvas.width!==width ||
        canvas.height!==height
    ){

        canvas.width=
            width;


        canvas.height=
            height;


        buffer.width=
            width;


        buffer.height=
            height;

    }

}


function render(){

    try{

        if(
            buffer.width!==canvas.width ||
            buffer.height!==canvas.height
        ){

            buffer.width=
                canvas.width;


            buffer.height=
                canvas.height;

        }


        bctx.clearRect(
            0,
            0,
            buffer.width,
            buffer.height
        );


        if(
            obbyActive
        ){

            drawObby(
                bctx
            );

        }

        else{

            drawWorld(
                bctx
            );

        }


        /*
           Visible canvas is replaced only
           after the entire frame succeeds.
        */

        ctx.clearRect(
            0,
            0,
            canvas.width,
            canvas.height
        );


        ctx.drawImage(
            buffer,
            0,
            0
        );

    }

    catch(_){

        /*
           Keep previous frame.
           No error overlay.
        */

    }

}


function gameLoop(
    now
){

    const dt=
        clamp(
            (
                now-
                lastTime
            )/
            1000,
            0,
            .05
        );


    lastTime=now;


    animationTime+=dt;


    try{

        resize();

        updatePlayer(dt);

        updateBreaking(dt);

        updateWater(dt);

        updateAnimals(dt);

        updateParticles(dt);

        updateConfetti(dt);

        updateHunger(dt);

        updateCamera();

        render();

    }

    catch(_){

        /*
           Keep the loop alive.
        */

    }


    requestAnimationFrame(
        gameLoop
    );

}


/* =========================================================
   WATER
   ========================================================= */

function updateWater(
    dt
){

    if(
        obbyActive
    ){

        return;

    }


    waterTimer-=dt;


    if(
        waterTimer>0
    ){

        return;

    }


    waterTimer=.10;


    const next=
        waterLevel.map(
            row =>
                row.slice()
        );


    for(
        const source of
        waterSources
    ){

        const parts=
            source
                .split(",")
                .map(Number);


        const x=parts[0];
        const y=parts[1];


        if(
            getBlock(x,y)===WATER
        ){

            next[y][x]=8;

        }

    }


    for(
        let y=WORLD_H-2;
        y>=0;
        y--
    ){

        for(
            let x=0;
            x<WORLD_W;
            x++
        ){

            if(
                getBlock(x,y)!==WATER
            ){

                continue;

            }


            const level=
                waterLevel[y][x] ||
                8;


            if(
                getBlock(
                    x,
                    y+1
                )===AIR
            ){

                setBlock(
                    x,
                    y+1,
                    WATER
                );


                next[y+1][x]=
                    Math.max(
                        next[y+1][x],
                        level
                    );


                continue;

            }


            if(
                level<=1
            ){

                continue;

            }


            for(
                const nx of
                [x-1,x+1]
            ){

                if(
                    inBounds(nx,y) &&
                    getBlock(
                        nx,
                        y
                    )===AIR
                ){

                    setBlock(
                        nx,
                        y,
                        WATER
                    );


                    next[y][nx]=
                        Math.max(
                            next[y][nx],
                            level-1
                        );

                }

            }

        }

    }


    for(
        let y=0;
        y<WORLD_H;
        y++
    ){

        for(
            let x=0;
            x<WORLD_W;
            x++
        ){

            if(
                getBlock(x,y)===WATER
            ){

                waterLevel[y][x]=
                    next[y][x] ||
                    8;

            }

            else{

                waterLevel[y][x]=0;

            }

        }

    }

}


/* =========================================================
   CAMERA
   ========================================================= */

function updateCamera(){

    if(
        obbyActive
    ){

        return;

    }


    cameraX+=
        (
            player.x+
            player.w/2-
            cameraX
        )*.14;


    cameraY+=
        (
            player.y+
            player.h/2-
            cameraY
        )*.14;


    const halfW=
        canvas.width/
        TILE/
        2;


    const halfH=
        canvas.height/
        TILE/
        2;


    cameraX=
        clamp(
            cameraX,
            halfW,
            WORLD_W-
            halfW
        );


    cameraY=
        clamp(
            cameraY,
            halfH,
            WORLD_H-
            halfH
        );

}


/* =========================================================
   TOP BUTTONS
   ========================================================= */

document.getElementById(
    "invBtn"
).onclick=
    () => {

        if(
            panelMode==="inventory"
        ){

            hidePanel();

        }

        else{

            renderInventory();

        }

    };


document.getElementById(
    "craftBtn"
).onclick=
    () => {

        if(
            panelMode==="craft"
        ){

            hidePanel();

        }

        else{

            renderCrafting();

        }

    };


document.getElementById(
    "avatarBtn"
).onclick=
    () => {

        if(
            panelMode==="avatar"
        ){

            hidePanel();

        }

        else{

            openAvatar();

        }

    };


document.getElementById(
    "terrainBtn"
).onclick=
    () => {

        if(
            panelMode==="terrain"
        ){

            hidePanel();

        }

        else{

            openTerrain();

        }

    };


document.getElementById(
    "obbyBtn"
).onclick=
    () => {

        if(
            panelMode==="obby"
        ){

            hidePanel();

        }

        else{

            openObbyPanel();

        }

    };


document.getElementById(
    "viewBtn"
).onclick=
    () => {

        viewFirst=
            !viewFirst;


        document.getElementById(
            "viewBtn"
        ).textContent=
            viewFirst
            ?"View: 1st person (V)"
            :"View: 3rd person (V)";

    };


document.getElementById(
    "resetBtn"
).onclick=
    () => {

        obbyActive=false;
        obbyWon=false;


        worldSeed=
            Date.now();


        generateWorld();


        hidePanel();


        showStatus(
            "New world generated"
        );

    };


/* =========================================================
   START
   ========================================================= */

loadAvatar();

generateWorld();

resize();

renderStats();

renderHotbar();

render();

requestAnimationFrame(
    gameLoop
);

})();
</script>

</body>
</html>
'''

components.html(
    GAME,
    height=1000,
    scrolling=False
)