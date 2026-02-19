import pygame
import sys
import random
import json
import os
import math

SAVE_FILE = 'save.json'


def load_state():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
                # Ensure owned_skins exists
                if 'owned_skins' not in data:
                    data['owned_skins'] = ['default']
                return data
        except Exception:
            return {'coins': 0, 'weapon_unlocked': False, 'skin': 'default', 'owned_skins': ['default'], 'zombies_killed': 0, 'turret_owned': False, 'tower_owned': False}
    return {'coins': 0, 'weapon_unlocked': False, 'skin': 'default', 'owned_skins': ['default'], 'zombies_killed': 0, 'turret_owned': False, 'tower_owned': False}


def save_state(state):
    with open(SAVE_FILE, 'w') as f:
        json.dump(state, f)


def draw_player(surface, player, facing, skin_name):
    x, y, w, h = player.x, player.y, player.w, player.h
    
    # Default Colors
    c_skin = (255, 220, 170)
    c_shirt = (200, 200, 200)
    c_pants = (100, 100, 100)
    c_hair = (50, 50, 50)
    c_shoes = (50, 50, 50)
    has_hair = True
    hair_style = 'flat' # flat, spiky, bald, hat, helmet
    
    # --- PALETTES & CONFIG ---
    if skin_name == 'default':
        c_shirt = (255, 220, 150)
        c_pants = (200, 160, 110)
    elif skin_name == 'blue':
        c_shirt = (100, 180, 255)
        c_pants = (70, 120, 180)
    elif skin_name == 'green':
        c_shirt = (140, 255, 140)
        c_pants = (90, 180, 90)
    
    # Anime
    elif skin_name == 'naruto':
        c_shirt = (255, 140, 0); c_pants = (255, 140, 0); c_hair = (255, 255, 0); hair_style = 'spiky'; c_shoes = (0, 0, 150)
    elif skin_name == 'sasuke':
        c_shirt = (200, 200, 255); c_pants = (240, 240, 240); c_hair = (20, 20, 40); hair_style = 'spiky'
    elif skin_name == 'luffy':
        c_shirt = (200, 50, 50); c_pants = (50, 100, 200); c_hair = (20, 20, 20); hair_style = 'hat_straw'
    elif skin_name == 'zoro':
        c_shirt = (240, 240, 240); c_pants = (30, 80, 30); c_hair = (50, 200, 50); hair_style = 'spiky'
    elif skin_name == 'tanjiro':
        c_shirt = (30, 180, 30); c_pants = (20, 20, 20); c_hair = (100, 20, 20); hair_style = 'spiky'
    elif skin_name == 'saitama':
        c_shirt = (255, 255, 0); c_pants = (255, 255, 0); has_hair = False; c_shoes = (200, 50, 50) # Cape logic needed?
    elif skin_name == 'deku':
        c_shirt = (30, 100, 80); c_pants = (30, 100, 80); c_hair = (20, 80, 40); hair_style = 'spiky'
    
    # Games
    elif skin_name == 'mario':
        c_shirt = (255, 0, 0); c_pants = (0, 0, 200); c_hair = (80, 40, 0); hair_style = 'hat_red'
    elif skin_name == 'luigi':
        c_shirt = (0, 200, 0); c_pants = (0, 0, 200); c_hair = (80, 40, 0); hair_style = 'hat_green'
    elif skin_name == 'steve':
        c_shirt = (0, 150, 150); c_pants = (0, 0, 150); c_hair = (60, 40, 20); c_skin = (200, 150, 120)
    elif skin_name == 'zombie_mc':
        c_skin = (50, 150, 50); c_shirt = (0, 150, 150); c_pants = (0, 0, 150); c_hair = (30, 80, 30)
    elif skin_name == 'creeper':
        c_skin = (50, 200, 50); c_shirt = (50, 200, 50); c_pants = (50, 200, 50); has_hair = False
    elif skin_name == 'link':
        c_shirt = (0, 200, 0); c_pants = (240, 240, 240); c_hair = (255, 255, 0); hair_style = 'hat_green_long'
    elif skin_name == 'sans':
        c_skin = (255, 255, 255); c_shirt = (50, 100, 255); c_pants = (20, 20, 20); has_hair = False
    elif skin_name == 'master_chief':
        c_skin = (20, 20, 20); c_shirt = (50, 100, 50); c_pants = (50, 100, 50); has_hair = False; hair_style = 'helmet_gold'
    elif skin_name == 'kratos':
        c_skin = (220, 220, 220); c_shirt = (100, 50, 50); c_pants = (80, 60, 40); has_hair = False; # Beard?
    
    # Heroes
    elif skin_name == 'spiderman':
        c_skin = (200, 0, 0); c_shirt = (200, 0, 0); c_pants = (0, 0, 200); has_hair = False; # Mask
    elif skin_name == 'ironman':
        c_skin = (200, 0, 0); c_shirt = (200, 0, 0); c_pants = (200, 0, 0); has_hair = False; hair_style = 'helmet_gold_face'
    elif skin_name == 'captain_america':
        c_skin = (0, 0, 200); c_shirt = (0, 0, 200); c_pants = (0, 0, 200); has_hair = False; # Mask
    elif skin_name == 'hulk':
        c_skin = (50, 200, 50); c_shirt = (50, 200, 50); c_pants = (100, 50, 150); c_hair = (20, 20, 20)
    elif skin_name == 'batman':
        c_skin = (200, 180, 150); c_shirt = (50, 50, 50); c_pants = (50, 50, 50); has_hair = False; hair_style = 'cowl_black'
    elif skin_name == 'superman':
        c_shirt = (0, 0, 200); c_pants = (0, 0, 200); c_hair = (20, 20, 20); # Cape
    elif skin_name == 'deadpool':
        c_skin = (200, 0, 0); c_shirt = (200, 0, 0); c_pants = (20, 20, 20); has_hair = False
    elif skin_name == 'joker':
        c_skin = (255, 255, 255); c_shirt = (100, 0, 150); c_pants = (100, 0, 150); c_hair = (50, 200, 50)
    
    # Cartoons/Movies
    elif skin_name == 'homer':
        c_skin = (255, 255, 0); c_shirt = (255, 255, 255); c_pants = (100, 150, 255); has_hair = False
    elif skin_name == 'bart':
        c_skin = (255, 255, 0); c_shirt = (255, 100, 0); c_pants = (50, 100, 200); c_hair = (255, 255, 0); hair_style = 'spiky'
    elif skin_name == 'shrek':
        c_skin = (150, 200, 50); c_shirt = (240, 230, 200); c_pants = (100, 80, 50); has_hair = False
    elif skin_name == 'rick':
        c_skin = (220, 200, 180); c_shirt = (180, 220, 240); c_pants = (100, 80, 60); c_hair = (180, 220, 255); hair_style = 'spiky'
    elif skin_name == 'morty':
        c_skin = (220, 200, 180); c_shirt = (255, 255, 0); c_pants = (0, 0, 150); c_hair = (100, 80, 50)
    elif skin_name == 'walter_white':
        c_skin = (220, 200, 180); c_shirt = (50, 100, 50); c_pants = (200, 180, 150); has_hair = False; # Hat?
    elif skin_name == 'john_wick':
        c_skin = (220, 200, 180); c_shirt = (20, 20, 20); c_pants = (20, 20, 20); c_hair = (20, 20, 20); hair_style = 'long'
    
    # Generic / Teams
    elif skin_name.startswith('soldier_'):
        color_map = {'red': (150, 50, 50), 'blue': (50, 50, 150), 'green': (50, 100, 50), 'black': (30, 30, 30), 'white': (220, 220, 220)}
        col = skin_name.split('_')[1]
        base = color_map.get(col, (100, 100, 100))
        c_shirt = base; c_pants = (base[0]//2, base[1]//2, base[2]//2); hair_style = 'helmet_' + col
    elif skin_name.startswith('ninja_'):
        color_map = {'red': (150, 0, 0), 'blue': (0, 0, 150), 'black': (20, 20, 20), 'white': (240, 240, 240)}
        col = skin_name.split('_')[1]
        base = color_map.get(col, (40, 40, 40))
        c_shirt = base; c_pants = base; c_skin = base; has_hair = False; # Masked
    
    # --- DRAWING ---
    
    # Special Custom Drawers
    if skin_name == 'goku':
        # ... (Keep existing Goku logic here or copy it)
        # For brevity in this function, I will reimplement Goku here to keep it self-contained
        pygame.draw.rect(surface, (255, 140, 0), (x, y + 4, w, h - 4)) # Gi
        pygame.draw.rect(surface, (0, 0, 200), (x + 2, y + 4, w - 4, 4)) # Undershirt
        pygame.draw.rect(surface, (0, 0, 200), (x, y + 10, w, 2)) # Sash
        pygame.draw.rect(surface, (255, 220, 170), (x + 2, y - 6, w - 4, 8)) # Head
        # Hair (Anime)
        pygame.draw.rect(surface, (0, 0, 0), (x + 1, y - 8, w - 2, 4))
        pygame.draw.polygon(surface, (0, 0, 0), [(x, y-6), (x-4, y-8), (x+2, y-10)])
        pygame.draw.polygon(surface, (0, 0, 0), [(x+2, y-8), (x-2, y-12), (x+4, y-10)])
        pygame.draw.polygon(surface, (0, 0, 0), [(x+w, y-6), (x+w+4, y-8), (x+w-2, y-10)])
        pygame.draw.polygon(surface, (0, 0, 0), [(x+w-2, y-8), (x+w+2, y-12), (x+w-4, y-10)])
        pygame.draw.polygon(surface, (0, 0, 0), [(player.centerx-2, y-8), (player.centerx, y-14), (player.centerx+2, y-8)])
        ex = x + (w - 5 if facing == 1 else 1)
        surface.fill((0, 0, 0), (ex, y - 4, 2, 2))
        pygame.draw.rect(surface, (0, 0, 150), (x + 2, y + h - 2, 4, 4)) # Boots
        pygame.draw.rect(surface, (0, 0, 150), (x + w - 6, y + h - 2, 4, 4))
        return

    elif skin_name == 'vegeta':
        # Reimplement Vegeta
        pygame.draw.rect(surface, (0, 0, 150), (x, y + 4, w, h - 4)) # Body
        pygame.draw.rect(surface, (240, 240, 240), (x, y + 4, w, 8)) # Armor
        pygame.draw.rect(surface, (218, 165, 32), (x + 2, y + 4, w - 4, 2)) # Straps
        pygame.draw.rect(surface, (255, 220, 170), (x + 2, y - 6, w - 4, 8)) # Head
        # Hair (Flame)
        pygame.draw.polygon(surface, (0, 0, 0), [(x, y - 6), (player.centerx, y - 4), (x + w, y - 6), (player.centerx, y - 8)])
        pygame.draw.polygon(surface, (0, 0, 0), [(x, y - 6), (x - 2, y - 12), (player.centerx, y - 18), (x + w + 2, y - 12), (x + w, y - 6)])
        ex = x + (w - 5 if facing == 1 else 1)
        surface.fill((0, 0, 0), (ex, y - 3, 2, 1))
        pygame.draw.rect(surface, (240, 240, 240), (x + 2, y + h - 2, 4, 4))
        pygame.draw.rect(surface, (240, 240, 240), (x + w - 6, y + h - 2, 4, 4))
        return

    elif skin_name == 'spongebob':
        # Reimplement Spongebob
        pygame.draw.rect(surface, (255, 255, 0), (x, y - 6, w, h - 2))
        pygame.draw.circle(surface, (200, 200, 0), (x + 3, y), 1)
        pygame.draw.circle(surface, (200, 200, 0), (x + w - 3, y + 5), 1)
        pygame.draw.rect(surface, (255, 255, 255), (x, y + h - 8, w, 4))
        pygame.draw.rect(surface, (139, 69, 19), (x, y + h - 4, w, 4))
        ex = x + (w - 8 if facing == 1 else 2)
        pygame.draw.circle(surface, (255, 255, 255), (ex + 2, y - 2), 3)
        pygame.draw.circle(surface, (50, 150, 255), (ex + 2, y - 2), 1)
        pygame.draw.rect(surface, (255, 255, 0), (x + 3, y + h - 2, 2, 4))
        pygame.draw.rect(surface, (255, 255, 0), (x + w - 5, y + h - 2, 2, 4))
        return

    # Standard Humanoid Drawing
    
    # 1. Legs/Pants (with shading)
    pygame.draw.rect(surface, c_pants, (x, y + 10, w, h - 10))
    # Shading on pants (side away from facing)
    shade_x = x if facing == 1 else x + w - 2
    pygame.draw.rect(surface, (max(0, c_pants[0]-30), max(0, c_pants[1]-30), max(0, c_pants[2]-30)), (shade_x, y + 10, 2, h - 10))
    # Center seam
    pygame.draw.rect(surface, (max(0, c_pants[0]-20), max(0, c_pants[1]-20), max(0, c_pants[2]-20)), (x + w//2 - 1, y + 12, 2, h - 12))

    # 2. Shirt/Body (with shading)
    pygame.draw.rect(surface, c_shirt, (x, y + 4, w, 6))
    # Shading on shirt
    pygame.draw.rect(surface, (max(0, c_shirt[0]-30), max(0, c_shirt[1]-30), max(0, c_shirt[2]-30)), (shade_x, y + 4, 2, 6))
    
    # 3. Arms (Simple sleeves)
    arm_color = c_shirt
    if facing == 1:
        # Right arm (front)
        pygame.draw.rect(surface, arm_color, (x + 4, y + 5, 3, 4))
        # Left arm (back) - slightly darker
        pygame.draw.rect(surface, (max(0, arm_color[0]-20), max(0, arm_color[1]-20), max(0, arm_color[2]-20)), (x - 2, y + 5, 2, 4))
    else:
        # Left arm (front)
        pygame.draw.rect(surface, arm_color, (x + 5, y + 5, 3, 4))
        # Right arm (back)
        pygame.draw.rect(surface, (max(0, arm_color[0]-20), max(0, arm_color[1]-20), max(0, arm_color[2]-20)), (x + w, y + 5, 2, 4))

    # 4. Head (with shading)
    pygame.draw.rect(surface, c_skin, (x + 2, y - 6, w - 4, 8))
    # Shading on face
    face_shade_x = x + 2 if facing == 1 else x + w - 4
    pygame.draw.rect(surface, (max(0, c_skin[0]-20), max(0, c_skin[1]-20), max(0, c_skin[2]-20)), (face_shade_x, y - 6, 2, 8))

    # 5. Belt (if shirt and pants are different)
    if c_shirt != c_pants:
        pygame.draw.rect(surface, (30, 30, 30), (x, y + 9, w, 1))
        pygame.draw.rect(surface, (180, 180, 180), (x + w//2 - 1, y + 9, 2, 1)) # Buckle

    # Hair / Hat
    if has_hair:
        if hair_style == 'flat':
            pygame.draw.rect(surface, c_hair, (x + 2, y - 8, w - 4, 2))
            pygame.draw.rect(surface, c_hair, (x + 1, y - 7, w - 2, 2))
        elif hair_style == 'spiky':
            pygame.draw.polygon(surface, c_hair, [(x, y-6), (x+2, y-9), (x+4, y-6)])
            pygame.draw.polygon(surface, c_hair, [(x+w, y-6), (x+w-2, y-9), (x+w-4, y-6)])
            pygame.draw.polygon(surface, c_hair, [(player.centerx-2, y-6), (player.centerx, y-10), (player.centerx+2, y-6)])
        elif hair_style == 'hat_red': # Mario
            pygame.draw.rect(surface, (255, 0, 0), (x + 1, y - 8, w - 2, 3))
            pygame.draw.rect(surface, (255, 0, 0), (x + (w if facing==1 else -2), y - 7, 4, 2)) # Brim
        elif hair_style == 'hat_green': # Luigi
            pygame.draw.rect(surface, (0, 200, 0), (x + 1, y - 8, w - 2, 3))
            pygame.draw.rect(surface, (0, 200, 0), (x + (w if facing==1 else -2), y - 7, 4, 2))
        elif hair_style == 'hat_straw': # Luffy
            pygame.draw.rect(surface, (220, 200, 100), (x, y - 8, w, 2))
            pygame.draw.rect(surface, (200, 50, 50), (x + 2, y - 9, w - 4, 2)) # Band
        elif hair_style == 'hat_green_long': # Link
            pygame.draw.polygon(surface, (0, 200, 0), [(x+1, y-6), (player.centerx, y-12), (x+w-1, y-6)])
        elif hair_style.startswith('helmet_'):
            # Simple helmet
            col = c_shirt # Match shirt usually
            pygame.draw.rect(surface, col, (x + 1, y - 8, w - 2, 4))
            pygame.draw.rect(surface, (0, 0, 0), (x + 4, y - 6, 4, 2)) # Visor
        elif hair_style == 'cowl_black': # Batman
            pygame.draw.rect(surface, (20, 20, 20), (x + 1, y - 9, w - 2, 5))
            pygame.draw.polygon(surface, (20, 20, 20), [(x+1, y-9), (x+1, y-12), (x+3, y-9)]) # Ears
            pygame.draw.polygon(surface, (20, 20, 20), [(x+w-1, y-9), (x+w-1, y-12), (x+w-3, y-9)])

    # Eyes
    ex = x + (w - 6 if facing == 1 else 2)
    if skin_name == 'spiderman' or skin_name == 'deadpool':
        pygame.draw.rect(surface, (255, 255, 255), (ex, y - 5, 4, 3)) # Big white eyes
    elif skin_name == 'ironman':
        pygame.draw.rect(surface, (150, 255, 255), (ex, y - 5, 4, 2)) # Glowing eyes
    elif skin_name == 'batman':
        pygame.draw.rect(surface, (255, 255, 255), (ex, y - 4, 3, 2))
    elif skin_name == 'sans':
        pygame.draw.rect(surface, (0, 0, 0), (ex, y - 5, 4, 4)) # Sockets
        pygame.draw.rect(surface, (255, 255, 255), (ex+1, y - 4, 1, 1)) # Pupil
    else:
        # Standard eyes with whites
        pygame.draw.rect(surface, (255, 255, 255), (ex, y - 4, 3, 3))
        pygame.draw.rect(surface, (20, 20, 20), (ex + (1 if facing == 1 else 0), y - 3, 2, 2))

    # Shoes (Detailed)
    pygame.draw.rect(surface, c_shoes, (x + 2, y + h - 2, 4, 4))
    pygame.draw.rect(surface, c_shoes, (x + w - 6, y + h - 2, 4, 4))
    # Shoe laces/detail
    pygame.draw.rect(surface, (200, 200, 200), (x + 3, y + h - 2, 2, 1))
    pygame.draw.rect(surface, (200, 200, 200), (x + w - 5, y + h - 2, 2, 1))


def main():
    pygame.init()
    SCALE = 2
    W, H = 320, 180
    SCREEN = pygame.display.set_mode((W * SCALE, H * SCALE))
    pygame.display.set_caption('Zombie Pixel Shooter (Python)')
    clock = pygame.time.Clock()

    surface = pygame.Surface((W, H))

    state = load_state()
    coins = state.get('coins', 0)
    # weapon index: 0 = default pistol. Keep backward compatibility with old 'weapon_unlocked'.
    if 'weapon_idx' in state:
        weapon_idx = state.get('weapon_idx', 0)
    else:
        weapon_idx = 1 if state.get('weapon_unlocked', False) else 0
    skin = state.get('skin', 'default')

    GROUND_Y = H - 30
    player = pygame.Rect(20, GROUND_Y - 16, 12, 16)
    GRAVITY = 0.6
    JUMP_V = -8
    MOVE_SPEED = 1.8
    player_vy = 0
    on_ground = True
    crouched = False

    bullets = []
    zombies = []
    drops = []

    lives = 2
    game_over = False
    hit_cooldown = 0

    spawn_timer = 0

    font = pygame.font.SysFont('Consolas', 10)

    skins = [
        'default', 'blue', 'green', 'goku', 'spongebob', 'vegeta',
        'naruto', 'sasuke', 'luffy', 'zoro', 'tanjiro', 'saitama', 'deku',
        'mario', 'luigi', 'steve', 'zombie_mc', 'creeper', 'link', 'sans', 'master_chief', 'kratos',
        'spiderman', 'ironman', 'captain_america', 'hulk', 'batman', 'superman', 'deadpool', 'joker',
        'homer', 'bart', 'shrek', 'rick', 'morty', 'walter_white', 'john_wick',
        'soldier_green', 'soldier_red', 'soldier_blue', 'soldier_black', 'soldier_white',
        'ninja_black', 'ninja_white', 'ninja_red', 'ninja_blue'
    ]
    SKIN_COSTS = {
        'default': 0,
        'blue': 1000, 'green': 1000,
        'goku': 3000, 'spongebob': 4000, 'vegeta': 5000,
        'naruto': 3000, 'sasuke': 3000, 'luffy': 3000, 'zoro': 3000, 'tanjiro': 3000, 'saitama': 5000, 'deku': 3000,
        'mario': 2000, 'luigi': 2000, 'steve': 2000, 'zombie_mc': 2000, 'creeper': 2500, 'link': 2500, 'sans': 2500, 'master_chief': 4000, 'kratos': 4000,
        'spiderman': 3500, 'ironman': 4000, 'captain_america': 3500, 'hulk': 4000, 'batman': 4000, 'superman': 5000, 'deadpool': 3500, 'joker': 3500,
        'homer': 2000, 'bart': 2000, 'shrek': 3000, 'rick': 3000, 'morty': 2000, 'walter_white': 3000, 'john_wick': 3500,
        'soldier_green': 1500, 'soldier_red': 1500, 'soldier_blue': 1500, 'soldier_black': 1500, 'soldier_white': 1500,
        'ninja_black': 2000, 'ninja_white': 2000, 'ninja_red': 2000, 'ninja_blue': 2000
    }
    skin_idx = skins.index(skin) if skin in skins else 0
    owned_skins = state.get('owned_skins', ['default'])
    zombies_killed = state.get('zombies_killed', 0)
    turret_owned = state.get('turret_owned', False)
    tower_owned = state.get('tower_owned', False)
    
    # spawn tuning: more zombies but capped to avoid overwhelming player
    MAX_ZOMBIES = 12
    SPAWN_INTERVAL = 800  # milliseconds between spawns (slower)
    current_spawn_interval = SPAWN_INTERVAL
    BOOST_DURATION = 8000  # ms boost after unpausing
    boost_timer = 0
    paused = False
    game_state = 'play' # play, shop_weapon, shop_skin
    shop_idx = 0 # Used for browsing in shops
    
    # Boss & Turret
    boss = None
    boss_defeated = False
    turret_cooldown = 0
    TURRET_COST = 50000
    TOWER_COST = 5000
    BOSS_TRIGGER = 100000
    
    # weapons: name, cost, bullet speed, penetration
    # weapons: name, cost, bullet speed, penetration
    WEAPONS = [
        {'name': 'Pistol', 'cost': 0, 'speed': 8, 'pen': 1},
        {'name': 'SMG', 'cost': 100, 'speed': 12, 'pen': 1},
        {'name': 'Shotgun', 'cost': 200, 'speed': 10, 'pen': 2},
        {'name': 'Rifle', 'cost': 400, 'speed': 14, 'pen': 2},
        {'name': 'Sniper', 'cost': 800, 'speed': 20, 'pen': 5},
        {'name': 'Minigun', 'cost': 1600, 'speed': 16, 'pen': 3},
        {'name': 'Laser', 'cost': 3200, 'speed': 22, 'pen': 4},
        {'name': 'Plasma', 'cost': 6400, 'speed': 18, 'pen': 6},
        {'name': 'Grenade', 'cost': 12800, 'speed': 12, 'pen': 10},
        {'name': 'Railgun', 'cost': 25600, 'speed': 30, 'pen': 100},
    ]

    def draw_gun(surface, x, y, facing, weapon_name):
        # x, y is the hand position roughly
        # facing: 1 (right), -1 (left)
        
        if weapon_name == 'Pistol':
            w, h = 8, 4
            dx = 0 if facing == 1 else -w
            pygame.draw.rect(surface, (50, 50, 50), (x + dx, y, w, h))
            pygame.draw.rect(surface, (30, 30, 30), (x + (dx + w - 2 if facing == 1 else dx), y, 2, h))

        elif weapon_name == 'SMG':
            w, h = 10, 5
            dx = 0 if facing == 1 else -w
            pygame.draw.rect(surface, (40, 40, 40), (x + dx, y, w, h))
            mag_x = x + (4 if facing == 1 else -6)
            pygame.draw.rect(surface, (20, 20, 20), (mag_x, y + 3, 3, 4))

        elif weapon_name == 'Shotgun':
            w, h = 14, 4
            dx = 0 if facing == 1 else -w
            pygame.draw.rect(surface, (100, 60, 30), (x + dx, y, 4, h)) # Stock
            barrel_x = x + (4 if facing == 1 else -w)
            pygame.draw.rect(surface, (60, 60, 60), (barrel_x, y, 10, 3)) # Barrel
            pump_x = x + (8 if facing == 1 else -10)
            pygame.draw.rect(surface, (40, 30, 20), (pump_x, y + 1, 4, 3))

        elif weapon_name == 'Rifle':
            w, h = 16, 4
            dx = 0 if facing == 1 else -w
            pygame.draw.rect(surface, (30, 30, 30), (x + dx, y, w, h))
            mag_x = x + (6 if facing == 1 else -8)
            pygame.draw.rect(surface, (10, 10, 10), (mag_x, y + 2, 3, 4))

        elif weapon_name == 'Sniper':
            w, h = 20, 3
            dx = 0 if facing == 1 else -w
            pygame.draw.rect(surface, (40, 50, 40), (x + dx, y, w, h))
            scope_x = x + (4 if facing == 1 else -10)
            pygame.draw.rect(surface, (10, 10, 10), (scope_x, y - 2, 6, 2))

        elif weapon_name == 'Minigun':
            w, h = 18, 8
            dx = 0 if facing == 1 else -w
            pygame.draw.rect(surface, (50, 50, 50), (x + dx, y - 2, 6, 8))
            bx = x + (6 if facing == 1 else -w)
            pygame.draw.rect(surface, (80, 80, 80), (bx, y - 1, 12, 2))
            pygame.draw.rect(surface, (80, 80, 80), (bx, y + 2, 12, 2))
            pygame.draw.rect(surface, (80, 80, 80), (bx, y + 5, 12, 2))

        elif weapon_name == 'Laser':
            w, h = 14, 5
            dx = 0 if facing == 1 else -w
            pygame.draw.rect(surface, (200, 200, 200), (x + dx, y, w, h))
            pygame.draw.rect(surface, (0, 255, 255), (x + (dx + 2 if facing == 1 else dx + 2), y + 1, w - 4, 1))

        elif weapon_name == 'Plasma':
            w, h = 12, 6
            dx = 0 if facing == 1 else -w
            pygame.draw.rect(surface, (100, 0, 150), (x + dx, y, w, h))
            pygame.draw.circle(surface, (0, 255, 0), (int(x + (dx + 4 if facing == 1 else dx + 8)), int(y + 3)), 2)
            pygame.draw.circle(surface, (0, 255, 0), (int(x + (dx + 8 if facing == 1 else dx + 4)), int(y + 3)), 2)

        elif weapon_name == 'Grenade':
            w, h = 12, 6
            dx = 0 if facing == 1 else -w
            pygame.draw.rect(surface, (60, 70, 60), (x + dx, y, w, h))
            pygame.draw.circle(surface, (20, 20, 20), (int(x + (dx + w if facing == 1 else dx)), int(y + 3)), 3)

        elif weapon_name == 'Railgun':
            w, h = 22, 5
            dx = 0 if facing == 1 else -w
            pygame.draw.rect(surface, (20, 20, 50), (x + dx, y + 1, w, 3))
            pygame.draw.rect(surface, (100, 100, 255), (x + dx, y - 1, w, 1))
            pygame.draw.rect(surface, (100, 100, 255), (x + dx, y + 5, w, 1))

        else:
            w, h = 10, 4
            dx = 0 if facing == 1 else -w
            pygame.draw.rect(surface, (60, 60, 60), (x + dx, y, w, h))

    def spawn_zombie():
        z_w, z_h = 14, 18
        y = GROUND_Y - z_h
        # Spawn from left or right randomly
        if random.random() < 0.5:
            start_x = -20
        else:
            start_x = W + 10
        rect = pygame.Rect(start_x, y, z_w, z_h)
        speed = 0.2 + random.random() * 0.3
        # assign rarity by weight: common blue, uncommon orange, rare red
        # make green zombies more common, keep blue common too
        r = random.random()
        if r < 0.40:
            rarity = 'green'
        elif r < 0.70:
            rarity = 'blue'
        elif r < 0.90:
            rarity = 'orange'
        else:
            rarity = 'red'
        zombies.append({'rect': rect, 'speed': speed, 'rarity': rarity, 'pos_x': float(start_x)})

    facing = 1

    def shoot(target_x=None, target_y=None):
        nonlocal facing
        if target_x is not None:
            facing = 1 if target_x >= player.centerx else -1
        
        w_data = WEAPONS[weapon_idx]
        speed = w_data['speed']
        w_name = w_data['name']
        
        if facing == 1:
            bx = player.right + 1
        else:
            bx = player.left - 7
        by = player.centery - 2
        
        # Bullet size/shape based on weapon
        bw, bh = 6, 4
        if w_name == 'Sniper': bw, bh = 8, 3
        elif w_name == 'Minigun': bw, bh = 5, 3
        elif w_name == 'Laser': bw, bh = 12, 2
        elif w_name == 'Plasma': bw, bh = 6, 6
        elif w_name == 'Grenade': bw, bh = 8, 8
        elif w_name == 'Railgun': bw, bh = 20, 4
        
        b = pygame.Rect(int(bx), int(by), bw, bh)
        pen = w_data.get('pen', 1)
        
        vx = speed * facing
        vy = 0
        
        if target_x is not None and target_y is not None:
            dx = target_x - bx
            dy = target_y - by
            dist = math.hypot(dx, dy)
            if dist != 0:
                vx = (dx / dist) * speed
                vy = (dy / dist) * speed

        bullets.append({'rect': b, 'x': float(bx), 'y': float(by), 'vx': vx, 'vy': vy, 'pen': pen, 'type': w_name})

    running = True
    while running:
        dt = clock.tick(60)
        if game_state == 'play' and not paused and not game_over:
            spawn_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_state({'coins': coins, 'weapon_idx': weapon_idx, 'skin': skins[skin_idx], 'owned_skins': owned_skins, 'zombies_killed': zombies_killed, 'turret_owned': turret_owned, 'tower_owned': tower_owned})
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_over and game_state == 'play':
                    mx, my = pygame.mouse.get_pos()
                    mx = int(mx / SCALE)
                    my = int(my / SCALE)
                    shoot(mx, my)
            elif event.type == pygame.KEYDOWN:
                if game_state == 'play':
                    if event.key == pygame.K_w and on_ground and not game_over:
                        player_vy = JUMP_V
                        on_ground = False
                    if event.key == pygame.K_t:
                        if not tower_owned and coins >= TOWER_COST:
                            coins -= TOWER_COST
                            tower_owned = True
                            save_state({'coins': coins, 'weapon_idx': weapon_idx, 'skin': skins[skin_idx], 'owned_skins': owned_skins, 'zombies_killed': zombies_killed, 'turret_owned': turret_owned, 'tower_owned': tower_owned})
                        elif tower_owned and not turret_owned and coins >= TURRET_COST:
                            coins -= TURRET_COST
                            turret_owned = True
                            save_state({'coins': coins, 'weapon_idx': weapon_idx, 'skin': skins[skin_idx], 'owned_skins': owned_skins, 'zombies_killed': zombies_killed, 'turret_owned': turret_owned, 'tower_owned': tower_owned})
                    if event.key == pygame.K_SPACE:
                        # toggle pause; when unpausing, spawn a small burst and boost spawn rate temporarily
                        paused = not paused
                        if not paused:
                            boost_timer = BOOST_DURATION
                            current_spawn_interval = max(150, SPAWN_INTERVAL // 3)
                            # immediate burst up to 8 zombies without exceeding MAX_ZOMBIES
                            can_spawn = MAX_ZOMBIES - len(zombies)
                            burst = min(8, can_spawn)
                            for _ in range(burst):
                                spawn_zombie()
                    if event.key == pygame.K_r and game_over:
                        lives = 2
                        game_over = False
                        zombies.clear()
                        bullets.clear()
                        drops.clear()
                        spawn_timer = 0
                        boss = None
                        boss_defeated = False

                # Global toggles (or context sensitive)
                if event.key == pygame.K_u and not game_over:
                    if game_state == 'shop_weapon':
                        game_state = 'play'
                    else:
                        game_state = 'shop_weapon'
                        shop_idx = weapon_idx # Start at current weapon
                        
                if event.key == pygame.K_c and not game_over:
                    if game_state == 'shop_skin':
                        game_state = 'play'
                    else:
                        game_state = 'shop_skin'
                        shop_idx = skin_idx # Start at current skin

                # Shop Inputs
                if game_state == 'shop_weapon':
                    if event.key == pygame.K_LEFT:
                        shop_idx = max(0, shop_idx - 1)
                    if event.key == pygame.K_RIGHT:
                        shop_idx = min(len(WEAPONS) - 1, shop_idx + 1)
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # Buy/Equip logic
                        if shop_idx <= weapon_idx:
                            # Already owned, just equip (though weapon logic is linear, so this is just 'equipped')
                            weapon_idx = shop_idx
                            save_state({'coins': coins, 'weapon_idx': weapon_idx, 'skin': skins[skin_idx], 'owned_skins': owned_skins, 'zombies_killed': zombies_killed, 'turret_owned': turret_owned, 'tower_owned': tower_owned})
                        elif shop_idx == weapon_idx + 1:
                             cost = WEAPONS[shop_idx]['cost']
                             if coins >= cost:
                                 coins -= cost
                                 weapon_idx = shop_idx
                                 save_state({'coins': coins, 'weapon_idx': weapon_idx, 'skin': skins[skin_idx], 'owned_skins': owned_skins, 'zombies_killed': zombies_killed, 'turret_owned': turret_owned, 'tower_owned': tower_owned})
                
                if game_state == 'shop_skin':
                    if event.key == pygame.K_LEFT:
                        shop_idx = (shop_idx - 1) % len(skins)
                    if event.key == pygame.K_RIGHT:
                        shop_idx = (shop_idx + 1) % len(skins)
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # Buy/Equip
                        s_name = skins[shop_idx]
                        if s_name in owned_skins:
                            # Already owned, just equip
                            skin_idx = shop_idx
                            skin = s_name
                            save_state({'coins': coins, 'weapon_idx': weapon_idx, 'skin': skin, 'owned_skins': owned_skins, 'zombies_killed': zombies_killed, 'turret_owned': turret_owned, 'tower_owned': tower_owned})
                        else:
                            cost = SKIN_COSTS.get(s_name, 0)
                            if coins >= cost:
                                coins -= cost
                                owned_skins.append(s_name)
                                skin_idx = shop_idx
                                skin = s_name
                                save_state({'coins': coins, 'weapon_idx': weapon_idx, 'skin': skin, 'owned_skins': owned_skins, 'zombies_killed': zombies_killed, 'turret_owned': turret_owned, 'tower_owned': tower_owned})

        if game_state == 'play' and not game_over and not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                player.x += MOVE_SPEED * dt / 16
                facing = 1
            if keys[pygame.K_a]:
                player.x -= MOVE_SPEED * dt / 16
                facing = -1
            if keys[pygame.K_s]:
                if not crouched:
                    crouched = True
                    player.h = 8
                    player.y += 8
            else:
                if crouched:
                    crouched = False
                    player.y -= 8
                    player.h = 16

            # Boss Logic
            if zombies_killed >= BOSS_TRIGGER and not boss and not boss_defeated:
                # Spawn Boss
                boss = {'rect': pygame.Rect(W + 20, GROUND_Y - 60, 40, 60), 'hp': 5000, 'max_hp': 5000, 'speed': 0.5}
            
            if boss:
                # Move Boss
                if boss['rect'].centerx > player.centerx:
                    boss['rect'].x -= boss['speed'] * dt / 16
                else:
                    boss['rect'].x += boss['speed'] * dt / 16
                
                # Boss Collision with Player
                if hit_cooldown <= 0 and boss['rect'].colliderect(player):
                    lives = 0 # Instant kill or massive damage
                    game_over = True
                    weapon_idx = 0
                    coins = 0
                    save_state({'coins': coins, 'weapon_idx': weapon_idx, 'skin': skins[skin_idx], 'owned_skins': owned_skins, 'zombies_killed': zombies_killed, 'turret_owned': turret_owned, 'tower_owned': tower_owned})
                
                # Boss Collision with Bullets
                for b in bullets[:]:
                    if boss['rect'].colliderect(b['rect']):
                        # Damage Boss
                        dmg = 10 # Base damage
                        if b['type'] == 'Sniper': dmg = 50
                        elif b['type'] == 'Railgun': dmg = 200
                        elif b['type'] == 'Grenade': dmg = 100
                        elif b['type'] == 'Minigun': dmg = 5
                        
                        boss['hp'] -= dmg
                        
                        # Remove bullet (unless railgun penetrates)
                        if b['type'] != 'Railgun':
                            try:
                                bullets.remove(b)
                            except ValueError:
                                pass
                        
                        if boss['hp'] <= 0:
                            boss = None
                            boss_defeated = True
                            coins += 50000 # Boss reward
                            save_state({'coins': coins, 'weapon_idx': weapon_idx, 'skin': skins[skin_idx], 'owned_skins': owned_skins, 'zombies_killed': zombies_killed, 'turret_owned': turret_owned, 'tower_owned': tower_owned})
                        break

            # Turret Logic
            if turret_owned:
                # Teleport Logic (Base)
                turret_base_rect = pygame.Rect(30, GROUND_Y - 20, 20, 20)
                if player.colliderect(turret_base_rect) and player.bottom >= GROUND_Y - 5:
                    # Teleport to top
                    player.y = GROUND_Y - 20 - 8 - player.h # Top of head (ty - 8)
                    player_vy = 0
                    on_ground = True

                turret_cooldown -= dt
                if turret_cooldown <= 0:
                    # Find target
                    target = None
                    min_dist = 200
                    
                    # Target Boss first
                    if boss:
                        dist = abs(boss['rect'].centerx - 40) # Turret at x=40
                        if dist < min_dist:
                            target = boss['rect']
                    
                    # Target Zombies
                    if not target:
                        for z in zombies:
                            dist = abs(z['rect'].centerx - 40)
                            if dist < min_dist:
                                min_dist = dist
                                target = z['rect']
                    
                    if target:
                        # Shoot
                        turret_cooldown = 500 # Fire rate
                        bx, by = 40, GROUND_Y - 25
                        
                        tx, ty = target.centerx, target.centery
                        dx = tx - bx
                        dy = ty - by
                        dist = math.hypot(dx, dy)
                        speed = 10
                        vx = (dx / dist) * speed if dist != 0 else speed
                        vy = (dy / dist) * speed if dist != 0 else 0
                        
                        b = pygame.Rect(bx, by, 6, 4)
                        bullets.append({'rect': b, 'x': float(bx), 'y': float(by), 'vx': vx, 'vy': vy, 'pen': 1, 'type': 'Turret'})

            if spawn_timer > current_spawn_interval and len(zombies) < MAX_ZOMBIES and not boss:
                # spawn up to 4 zombies at once, but never exceed MAX_ZOMBIES
                can_spawn = MAX_ZOMBIES - len(zombies)
                spawn_count = min(4, can_spawn)
                for _ in range(spawn_count):
                    spawn_zombie()
                spawn_timer = 0

            player_vy += GRAVITY * (dt / 16)
            player.y += player_vy * (dt / 16)

            if turret_owned:
                turret_top_y = GROUND_Y - 28
                if 32 - player.w < player.x < 32 + 16:
                    if player.y + player.h >= turret_top_y and player.y + player.h <= turret_top_y + 10 and player_vy >= 0:
                        player.y = turret_top_y - player.h
                        player_vy = 0
                        on_ground = True

            if player.y + player.h >= GROUND_Y:
                player.y = GROUND_Y - player.h
                player_vy = 0
                on_ground = True

            if player.x < 0:
                player.x = 0
            if player.x + player.w > W:
                player.x = W - player.w

            for b in bullets[:]:
                b['x'] += b['vx']
                b['y'] += b['vy']
                b['rect'].x = int(b['x'])
                b['rect'].y = int(b['y'])
                
                if b['rect'].x > W or b['rect'].x < 0 or b['rect'].y > H or b['rect'].y < 0:
                    try:
                        bullets.remove(b)
                    except ValueError:
                        pass

            for z in zombies[:]:
                # Ensure pos_x exists (for backward compatibility with existing zombies if any)
                if 'pos_x' not in z:
                    z['pos_x'] = float(z['rect'].x)

                # Move towards player
                if z['rect'].centerx > player.centerx:
                    z['pos_x'] -= z['speed'] * dt / 16
                else:
                    z['pos_x'] += z['speed'] * dt / 16
                
                z['rect'].x = int(z['pos_x'])

                killed = False
                for b in bullets[:]:
                    if z['rect'].colliderect(b['rect']):
                        try:
                            zombies.remove(z)
                        except ValueError:
                            pass
                        
                        # Handle penetration
                        b['pen'] -= 1
                        if b['pen'] <= 0:
                            try:
                                bullets.remove(b)
                            except ValueError:
                                pass

                        # coin drop behavior based on rarity with chances
                        drop_amount = 0
                        if z.get('rarity') == 'blue':
                            if random.random() < 0.80:
                                drop_amount = 10
                        elif z.get('rarity') == 'green':
                            if random.random() < 0.50:
                                drop_amount = 5
                        elif z.get('rarity') == 'orange':
                            if random.random() < 0.60:
                                drop_amount = 50
                        elif z.get('rarity') == 'red':
                            if random.random() < 0.40:
                                drop_amount = 500
                        if drop_amount > 0:
                            # drops.append({'x': z['rect'].centerx, 'y': z['rect'].centery, 'life': 180, 'amount': drop_amount})
                            coins += drop_amount
                            zombies_killed += 1
                            save_state({'coins': coins, 'weapon_idx': weapon_idx, 'skin': skins[skin_idx], 'owned_skins': owned_skins, 'zombies_killed': zombies_killed, 'turret_owned': turret_owned, 'tower_owned': tower_owned})
                        killed = True
                        break

                if not killed:
                    if hit_cooldown <= 0 and z['rect'].colliderect(player):
                        try:
                            zombies.remove(z)
                        except ValueError:
                            pass
                        lives -= 1
                        hit_cooldown = 800
                        if lives <= 0:
                            game_over = True
                            # reset weapon and coins on death
                            weapon_idx = 0
                            coins = 0
                            save_state({'coins': coins, 'weapon_idx': weapon_idx, 'skin': skins[skin_idx], 'owned_skins': owned_skins, 'zombies_killed': zombies_killed, 'turret_owned': turret_owned, 'tower_owned': tower_owned})
                        continue

                if not killed:
                    if z['rect'].right < -50 or z['rect'].left > W + 50:
                        try:
                            zombies.remove(z)
                        except ValueError:
                            pass

            for d in drops[:]:
                d['y'] += 0.3 * dt / 16
                d['life'] -= dt / 16
                if d['life'] <= 0:
                    try:
                        drops.remove(d)
                    except ValueError:
                        pass

            if hit_cooldown > 0:
                hit_cooldown -= dt
                if hit_cooldown < 0:
                    hit_cooldown = 0

        # handle boost timer (only while not paused)
        if boost_timer > 0 and not paused:
            boost_timer -= dt
            if boost_timer <= 0:
                current_spawn_interval = SPAWN_INTERVAL

        if game_state == 'play':
            surface.fill((150, 200, 255))
            pygame.draw.circle(surface, (255, 240, 120), (W - 50, 36), 24)
            pygame.draw.polygon(surface, (237, 201, 175), [(0, 120), (70, 95), (150, 120), (230, 92), (320, 120), (320, 180), (0, 180)])
            pygame.draw.polygon(surface, (222, 184, 135), [(0, 140), (90, 115), (200, 140), (320, 110), (320, 180), (0, 180)])
            pygame.draw.rect(surface, (210, 180, 140), (0, 120, W, 60))

            def draw_cactus(x, base_y, scale=1.0):
                w = int(6 * scale)
                h = int(20 * scale)
                sx = int(x)
                sy = int(base_y - h)
                surface.fill((34, 139, 34), (sx, sy, w, h))
                surface.fill((34, 139, 34), (sx - 6, sy + 6, int(5 * scale), int(4 * scale)))
                surface.fill((34, 139, 34), (sx + w + 1, sy + 6, int(5 * scale), int(4 * scale)))

            draw_cactus(40, 130, 1.2)
            draw_cactus(140, 140, 1.0)
            draw_cactus(260, 125, 0.9)

            # Player Drawing
            draw_player(surface, player, facing, skins[skin_idx])

            gun_x = player.right if facing == 1 else player.left
            gun_y = player.centery - 3
            draw_gun(surface, gun_x, gun_y, facing, WEAPONS[weapon_idx]['name'])

            for b in bullets:
                b_type = b.get('type', 'Pistol')
                b_rect = b['rect']
                
                if b_type == 'Laser':
                    pygame.draw.rect(surface, (0, 255, 255), b_rect)
                    # Glow effect
                    pygame.draw.rect(surface, (200, 255, 255), (b_rect.x, b_rect.y + 1, b_rect.w, 1))
                elif b_type == 'Plasma':
                    pygame.draw.circle(surface, (0, 255, 0), b_rect.center, 3)
                    pygame.draw.circle(surface, (200, 255, 200), b_rect.center, 1)
                elif b_type == 'Railgun':
                    pygame.draw.rect(surface, (100, 100, 255), b_rect)
                    pygame.draw.rect(surface, (200, 200, 255), (b_rect.x, b_rect.y + 1, b_rect.w, 2))
                elif b_type == 'Grenade':
                    pygame.draw.circle(surface, (50, 50, 50), b_rect.center, 4)
                    pygame.draw.circle(surface, (200, 50, 50), (b_rect.centerx + 1, b_rect.centery - 1), 1)
                elif b_type == 'Sniper':
                    pygame.draw.rect(surface, (255, 255, 200), b_rect)
                elif b_type == 'Minigun':
                    pygame.draw.rect(surface, (255, 200, 100), b_rect)
                else:
                    # Standard bullet
                    pygame.draw.rect(surface, (255, 255, 255), b_rect)

            # Draw Turret
            if turret_owned:
                tx, ty = 40, GROUND_Y - 20
                # Base
                pygame.draw.rect(surface, (50, 50, 50), (tx - 10, ty, 20, 20))
                pygame.draw.rect(surface, (30, 30, 30), (tx - 12, ty + 15, 24, 5))
                # Head
                pygame.draw.rect(surface, (100, 100, 100), (tx - 8, ty - 8, 16, 10))
                # Barrel
                pygame.draw.rect(surface, (20, 20, 20), (tx + 8, ty - 5, 10, 4))
                # Status Light
                col = (0, 255, 0) if turret_cooldown <= 0 else (255, 0, 0)
                pygame.draw.rect(surface, col, (tx - 2, ty - 6, 4, 2))

            # Draw Boss
            if boss:
                bx, by, bw, bh = boss['rect'].x, boss['rect'].y, boss['rect'].w, boss['rect'].h
                # Big Zombie Drawing
                pygame.draw.rect(surface, (30, 30, 40), (bx + 4, by + bh - 10, 10, 10)) # Leg L
                pygame.draw.rect(surface, (30, 30, 40), (bx + bw - 14, by + bh - 10, 10, 10)) # Leg R
                pygame.draw.rect(surface, (60, 20, 20), (bx, by + 10, bw, bh - 20)) # Body
                pygame.draw.rect(surface, (100, 150, 100), (bx + 5, by - 10, bw - 10, 20)) # Head
                # Eyes
                pygame.draw.rect(surface, (255, 0, 0), (bx + 8, by - 4, 6, 6))
                pygame.draw.rect(surface, (255, 0, 0), (bx + bw - 14, by - 4, 6, 6))
                
                # Health Bar
                hp_pct = max(0, boss['hp'] / boss['max_hp'])
                pygame.draw.rect(surface, (50, 0, 0), (bx, by - 20, bw, 5))
                pygame.draw.rect(surface, (255, 0, 0), (bx, by - 20, int(bw * hp_pct), 5))

            for z in zombies:
                zx, zy, zw, zh = z['rect'].x, z['rect'].y, z['rect'].w, z['rect'].h
                # color by rarity
                rarity = z.get('rarity')
                if rarity == 'orange':
                    skin_color = (200, 130, 70)
                    shirt_color = (150, 80, 40)
                elif rarity == 'red':
                    skin_color = (180, 60, 60)
                    shirt_color = (120, 30, 30)
                elif rarity == 'green':
                    skin_color = (120, 200, 120)
                    shirt_color = (80, 140, 80)
                else: # Blue/Common
                    skin_color = (100, 140, 100)
                    shirt_color = (70, 100, 130)

                pants_color = (50, 50, 60)

                # Legs
                pygame.draw.rect(surface, pants_color, (zx + 2, zy + zh - 6, 4, 6))
                pygame.draw.rect(surface, pants_color, (zx + zw - 6, zy + zh - 6, 4, 6))
                
                # Body (Shirt)
                pygame.draw.rect(surface, shirt_color, (zx + 1, zy + 4, zw - 2, zh - 10))
                
                # Arms (reaching out)
                side = 1 if z['rect'].centerx - player.centerx > 0 else -1
                # If side is 1 (right of player), face left (-1). Arms point left.
                # If side is -1 (left of player), face right (1). Arms point right.
                
                arm_dir = -1 if side == 1 else 1
                
                if arm_dir == 1:
                    pygame.draw.rect(surface, skin_color, (zx + zw - 2, zy + 6, 6, 3)) # Right arm
                    pygame.draw.rect(surface, skin_color, (zx + 2, zy + 6, 2, 3)) # Left arm (shoulder)
                else:
                    pygame.draw.rect(surface, skin_color, (zx - 4, zy + 6, 6, 3)) # Left arm
                    pygame.draw.rect(surface, skin_color, (zx + zw - 4, zy + 6, 2, 3)) # Right arm (shoulder)

                # Head
                pygame.draw.rect(surface, skin_color, (zx + 3, zy - 2, zw - 6, 6))
                
                # Eyes (Red glowing for effect?)
                eye_color = (255, 50, 50) if rarity == 'red' else (20, 20, 20)
                
                if arm_dir == 1: # Facing Right
                    surface.fill(eye_color, (zx + zw - 5, zy, 2, 2))
                else: # Facing Left
                    surface.fill(eye_color, (zx + 3, zy, 2, 2))

            for d in drops:
                amt = d.get('amount', 1)
                if amt >= 500:
                    color = (255, 80, 80)
                elif amt >= 50:
                    color = (255, 140, 40)
                else:
                    color = (255, 204, 0)
                surface.fill(color, (int(d['x']), int(d['y']), 6, 6))

            pygame.draw.circle(surface, (255, 204, 0), (14, 14), 8)
            pygame.draw.circle(surface, (200, 160, 0), (18, 14), 3)
            coin_text = font.render(str(coins), True, (40, 40, 40))
            surface.blit(coin_text, (30, 6))
            wtext = font.render(WEAPONS[weapon_idx]['name'] + '  ' + skins[skin_idx], True, (50, 50, 50))
            surface.blit(wtext, (90, 6))

            def draw_heart(surf, x, y, size=8, filled=True):
                color = (220, 20, 60) if filled else (120, 120, 120)
                cx = x
                cy = y
                pygame.draw.circle(surf, color, (cx, cy), size // 2)
                pygame.draw.circle(surf, color, (cx + size // 2, cy), size // 2)
                pygame.draw.polygon(surf, color, [(cx - size // 2, cy), (cx + size, cy), (cx + size // 2, cy + size)])

            heart_x = W - 64
            for i in range(3):
                filled = (i < lives)
                draw_heart(surface, heart_x + i * 18, 12, 10, filled)

            if game_over:
                overlay = pygame.Surface((W, H))
                overlay.set_alpha(200)
                overlay.fill((0, 0, 0))
                surface.blit(overlay, (0, 0))
                go = pygame.font.SysFont('Consolas', 22).render('GAME OVER', True, (255, 80, 80))
                sub = pygame.font.SysFont('Consolas', 12).render('Apasă R pentru a reîncepe', True, (220, 220, 220))
                surface.blit(go, (W // 2 - go.get_width() // 2, H // 2 - 20))
                surface.blit(sub, (W // 2 - sub.get_width() // 2, H // 2 + 8))
            else:
                inst_text = 'Click stânga: Trage | U: Arme | C: Skin | R: Restart'
                if not turret_owned and coins >= TURRET_COST:
                    inst_text += ' | T: Cumpără Turetă (500k)'
                elif turret_owned:
                    inst_text += ' | Turetă Activă'
                
                inst = font.render(inst_text, True, (80, 80, 80))
                surface.blit(inst, (6, H - 16))
                
                # Boss Warning
                if zombies_killed >= BOSS_TRIGGER and not boss and not boss_defeated:
                    warn = font.render("BOSS ZOMBIE APPROACHING!", True, (255, 0, 0))
                    surface.blit(warn, (W//2 - warn.get_width()//2, 30))

            # pause overlay (frozen state)
            if paused:
                prow = pygame.Surface((W, H))
                prow.set_alpha(200)
                prow.fill((20, 24, 40))
                surface.blit(prow, (0, 0))
                ptxt = pygame.font.SysFont('Consolas', 20).render('PAUSED', True, (240, 240, 240))
                psub = pygame.font.SysFont('Consolas', 12).render('Apasă SPACE pentru a relua', True, (200, 200, 200))
                surface.blit(ptxt, (W // 2 - ptxt.get_width() // 2, H // 2 - 12))
                surface.blit(psub, (W // 2 - psub.get_width() // 2, H // 2 + 12))

        elif game_state == 'shop_weapon':
            # Gun Shop Visuals
            surface.fill((50, 50, 50)) # Walls
            pygame.draw.rect(surface, (30, 30, 30), (0, H - 40, W, 40)) # Floor
            # Decor: Gun Rack
            pygame.draw.rect(surface, (80, 80, 80), (40, 40, W - 80, 60))
            pygame.draw.rect(surface, (40, 40, 40), (45, 45, W - 90, 50))
            # Draw some dummy guns
            for i in range(5):
                gx = 60 + i * 40
                pygame.draw.rect(surface, (20, 20, 20), (gx, 60, 30, 10))
            
            # Player in shop
            shop_player = pygame.Rect(W // 2 - 6, H - 56, 12, 16)
            draw_player(surface, shop_player, 1, skins[skin_idx])
            
            # Draw gun on player
            gun_x = shop_player.right
            gun_y = shop_player.centery - 3
            draw_gun(surface, gun_x, gun_y, 1, WEAPONS[shop_idx]['name'])
            
            # UI
            title_font = pygame.font.SysFont('Consolas', 16)
            info_font = pygame.font.SysFont('Consolas', 10)
            
            title = title_font.render("GUN SHOP (Left/Right to browse)", True, (255, 200, 50))
            surface.blit(title, (W//2 - title.get_width()//2, 10))
            
            w_data = WEAPONS[shop_idx]
            name_txt = title_font.render(w_data['name'], True, (255, 255, 255))
            surface.blit(name_txt, (W//2 - name_txt.get_width()//2, 30))
            
            stats = f"Speed: {w_data.get('speed', '?')} | Pen: {w_data['pen']}"
            stats_txt = info_font.render(stats, True, (200, 200, 200))
            surface.blit(stats_txt, (W//2 - stats_txt.get_width()//2, 50))
            
            cost = w_data['cost']
            if shop_idx <= weapon_idx:
                status = "OWNED (Equipped)" if shop_idx == weapon_idx else "OWNED"
                col = (100, 255, 100)
            elif shop_idx == weapon_idx + 1:
                status = f"COST: {cost} - Press ENTER to Buy"
                col = (255, 255, 100) if coins >= cost else (255, 100, 100)
            else:
                status = "LOCKED (Buy previous first)"
                col = (150, 150, 150)
                
            status_txt = info_font.render(status, True, col)
            surface.blit(status_txt, (W//2 - status_txt.get_width()//2, 110))
            
            # Coins display in shop
            pygame.draw.circle(surface, (255, 204, 0), (14, 14), 8)
            coin_text = font.render(str(coins), True, (255, 255, 255))
            surface.blit(coin_text, (30, 6))
            
            footer = info_font.render("Press U to return", True, (150, 150, 150))
            surface.blit(footer, (W//2 - footer.get_width()//2, H - 20))

        elif game_state == 'shop_skin':
            # Skin Shop Visuals
            surface.fill((240, 230, 200)) # Walls
            pygame.draw.rect(surface, (160, 100, 50), (0, H - 40, W, 40)) # Floor
            # Decor: Mirrors
            pygame.draw.rect(surface, (100, 50, 20), (W//2 - 20, 40, 40, 60)) # Frame
            pygame.draw.rect(surface, (200, 230, 255), (W//2 - 16, 44, 32, 52)) # Glass
            pygame.draw.line(surface, (255, 255, 255), (W//2 - 10, 50), (W//2 + 10, 70), 1)
            
            # Player in shop (Preview)
            # We draw the selected skin, not the current skin
            preview_player = pygame.Rect(W // 2 - 6, H - 56, 12, 16)
            draw_player(surface, preview_player, 1, skins[shop_idx])
            
            # UI
            title_font = pygame.font.SysFont('Consolas', 16)
            info_font = pygame.font.SysFont('Consolas', 10)
            
            title = title_font.render("SKIN SHOP (Left/Right to browse)", True, (50, 150, 255))
            surface.blit(title, (W//2 - title.get_width()//2, 10))
            
            s_name = skins[shop_idx]
            name_txt = title_font.render(s_name, True, (50, 50, 50))
            surface.blit(name_txt, (W//2 - name_txt.get_width()//2, 30))
            
            cost = SKIN_COSTS.get(s_name, 0)
            if skin_idx == shop_idx:
                status = "EQUIPPED"
                col = (50, 255, 50)
            elif s_name in owned_skins:
                status = "OWNED - Press ENTER to Equip"
                col = (100, 200, 100)
            else:
                status = f"COST: {cost} - Press ENTER to Buy/Equip"
                col = (200, 150, 0) if coins >= cost else (200, 50, 50)
                
            status_txt = info_font.render(status, True, col)
            surface.blit(status_txt, (W//2 - status_txt.get_width()//2, 110))
            
            # Coins display in shop
            pygame.draw.circle(surface, (255, 204, 0), (14, 14), 8)
            coin_text = font.render(str(coins), True, (40, 40, 40))
            surface.blit(coin_text, (30, 6))
            
            footer = info_font.render("Press C to return", True, (100, 100, 100))
            surface.blit(footer, (W//2 - footer.get_width()//2, H - 20))

        pygame.transform.scale(surface, (W * SCALE, H * SCALE), SCREEN)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
