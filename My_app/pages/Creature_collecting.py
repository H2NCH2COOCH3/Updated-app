
import pygame
import random
import json
import os
import math
import copy

# ============================================================
# MYTHIC WILDS - SLIM CREATURES + ANIMATED SKILLS
# Install: pip install pygame
# ============================================================

pygame.init()
W, H = 1120, 760
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("MYTHIC WILDS")
clock = pygame.time.Clock()

SAVE_FILE = "mythic_wilds_save.json"
FONT = pygame.font.SysFont("arial", 20, bold=True)
SMALL = pygame.font.SysFont("arial", 15, bold=True)
BIG = pygame.font.SysFont("arial", 34, bold=True)
TITLE = pygame.font.SysFont("arial", 45, bold=True)

BG = (16, 23, 39)
PANEL = (29, 40, 61)
PANEL2 = (42, 56, 80)
WHITE = (241, 246, 255)
MUTED = (160, 177, 202)
GREEN = (80, 221, 137)
RED = (255, 88, 103)
GOLD = (255, 205, 90)
BLUE = (85, 170, 255)

ELEMENTS = {
    "Nature": {
        "color": (83, 204, 104), "dark": (29, 89, 53),
        "light": (190, 255, 176),
        "moves": ["Razor Leaf", "Vine Whip", "Wild Bloom"]
    },
    "Fire": {
        "color": (241, 82, 49), "dark": (117, 36, 39),
        "light": (255, 211, 105),
        "moves": ["Flame Claw", "Fireball", "Inferno"]
    },
    "Water": {
        "color": (65, 157, 240), "dark": (29, 70, 143),
        "light": (184, 239, 255),
        "moves": ["Aqua Fang", "Water Shot", "Tidal Crash"]
    },
    "Electric": {
        "color": (240, 203, 59), "dark": (123, 91, 25),
        "light": (255, 255, 180),
        "moves": ["Spark Claw", "Thunderbolt", "Storm Strike"]
    },
    "Earth": {
        "color": (163, 119, 81), "dark": (77, 54, 43),
        "light": (231, 193, 145),
        "moves": ["Stone Claw", "Rock Shot", "Earthquake"]
    },
    "Shadow": {
        "color": (143, 88, 221), "dark": (52, 31, 100),
        "light": (223, 188, 255),
        "moves": ["Shadow Slash", "Void Orb", "Nightfall"]
    }
}

RARITIES = {
    "Common": ((166, 180, 194), 1.0),
    "Uncommon": ((83, 219, 135), 1.15),
    "Rare": ((80, 164, 255), 1.4),
    "Epic": ((190, 105, 255), 1.8),
    "Mythic": ((255, 190, 66), 2.4)
}

STAGES = ["Young", "Evolved", "Ascended"]


# ------------------------------------------------------------
# GENERAL HELPERS
# ------------------------------------------------------------

def clamp(v, low, high):
    return max(low, min(high, v))


def mix(a, b, t):
    return tuple(int(a[i] * (1-t) + b[i] * t) for i in range(3))


def text(surface, value, x, y, font=FONT, color=WHITE, center=False):
    image = font.render(str(value), True, color)
    rect = image.get_rect()
    if center:
        rect.center = (int(x), int(y))
    else:
        rect.topleft = (int(x), int(y))
    surface.blit(image, rect)


def rounded(surface, color, rect, radius=12, border=None, width=2):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, width, border_radius=radius)


def panel(rect, title=None):
    rounded(screen, PANEL, rect, 17, (57, 75, 105), 2)
    if title:
        text(screen, title, rect[0]+17, rect[1]+12)


def draw_bar(surface, x, y, width, height, value, maximum, color):
    pygame.draw.rect(surface, (12, 17, 28), (x, y, width, height),
                     border_radius=height//2)
    ratio = clamp(value/max(1, maximum), 0, 1)
    if ratio:
        pygame.draw.rect(
            surface, color,
            (x, y, max(2, int(width*ratio)), height),
            border_radius=height//2
        )


# ------------------------------------------------------------
# CREATURE DATA
# ------------------------------------------------------------

def make_creature(element=None, rarity=None):
    element = element or random.choice(list(ELEMENTS))
    rarity = rarity or random.choices(
        list(RARITIES), weights=[42, 28, 17, 9, 4]
    )[0]

    names = {
        "Nature": ["Thornlynx", "Bramblefang", "Verdant Drake"],
        "Fire": ["Cinderclaw", "Pyrolynx", "Emberdrake"],
        "Water": ["Rivertalon", "Tidefang", "Azure Drake"],
        "Electric": ["Voltlynx", "Stormclaw", "Thunder Drake"],
        "Earth": ["Cragfang", "Stoneclaw", "Terra Drake"],
        "Shadow": ["Duskfang", "Nightclaw", "Void Drake"]
    }

    c = {
        "id": random.randint(100000, 999999999),
        "name": random.choice(names[element]),
        "element": element,
        "rarity": rarity,
        "stage": 0,
        "level": 1,
        "exp": 0,
        "favorite": False,
        "seed": random.randint(0, 999999)
    }
    update_stats(c, True)
    return c


def update_stats(c, full=False):
    multiplier = RARITIES[c["rarity"]][1]
    stage_multiplier = [1.0, 1.65, 2.6][c["stage"]]
    old_max = c.get("max_hp", 1)
    old_hp = c.get("hp", 1)

    c["max_hp"] = int((70+c["level"]*12)*multiplier*stage_multiplier)
    c["attack"] = int((12+c["level"]*2.8)*multiplier*stage_multiplier)
    c["defense"] = int((5+c["level"]*1.3)*multiplier*stage_multiplier)

    if full:
        c["hp"] = c["max_hp"]
    else:
        c["hp"] = min(c["max_hp"],
                      int(old_hp+max(0, c["max_hp"]-old_max)))


def gain_exp(c, amount):
    c["exp"] += amount
    leveled = False
    while c["exp"] >= c["level"]*30:
        c["exp"] -= c["level"]*30
        c["level"] += 1
        update_stats(c, True)
        leveled = True
    return leveled


def new_game():
    starter = make_creature("Nature", "Common")
    return {"creatures": [starter], "selected": starter["id"],
            "coins": 100, "orbs": 5}


def save_game():
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(game, f, indent=2)
    except Exception as e:
        print("Save error:", e)


def load_game():
    if not os.path.exists(SAVE_FILE):
        return new_game()
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not data.get("creatures"):
            return new_game()
        for c in data["creatures"]:
            c.setdefault("stage", 0)
            c.setdefault("level", 1)
            c.setdefault("exp", 0)
            c.setdefault("favorite", False)
            c.setdefault("seed", random.randint(0, 999999))
            update_stats(c)
        if not any(c["id"] == data.get("selected")
                   for c in data["creatures"]):
            data["selected"] = data["creatures"][0]["id"]
        data.setdefault("coins", 100)
        data.setdefault("orbs", 5)
        return data
    except Exception as e:
        print("Load error:", e)
        return new_game()


game = load_game()


def selected_creature():
    for c in game["creatures"]:
        if c["id"] == game["selected"]:
            return c
    game["selected"] = game["creatures"][0]["id"]
    return game["creatures"][0]


# ------------------------------------------------------------
# SLIM FANTASY CREATURE ART
# Each creature is drawn facing RIGHT, then flipped for enemies.
# Narrow torso, longer legs, pointed muzzle, angular silhouette.
# ------------------------------------------------------------

def draw_creature(surface, c, center, scale=1.0, facing=1,
                  animation=0, hit_flash=False):
    element = ELEMENTS[c["element"]]
    base = (255, 255, 255) if hit_flash else element["color"]
    dark = (190, 190, 200) if hit_flash else element["dark"]
    light = (255, 255, 255) if hit_flash else element["light"]
    stage = c["stage"]
    kind = list(ELEMENTS).index(c["element"])

    size = max(100, int(270*scale))
    sprite = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, int(size*.57)

    def P(x, y):
        return int(cx+x*scale), int(cy+y*scale)

    def poly(color, points, outline=None):
        pts = [P(x, y) for x, y in points]
        pygame.draw.polygon(sprite, color, pts)
        if outline:
            pygame.draw.polygon(sprite, outline, pts,
                                max(1, int(2*scale)))

    def ell(color, x, y, w, h, outline=None):
        r = (int(cx+x*scale), int(cy+y*scale),
             max(1, int(w*scale)), max(1, int(h*scale)))
        pygame.draw.ellipse(sprite, color, r)
        if outline:
            pygame.draw.ellipse(sprite, outline, r,
                                max(1, int(2*scale)))

    # Ground shadow
    ell((0, 0, 0, 75), -73, 43, 145, 17)

    # Evolved aura
    if stage >= 1:
        radius = int((65+stage*12)*scale)
        pygame.draw.circle(sprite, (*base, 25), P(0, -12), radius)
        pygame.draw.circle(sprite, (*light, 80), P(0, -12),
                           radius, max(1, int(2*scale)))

    # Tail: narrow and long, not a round nub
    if kind == 0:
        poly(dark, [(-36, 2), (-61, -5), (-91, -22),
                    (-76, -4), (-99, 5), (-68, 9), (-39, 12)])
        poly(base, [(-46, 3), (-67, -3), (-86, -15),
                    (-74, -1), (-90, 4), (-64, 5)])
        poly(light, [(-83, -13), (-75, -3), (-87, 1)])
    elif kind == 1:
        poly(dark, [(-38, 4), (-64, -8), (-87, -24),
                    (-76, -3), (-94, 11), (-61, 13)])
        poly((255, 157, 56), [(-64, -8), (-76, -3),
                              (-94, 11), (-82, 4)])
    elif kind == 2:
        poly(dark, [(-39, 3), (-70, -13), (-99, -1),
                    (-77, 9), (-94, 19), (-57, 12)])
        poly(light, [(-57, 2), (-80, -7), (-90, -1), (-67, 7)])
    elif kind == 3:
        poly(light, [(-39, 4), (-65, -8), (-88, 4),
                     (-62, 12), (-46, 10)])
    elif kind == 4:
        poly(dark, [(-38, 4), (-67, -4), (-90, 10),
                    (-66, 18), (-43, 12)])
        poly(base, [(-48, 6), (-69, 3), (-80, 10), (-63, 13)])
    else:
        poly(dark, [(-38, 3), (-66, -15), (-63, 1),
                    (-95, 12), (-67, 19), (-41, 12)])

    # Wings are narrow, angular, and attached to the shoulders.
    if stage >= 1 or kind == 5:
        wing_dark = mix(dark, (16, 20, 32), .20)
        wing_mid = mix(base, dark, .35)

        poly(wing_dark, [
            (-26, -18), (-39, -40), (-69, -58),
            (-62, -35), (-78, -24), (-51, -13), (-34, -2)
        ], dark)
        poly(wing_mid, [
            (-39, -34), (-62, -51), (-55, -32),
            (-69, -25), (-48, -18)
        ])
        poly(light, [
            (-43, -31), (-58, -43), (-52, -28), (-43, -22)
        ])

        poly(wing_dark, [
            (5, -23), (17, -48), (43, -58),
            (38, -38), (54, -29), (38, -13), (23, -1)
        ], dark)
        poly(wing_mid, [
            (20, -34), (39, -51), (33, -32),
            (47, -27), (33, -17)
        ])
        poly(light, [
            (22, -31), (35, -43), (31, -28), (23, -22)
        ])

        # Fine wing veins
        pygame.draw.line(sprite, dark, P(-39, -27), P(-63, -45),
                         max(1, int(2*scale)))
        pygame.draw.line(sprite, dark, P(25, -28), P(41, -43),
                         max(1, int(2*scale)))

    # Long legs with visible joints and narrow feet
    for lx in (-39, -8, 25, 43):
        leg_top = 8 if lx in (-8, 25) else 4
        pygame.draw.line(sprite, dark, P(lx, leg_top),
                         P(lx+(-2 if lx < 0 else 3), 43),
                         max(3, int(10*scale)))
        pygame.draw.line(sprite, base, P(lx-1, leg_top+3),
                         P(lx+(-2 if lx < 0 else 3), 39),
                         max(2, int(5*scale)))
        poly(dark, [
            (lx-7, 42), (lx+5, 42), (lx+10, 48),
            (lx-9, 48)
        ])
        poly(light, [(lx-4, 43), (lx+2, 43), (lx+5, 45)])

    # Slim body, different silhouette per element
    if kind == 0:
        poly(dark, [(-49, -9), (-43, -31), (-19, -37),
                    (11, -31), (34, -17), (39, 2),
                    (22, 18), (-28, 17), (-47, 7)])
        poly(base, [(-44, -10), (-38, -28), (-17, -33),
                    (10, -27), (29, -14), (34, 1),
                    (19, 13), (-26, 12), (-42, 4)])
        poly(light, [(-30, -25), (-15, -30), (3, -26),
                     (-7, -19), (-26, -18)])
        poly(dark, [(-23, -30), (-18, -49), (-7, -31)])
        poly(dark, [(0, -29), (10, -45), (15, -26)])
    elif kind == 1:
        poly(dark, [(-48, 2), (-45, -20), (-25, -36),
                    (9, -38), (33, -19), (43, 2),
                    (22, 17), (-27, 16)])
        poly(base, [(-43, 0), (-40, -18), (-22, -31),
                    (8, -33), (29, -16), (38, 1),
                    (20, 12), (-25, 12)])
        poly(light, [(-29, -23), (-9, -31), (8, -25),
                     (-4, -17), (-22, -16)])
        poly((255, 161, 54), [(-14, 2), (-1, -13),
                              (8, 2), (1, 12), (-11, 11)])
    elif kind == 2:
        poly(dark, [(-49, -8), (-40, -29), (-12, -35),
                    (18, -27), (39, -9), (31, 9),
                    (-25, 15), (-46, 5)])
        poly(base, [(-43, -9), (-35, -26), (-12, -31),
                    (15, -23), (33, -7), (26, 5),
                    (-24, 10), (-41, 2)])
        poly(light, [(-27, -24), (-11, -29), (5, -23),
                     (-7, -18), (-23, -17)])
        poly(light, [(-13, -30), (-5, -49), (5, -28)])
        poly(dark, [(-32, 0), (-47, -10), (-44, 12)])
    elif kind == 3:
        poly(dark, [(-47, -7), (-40, -28), (-15, -34),
                    (13, -28), (35, -11), (35, 6),
                    (15, 16), (-29, 12), (-45, 4)])
        poly(base, [(-41, -8), (-35, -25), (-14, -30),
                    (11, -24), (29, -9), (29, 4),
                    (13, 11), (-27, 8), (-40, 2)])
        poly(light, [(-29, -23), (-12, -29), (3, -23),
                     (-9, -17), (-25, -17)])
        poly(dark, [(-24, -29), (-39, -47), (-7, -32)])
        poly(light, [(-28, -34), (-35, -42), (-17, -32)])
        poly(dark, [(0, -28), (17, -47), (13, -26)])
        poly(light, [(-9, -12), (3, -12), (-3, -1),
                     (8, -1), (-10, 12), (-5, 2), (-15, 2)])
    elif kind == 4:
        poly(dark, [(-48, 4), (-44, -21), (-24, -37),
                    (8, -37), (34, -17), (39, 4),
                    (20, 16), (-28, 15)])
        poly(base, [(-42, 1), (-39, -19), (-22, -32),
                    (7, -32), (29, -15), (33, 2),
                    (17, 11), (-26, 11)])
        poly(light, [(-30, -25), (-15, -31), (-4, -24),
                     (-15, -17), (-28, -18)])
        poly(dark, [(-29, -30), (-18, -50), (-9, -31)])
        poly(dark, [(0, -31), (18, -48), (16, -27)])
    else:
        poly(dark, [(-48, -7), (-40, -29), (-13, -35),
                    (14, -27), (35, -10), (32, 7),
                    (13, 16), (-28, 13), (-45, 4)])
        poly(base, [(-42, -8), (-35, -25), (-12, -30),
                    (12, -22), (29, -8), (26, 3),
                    (11, 11), (-26, 9), (-40, 2)])
        poly(light, [(-28, -23), (-12, -29), (2, -22),
                     (-8, -17), (-24, -17)])
        poly(light, [(-29, -28), (-27, -47), (-15, -30)])
        poly(light, [(-4, -29), (8, -49), (12, -27)])

    # Chest plate and belly shading, kept narrow
    ell(mix(base, dark, .28), -13, -2, 36, 18)
    ell(mix(base, light, .17), -12, -4, 26, 8)

    # Neck and pointed head
    poly(dark, [(16, -27), (34, -42), (51, -38),
                (62, -26), (53, -13), (30, -12)])
    poly(base, [(18, -29), (35, -39), (50, -35),
                (58, -26), (50, -17), (31, -15)])
    poly(light, [(34, -35), (46, -35), (53, -29),
                 (40, -29)])

    # Long pointed snout - avoids the round pig-like face
    poly(dark, [(44, -29), (64, -28), (78, -20),
                (66, -16), (48, -18)])
    poly(base, [(48, -27), (64, -26), (73, -21),
                (64, -19), (49, -20)])
    poly(light, [(52, -25), (65, -24), (69, -22)])

    # Eye and eyebrow
    eye = P(43, -34)
    pygame.draw.ellipse(sprite, (15, 19, 30),
                        (eye[0]-int(7*scale), eye[1]-int(5*scale),
                         int(14*scale), int(11*scale)))
    pygame.draw.circle(sprite, light, eye, max(2, int(4*scale)))
    pygame.draw.circle(sprite, (18, 23, 35),
                       (eye[0]+int(2*scale), eye[1]),
                       max(1, int(2*scale)))
    pygame.draw.line(sprite, dark, P(34, -41), P(49, -40),
                     max(1, int(3*scale)))

    # Nose and mouth line
    pygame.draw.circle(sprite, dark, P(72, -21), max(2, int(2.5*scale)))
    pygame.draw.line(sprite, dark, P(55, -17), P(69, -17),
                     max(1, int(1.5*scale)))

    # Element details
    if kind == 0:
        poly(light, [(-4, -19), (4, -29), (8, -17)])
        poly(dark, [(15, -15), (24, -22), (27, -11)])
    elif kind == 1:
        poly(GOLD, [(-31, -18), (-25, -34), (-17, -20)])
        for i in range(3):
            px = -35 + ((i*22+int(animation*35)) % 65)
            py = -47-(i % 2)*8
            poly(GOLD, [(px, py+6), (px+4, py-5), (px+7, py+6)])
    elif kind == 2:
        poly(light, [(-22, -28), (-11, -43), (-7, -25)])
        ell(light, -38, -31, 6, 6)
    elif kind == 3:
        poly(light, [(-10, -12), (1, -12), (-4, -2),
                     (6, -2), (-9, 10), (-5, 2), (-14, 2)])
    elif kind == 4:
        poly(dark, [(-30, -31), (-20, -47), (-12, -31)])
        poly(light, [(-27, -33), (-21, -42), (-17, -32)])
    elif kind == 5:
        poly(light, [(-25, -29), (-22, -48), (-12, -30)])
        pygame.draw.circle(sprite, (*light, 160), P(-49, -26),
                           max(2, int(3*scale)))

    # Evolution armor and crown
    if stage >= 1:
        armor = GOLD if stage == 2 else dark
        poly(armor, [(-20, -17), (-8, -31), (5, -19),
                     (1, -7), (-13, -6)])
        poly(mix(armor, light, .35),
             [(-15, -19), (-8, -26), (-2, -19), (-8, -12)])
        poly(armor, [(-34, -13), (-25, -24), (-15, -15),
                     (-23, -5)])
        poly(armor, [(18, -19), (30, -28), (36, -16),
                     (27, -7)])

    if stage == 2:
        poly(GOLD, [(-13, -42), (-5, -61), (2, -43),
                    (13, -57), (17, -39), (28, -48),
                    (30, -34), (-12, -33)])
        poly((255, 240, 177), [(-8, -44), (-5, -55), (0, -43)])

    # Favorite marker
    if c.get("favorite"):
        text(sprite, "★", int(cx-70*scale), int(cy-60*scale),
             SMALL, GOLD, True)

    # Flip all features together, so enemy looks left.
    if facing < 0:
        sprite = pygame.transform.flip(sprite, True, False)

    surface.blit(sprite, sprite.get_rect(
        center=(int(center[0]), int(center[1]))
    ))


# ------------------------------------------------------------
# SKILL EFFECTS
# Slash / fireball / water wave / lightning / rock / shadow.
# Effects animate across the arena toward the opposing creature.
# ------------------------------------------------------------

effects = []
floaters = []
screen_shake = 0


def spawn_skill_effect(element, skill_index, start, end):
    effects.append({
        "element": element,
        "skill": skill_index,
        "start": start,
        "end": end,
        "t": 0.0,
        "duration": .42 if skill_index == 0 else .62,
        "particles": [
            {
                "offset": random.uniform(-28, 28),
                "side": random.choice([-1, 1]),
                "size": random.randint(2, 5)
            }
            for _ in range(16)
        ]
    })


def burst(x, y, color, amount=18):
    for _ in range(amount):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(45, 220)
        effects.append({
            "element": "PARTICLE",
            "color": color,
            "x": x, "y": y,
            "vx": math.cos(angle)*speed,
            "vy": math.sin(angle)*speed,
            "life": random.uniform(.25, .65),
            "max": .65,
            "size": random.randint(2, 6)
        })


def floater(value, x, y, color=WHITE):
    floaters.append({"value": str(value), "x": x, "y": y,
                     "life": 1.0, "color": color})


def update_effects(dt):
    for e in effects[:]:
        e["t"] += dt
        if e["element"] == "PARTICLE":
            e["x"] += e["vx"]*dt
            e["y"] += e["vy"]*dt
            e["vy"] += 70*dt
            e["life"] -= dt
            if e["life"] <= 0:
                effects.remove(e)
        elif e["t"] > e["duration"]:
            effects.remove(e)

    for f in floaters[:]:
        f["y"] -= 38*dt
        f["life"] -= dt
        if f["life"] <= 0:
            floaters.remove(f)


def draw_skill_effects():
    for e in effects:
        if e["element"] == "PARTICLE":
            r = max(1, int(e["size"]*e["life"]/e["max"]))
            pygame.draw.circle(screen, e["color"],
                               (int(e["x"]), int(e["y"])), r)
            continue

        element = e["element"]
        data = ELEMENTS[element]
        col, light = data["color"], data["light"]
        start, end = e["start"], e["end"]
        t = clamp(e["t"]/e["duration"], 0, 1)
        x = start[0] + (end[0]-start[0])*t
        y = start[1] + (end[1]-start[1])*t
        skill = e["skill"]

        if skill == 0:
            # Fast slash: several diagonal, bright blade streaks.
            width = int(45*(1-t)+12)
            for j in range(3):
                offset = (j-1)*13
                a = (int(x-width), int(y+offset+22))
                b = (int(x+width*.25), int(y+offset-22))
                pygame.draw.line(screen, col, a, b, 5)
                pygame.draw.line(screen, light, a, b, 2)
            pygame.draw.circle(screen, light, (int(x), int(y)), 5)

        elif skill == 1:
            # A moving elemental projectile with a glowing core.
            radius = int(10+5*math.sin(t*math.pi*8))
            pygame.draw.circle(screen, (*col, 60), (int(x), int(y)),
                               radius+12)
            pygame.draw.circle(screen, col, (int(x), int(y)), radius)
            pygame.draw.circle(screen, light, (int(x), int(y)),
                               max(2, radius//2))
            tail_x = int(x-(end[0]-start[0])*.06)
            pygame.draw.line(screen, col, (tail_x, int(y)),
                             (int(x), int(y)), 7)

        else:
            # Big ultimate effects vary by element.
            if element == "Electric":
                pts = [(int(x-24), int(y-48)), (int(x-5), int(y-15)),
                       (int(x-17), int(y-15)), (int(x+17), int(y+25)),
                       (int(x+5), int(y-3)), (int(x+19), int(y-3))]
                pygame.draw.lines(screen, light, False, pts, 8)
                pygame.draw.lines(screen, col, False, pts, 4)

            elif element == "Water":
                rect = pygame.Rect(int(x-43), int(y-27), 86, 54)
                pygame.draw.arc(screen, col, rect, 0, math.pi, 7)
                pygame.draw.arc(screen, light, rect.inflate(-15, -12),
                                0, math.pi, 4)
                pygame.draw.circle(screen, light,
                                   (int(x), int(y)), 11, 3)

            elif element == "Fire":
                for j in range(5):
                    angle = j*math.tau/5
                    px = int(x+math.cos(angle)*20)
                    py = int(y+math.sin(angle)*20)
                    pygame.draw.circle(screen, col, (px, py), 10)
                    pygame.draw.circle(screen, light, (px, py), 4)

            elif element == "Nature":
                for j in range(5):
                    px = int(x+(j-2)*13)
                    py = int(y+math.sin(t*8+j)*12)
                    pygame.draw.ellipse(screen, col,
                                        (px-5, py-12, 10, 24))
                    pygame.draw.line(screen, light, (px, py-8),
                                     (px, py+8), 2)

            elif element == "Earth":
                for j in range(5):
                    px = int(x+(j-2)*15)
                    py = int(y+abs(j-2)*5)
                    pygame.draw.polygon(
                        screen, col,
                        [(px-9, py+12), (px-3, py-12),
                         (px+8, py-4), (px+10, py+12)]
                    )
                    pygame.draw.line(screen, light, (px-3, py-7),
                                     (px+2, py+3), 2)

            else:
                pygame.draw.circle(screen, col, (int(x), int(y)), 30, 5)
                pygame.draw.circle(screen, light, (int(x), int(y)), 18, 3)
                pygame.draw.circle(screen, col, (int(x), int(y)), 8)

    for f in floaters:
        img = BIG.render(f["value"], True, f["color"])
        img.set_alpha(int(255*clamp(f["life"], 0, 1)))
        screen.blit(img, (int(f["x"]), int(f["y"])))


# ------------------------------------------------------------
# BUTTONS
# ------------------------------------------------------------

buttons = []


def add_button(label, rect, color=PANEL2, action=None,
               text_color=WHITE, border=None):
    rect = pygame.Rect(rect)
    pygame.draw.rect(screen, color, rect, border_radius=12)
    if border:
        pygame.draw.rect(screen, border, rect, 2, border_radius=12)
    img = SMALL.render(str(label), True, text_color)
    screen.blit(img, img.get_rect(center=rect.center))
    buttons.append((rect, label if action is None else action))


def clicked_action(pos):
    for rect, action in reversed(buttons):
        if rect.collidepoint(pos):
            return action
    return None


# ------------------------------------------------------------
# BATTLE SYSTEM
# ------------------------------------------------------------

page = "home"
battle = None
message = ""


def start_battle():
    global battle, page, message
    player = selected_creature()
    if player["hp"] <= 0:
        player["hp"] = player["max_hp"]

    enemy = make_creature()
    enemy["level"] = random.randint(max(1, player["level"]-1),
                                    player["level"]+2)
    update_stats(enemy, True)

    battle = {
        "player_id": player["id"],
        "enemy": enemy,
        "phase": "ready",
        "timer": 0,
        "result": None
    }
    page = "battle"
    message = "A wild creature appeared!"


def finish_battle(won):
    global message
    player = next(
        (c for c in game["creatures"]
         if c["id"] == battle["player_id"]),
        selected_creature()
    )
    if won:
        reward = 20+battle["enemy"]["level"]*8
        game["coins"] += reward
        leveled = gain_exp(player, 25+battle["enemy"]["level"]*5)
        update_stats(player)
        message = f"Victory! +{reward} coins!"
        if leveled:
            message += " LEVEL UP!"
    else:
        message = "Defeat! Your creature needs a rest."
    save_game()


def perform_move(index):
    global message, screen_shake

    if battle is None or battle["phase"] != "ready":
        return

    player = next(
        (c for c in game["creatures"]
         if c["id"] == battle["player_id"]),
        None
    )
    if player is None:
        return

    enemy = battle["enemy"]
    if player["hp"] <= 0 or enemy["hp"] <= 0:
        return

    index = clamp(index, 0, 2)
    move_name = ELEMENTS[player["element"]]["moves"][index]
    multiplier = [1.0, 1.45, 2.0][index]
    damage = max(1, int(player["attack"]*multiplier
                        - enemy["defense"]*.35
                        + random.randint(0, 5)))

    enemy["hp"] = max(0, enemy["hp"]-damage)

    # The player attacks from the left toward the enemy on the right.
    spawn_skill_effect(player["element"], index, (375, 315), (765, 315))
    floater(f"-{damage}", 760, 250, RED)
    burst(765, 315, ELEMENTS[player["element"]]["color"], 22)
    screen_shake = 5

    battle["phase"] = "player_attack"
    battle["timer"] = .48
    message = f"{player['name']} used {move_name}!"


def enemy_attack():
    global message, screen_shake

    player = next(
        (c for c in game["creatures"]
         if c["id"] == battle["player_id"]),
        None
    )
    if player is None:
        return

    enemy = battle["enemy"]
    damage = max(1, int(enemy["attack"]*random.uniform(.75, 1.15)
                        - player["defense"]*.3))
    player["hp"] = max(0, player["hp"]-damage)

    # Enemy attacks from the right toward the player on the left.
    spawn_skill_effect(enemy["element"], random.randint(0, 2),
                       (755, 315), (365, 315))
    floater(f"-{damage}", 325, 250, RED)
    burst(365, 315, ELEMENTS[enemy["element"]]["color"], 18)
    screen_shake = 5

    battle["phase"] = "enemy_attack"
    battle["timer"] = .58
    message = f"{enemy['name']} attacks!"


def update_battle(dt):
    global page, battle, screen_shake

    if battle is None or battle["phase"] == "ready":
        return

    battle["timer"] -= dt

    if battle["phase"] == "player_attack" and battle["timer"] <= 0:
        if battle["enemy"]["hp"] <= 0:
            battle["phase"] = "result"
            battle["result"] = "win"
            battle["timer"] = 1.5
            finish_battle(True)
        else:
            enemy_attack()

    elif battle["phase"] == "enemy_attack" and battle["timer"] <= 0:
        player = next(
            (c for c in game["creatures"]
             if c["id"] == battle["player_id"]),
            None
        )
        if player is None or player["hp"] <= 0:
            battle["phase"] = "result"
            battle["result"] = "lose"
            battle["timer"] = 1.5
            finish_battle(False)
        else:
            battle["phase"] = "ready"

    elif battle["phase"] == "result" and battle["timer"] <= 0:
        page = "home"
        battle = None
        save_game()

    screen_shake = max(0, screen_shake-dt*18)


def try_capture():
    global message
    if battle is None or battle["phase"] != "ready":
        return
    if game["orbs"] <= 0:
        message = "You have no capture orbs!"
        return

    game["orbs"] -= 1
    enemy = battle["enemy"]
    ratio = enemy["hp"]/max(1, enemy["max_hp"])
    chance = clamp(.25+(1-ratio)*.65, .25, .9)

    if random.random() < chance:
        captured = copy.deepcopy(enemy)
        captured["id"] = random.randint(100000, 999999999)
        captured["hp"] = captured["max_hp"]
        game["creatures"].append(captured)
        message = f"Captured {captured['name']}!"
        battle["phase"] = "result"
        battle["result"] = "capture"
        battle["timer"] = 1.5
        save_game()
    else:
        message = "The creature escaped!"
        enemy_attack()
    save_game()


# ------------------------------------------------------------
# HOME SCREEN
# ------------------------------------------------------------

def home_screen():
    buttons.clear()
    screen.fill(BG)
    text(screen, "MYTHIC WILDS", 35, 22, TITLE)
    text(screen, "Collect  •  Evolve  •  Battle", 40, 76,
         SMALL, MUTED)
    text(screen, f"Coins: {game['coins']}", 840, 35, FONT, GOLD)
    text(screen, f"Orbs: {game['orbs']}", 840, 68, FONT, BLUE)

    c = selected_creature()
    panel((30, 125, 510, 565), "YOUR PARTNER")
    draw_creature(screen, c, (280, 345), 1.48, 1,
                  pygame.time.get_ticks()/1000)
    text(screen, c["name"], 280, 477, BIG, WHITE, True)
    text(screen, f"{c['rarity']} {c['element']} • {STAGES[c['stage']]}",
         280, 514, SMALL, RARITIES[c["rarity"]][0], True)
    text(screen, f"Level {c['level']}", 85, 553)
    text(screen, f"HP {c['hp']}/{c['max_hp']}",
         85, 583, SMALL, GREEN)
    draw_bar(screen, 85, 607, 380, 13, c["hp"], c["max_hp"], GREEN)
    text(screen, f"ATK {c['attack']}    DEF {c['defense']}",
         85, 635, SMALL, MUTED)

    panel((565, 125, 525, 565), "ADVENTURE")
    add_button("BATTLE  /  Find a wild creature",
               (605, 180, 445, 58), (61, 109, 186), "BATTLE")
    add_button("COLLECTION  /  View creatures",
               (605, 253, 445, 58), (48, 129, 98), "COLLECTION")
    add_button("EVOLVE  /  Upgrade your partner",
               (605, 326, 445, 58), (126, 78, 180), "EVOLVE")
    add_button("HEAL", (605, 400, 215, 52), (44, 125, 91), "HEAL")
    add_button("FAVORITE", (835, 400, 215, 52),
               (128, 98, 43), "FAVORITE")
    add_button("SHOP", (605, 468, 215, 52),
               (47, 91, 151), "SHOP")
    add_button("SAVE GAME", (835, 468, 215, 52), PANEL2, "SAVE")
    add_button("QUIT", (605, 538, 445, 48), (112, 53, 68), "QUIT")
    text(screen, "Sharper silhouettes • elemental skill effects",
         605, 615, SMALL, MUTED)


# ------------------------------------------------------------
# BATTLE SCREEN
# ------------------------------------------------------------

def battle_screen():
    buttons.clear()
    screen.fill((17, 28, 45))

    pygame.draw.rect(screen, (24, 43, 63), (0, 0, W, 470))
    pygame.draw.circle(screen, (36, 61, 81), (560, 205), 205)
    pygame.draw.ellipse(screen, (43, 80, 76), (20, 315, 1080, 175))
    pygame.draw.ellipse(screen, (35, 65, 65), (80, 350, 960, 120))

    player = next(
        (c for c in game["creatures"]
         if c["id"] == battle["player_id"]),
        selected_creature()
    )
    enemy = battle["enemy"]

    player_offset = 0
    enemy_offset = 0
    player_hit = battle["phase"] == "enemy_attack"
    enemy_hit = battle["phase"] == "player_attack"

    if battle["phase"] == "player_attack":
        player_offset = int(22*math.sin(
            (1-battle["timer"]/.48)*math.pi
        ))
    elif battle["phase"] == "enemy_attack":
        enemy_offset = int(22*math.sin(
            (1-battle["timer"]/.58)*math.pi
        ))

    # Face-to-face: player looks RIGHT, enemy looks LEFT.
    draw_creature(screen, player, (310+player_offset, 325),
                  1.22, 1, pygame.time.get_ticks()/1000, player_hit)
    draw_creature(screen, enemy, (805-enemy_offset, 325),
                  1.22, -1, pygame.time.get_ticks()/1000, enemy_hit)

    panel((35, 20, 405, 102))
    text(screen, f"{player['name']} Lv.{player['level']}", 55, 35)
    text(screen, f"{player['element']} • {player['rarity']}",
         55, 63, SMALL, ELEMENTS[player["element"]]["color"])
    draw_bar(screen, 55, 92, 350, 14,
             player["hp"], player["max_hp"], GREEN)
    text(screen, f"{player['hp']}/{player['max_hp']}",
         340, 91, SMALL)

    panel((680, 20, 405, 102))
    text(screen, f"{enemy['name']} Lv.{enemy['level']}", 700, 35)
    text(screen, f"{enemy['element']} • {enemy['rarity']}",
         700, 63, SMALL, ELEMENTS[enemy["element"]]["color"])
    draw_bar(screen, 700, 92, 350, 14,
             enemy["hp"], enemy["max_hp"], RED)
    text(screen, f"{enemy['hp']}/{enemy['max_hp']}",
         985, 91, SMALL)

    panel((25, 480, 1070, 250), "BATTLE ACTIONS")

    if battle["phase"] == "ready":
        moves = ELEMENTS[player["element"]]["moves"]
        colors = [ELEMENTS[player["element"]]["dark"],
                  ELEMENTS[player["element"]]["color"],
                  (117, 75, 172)]
        powers = [1.0, 1.45, 2.0]

        for i in range(3):
            rect = pygame.Rect(50+i*265, 535, 245, 72)
            rounded(screen, colors[i], rect, 12, (220, 230, 250), 2)
            text(screen, moves[i], rect.centerx, rect.y+23,
                 FONT, WHITE, True)
            text(screen, f"Power x{powers[i]:.2f}",
                 rect.centerx, rect.y+51, SMALL, WHITE, True)
            buttons.append((rect, f"SKILL_{i}"))

        add_button(f"CAPTURE ORB ({game['orbs']})",
                   (50, 625, 245, 48), (50, 100, 163), "CAPTURE")
        add_button("HEAL - 30 COINS",
                   (315, 625, 245, 48), (43, 128, 92), "BATTLE_HEAL")
        add_button("RUN AWAY", (580, 625, 245, 48),
                   (132, 59, 71), "RUN")
    elif battle["phase"] == "result":
        label = "VICTORY!" if battle.get("result") in ("win", "capture") else "DEFEAT"
        text(screen, label, 560, 575, BIG, GOLD, True)
        text(screen, "Returning to home...", 560, 620,
             SMALL, MUTED, True)
    else:
        text(screen, message, 560, 580, BIG, WHITE, True)
        text(screen, "Skill animation...", 560, 620, SMALL, MUTED, True)

    add_button("BACK TO HOME", (850, 665, 210, 42), PANEL2, "HOME")


# ------------------------------------------------------------
# COLLECTION
# ------------------------------------------------------------

def collection_screen():
    buttons.clear()
    screen.fill(BG)
    text(screen, "CREATURE COLLECTION", 35, 25, TITLE)
    text(screen, "Choose your battle partner.", 40, 80, SMALL, MUTED)
    add_button("BACK", (930, 30, 150, 45), PANEL2, "HOME")

    for i, c in enumerate(game["creatures"][:5]):
        y = 130+i*106
        chosen = c["id"] == game["selected"]
        rounded(screen, PANEL, (35, y, 1050, 91), 14,
                GOLD if chosen else (56, 73, 105), 2)
        draw_creature(screen, c, (105, y+45), .46, 1,
                      pygame.time.get_ticks()/1000)
        text(screen, c["name"], 160, y+12)
        text(screen, f"{c['rarity']} {c['element']} • {STAGES[c['stage']]} • Lv.{c['level']}",
             160, y+42, SMALL, RARITIES[c["rarity"]][0])
        text(screen, f"HP {c['hp']}/{c['max_hp']}",
             535, y+18, SMALL, GREEN)
        text(screen, f"ATK {c['attack']}  DEF {c['defense']}",
             535, y+46, SMALL, MUTED)
        add_button("SELECT", (780, y+23, 105, 42),
                   (48, 125, 86), f"SELECT_{c['id']}")
        add_button("★" if c.get("favorite") else "☆",
                   (905, y+23, 55, 42), (133, 98, 41),
                   f"FAV_{c['id']}")

    if len(game["creatures"]) > 5:
        text(screen, f"Showing 5 of {len(game['creatures'])} creatures.",
             40, 675, SMALL, MUTED)


# ------------------------------------------------------------
# EVOLUTION
# ------------------------------------------------------------

def evolve_screen():
    buttons.clear()
    screen.fill(BG)
    c = selected_creature()
    text(screen, "EVOLUTION CHAMBER", 35, 25, TITLE)
    add_button("BACK", (930, 30, 150, 45), PANEL2, "HOME")
    panel((80, 125, 960, 555), "YOUR CREATURE")

    draw_creature(screen, c, (330, 350), 1.5, 1,
                  pygame.time.get_ticks()/1000)
    text(screen, c["name"], 330, 480, BIG, WHITE, True)
    text(screen, f"Stage: {STAGES[c['stage']]}",
         330, 520, FONT, GOLD, True)

    if c["stage"] < 2:
        cost = [100, 250][c["stage"]]
        text(screen, "Evolution gives your creature", 600, 250,
             SMALL, MUTED)
        text(screen, "new armor, wings and stronger stats.", 600, 275,
             SMALL, MUTED)
        text(screen, f"Cost: {cost} coins", 600, 335, FONT, GOLD)
        text(screen, f"Your coins: {game['coins']}", 600, 370,
             SMALL, WHITE)
        add_button("EVOLVE NOW", (600, 420, 280, 60),
                   (126, 78, 181), "EVOLVE_NOW")
    else:
        text(screen, "MAXIMUM EVOLUTION REACHED", 600, 350,
             FONT, GOLD)


# ------------------------------------------------------------
# SHOP
# ------------------------------------------------------------

def shop_screen():
    buttons.clear()
    screen.fill(BG)
    text(screen, "WILD SHOP", 35, 25, TITLE)
    add_button("BACK", (930, 30, 150, 45), PANEL2, "HOME")
    panel((100, 145, 920, 500), "SUPPLIES")
    text(screen, f"Coins: {game['coins']}", 155, 210, BIG, GOLD)
    text(screen, f"Capture orbs: {game['orbs']}", 155, 275, FONT, BLUE)
    add_button("BUY 1 ORB • 25 COINS",
               (155, 345, 350, 65), (48, 101, 170), "BUY_1")
    add_button("BUY 5 ORBS • 100 COINS",
               (555, 345, 350, 65), (63, 110, 184), "BUY_5")
    text(screen, "Wild creatures are easier to catch at low HP.",
         155, 465, SMALL, MUTED)


# ------------------------------------------------------------
# ACTION HANDLER
# ------------------------------------------------------------

def handle_action(action):
    global page, battle, message

    if action is None:
        return

    if action == "BATTLE":
        start_battle()
    elif action == "COLLECTION":
        page = "collection"
    elif action == "EVOLVE":
        page = "evolve"
    elif action == "SHOP":
        page = "shop"
    elif action == "HOME":
        page = "home"
    elif action == "SAVE":
        save_game()
        message = "Game saved!"
    elif action == "HEAL":
        c = selected_creature()
        c["hp"] = c["max_hp"]
        message = "Creature healed!"
        save_game()
    elif action == "FAVORITE":
        c = selected_creature()
        c["favorite"] = not c.get("favorite", False)
        save_game()
    elif action == "EVOLVE_NOW":
        c = selected_creature()
        if c["stage"] >= 2:
            message = "Already fully evolved."
        else:
            cost = [100, 250][c["stage"]]
            if game["coins"] < cost:
                message = "Not enough coins!"
            else:
                game["coins"] -= cost
                c["stage"] += 1
                update_stats(c, True)
                burst(330, 340, ELEMENTS[c["element"]]["color"], 40)
                message = f"{c['name']} evolved!"
                save_game()
    elif action == "BUY_1":
        if game["coins"] >= 25:
            game["coins"] -= 25
            game["orbs"] += 1
            message = "Bought 1 orb."
        else:
            message = "Not enough coins!"
        save_game()
    elif action == "BUY_5":
        if game["coins"] >= 100:
            game["coins"] -= 100
            game["orbs"] += 5
            message = "Bought 5 orbs."
        else:
            message = "Not enough coins!"
        save_game()
    elif action == "CAPTURE":
        try_capture()
    elif action == "BATTLE_HEAL":
        player = next((c for c in game["creatures"]
                       if c["id"] == battle["player_id"]), None)
        if player and game["coins"] >= 30:
            game["coins"] -= 30
            amount = int(player["max_hp"]*.4)
            player["hp"] = min(player["max_hp"], player["hp"]+amount)
            floater(f"+{amount} HP", 315, 250, GREEN)
            message = f"Recovered {amount} HP!"
            enemy_attack()
            save_game()
        else:
            message = "You need 30 coins."
    elif action == "RUN":
        page = "home"
        battle = None
        message = "You escaped."
    elif action == "QUIT":
        save_game()
        pygame.quit()
        raise SystemExit
    elif isinstance(action, str) and action.startswith("SKILL_"):
        try:
            perform_move(int(action.split("_", 1)[1]))
        except (ValueError, IndexError):
            pass
    elif isinstance(action, str) and action.startswith("SELECT_"):
        try:
            cid = int(action.split("_", 1)[1])
            if any(c["id"] == cid for c in game["creatures"]):
                game["selected"] = cid
                message = "Battle partner selected."
                save_game()
        except ValueError:
            pass
    elif isinstance(action, str) and action.startswith("FAV_"):
        try:
            cid = int(action.split("_", 1)[1])
            c = next((c for c in game["creatures"] if c["id"] == cid), None)
            if c:
                c["favorite"] = not c.get("favorite", False)
                save_game()
        except ValueError:
            pass


# ------------------------------------------------------------
# MAIN LOOP
# ------------------------------------------------------------

running = True

while running:
    dt = min(clock.tick(60)/1000.0, .05)
    update_effects(dt)

    if page == "battle":
        update_battle(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if page == "battle":
                    page = "home"
                    battle = None
                elif page != "home":
                    page = "home"
                else:
                    save_game()
                    running = False

            elif page == "battle" and battle is not None:
                if event.key == pygame.K_1:
                    perform_move(0)
                elif event.key == pygame.K_2:
                    perform_move(1)
                elif event.key == pygame.K_3:
                    perform_move(2)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_action(clicked_action(event.pos))

    if page == "home":
        home_screen()
    elif page == "battle" and battle is not None:
        battle_screen()
    elif page == "collection":
        collection_screen()
    elif page == "evolve":
        evolve_screen()
    elif page == "shop":
        shop_screen()
    else:
        page = "home"
        home_screen()

    draw_skill_effects()

    if message:
        rounded(screen, (12, 17, 30), (280, 710, 560, 36), 10)
        text(screen, message, 560, 728, SMALL, WHITE, True)

    pygame.display.flip()

save_game()
pygame.quit()
