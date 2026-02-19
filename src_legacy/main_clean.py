import pygame
import sys
import random
import json
import os

SAVE_FILE = 'save.json'


def load_state():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {'coins': 0, 'weapon_unlocked': False, 'skin': 'default'}
    return {'coins': 0, 'weapon_unlocked': False, 'skin': 'default'}


def save_state(state):
    with open(SAVE_FILE, 'w') as f:
        json.dump(state, f)


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
    weapon_unlocked = state.get('weapon_unlocked', False)
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

    lives = 3
    game_over = False
    hit_cooldown = 0

    spawn_timer = 0

    font = pygame.font.SysFont('Consolas', 10)

    skins = ['default', 'blue', 'green']
    skin_idx = skins.index(skin) if skin in skins else 0

    def spawn_zombie():
        z_w, z_h = 14, 18
        y = GROUND_Y - z_h
        rect = pygame.Rect(W + 10, y, z_w, z_h)
        speed = 0.25 + random.random() * 0.35
        zombies.append({'rect': rect, 'speed': speed})

    facing = 1

    def shoot(target_x=None):
        nonlocal facing
        if target_x is not None:
            facing = 1 if target_x >= player.centerx else -1
        speed = 10 if weapon_unlocked else 7
        if facing == 1:
            bx = player.right + 1
        else:
            bx = player.left - 7
        by = player.centery - 2
        b = pygame.Rect(int(bx), int(by), 6, 4)
        bullets.append({'rect': b, 'vx': speed * facing})

    running = True
    while running:
        dt = clock.tick(60)
        spawn_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_state({'coins': coins, 'weapon_unlocked': weapon_unlocked, 'skin': skins[skin_idx]})
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_over:
                    mx, my = pygame.mouse.get_pos()
                    mx = int(mx / SCALE)
                    shoot(mx)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and on_ground and not game_over:
                    player_vy = JUMP_V
                    on_ground = False
                if event.key == pygame.K_u and not game_over:
                    if not weapon_unlocked and coins >= 100:
                        coins -= 100
                        weapon_unlocked = True
                        save_state({'coins': coins, 'weapon_unlocked': weapon_unlocked, 'skin': skins[skin_idx]})
                if event.key == pygame.K_c and not game_over:
                    if coins >= 1000:
                        coins -= 1000
                        skin_idx = (skin_idx + 1) % len(skins)
                        skin = skins[skin_idx]
                        save_state({'coins': coins, 'weapon_unlocked': weapon_unlocked, 'skin': skin})
                if event.key == pygame.K_r and game_over:
                    lives = 3
                    game_over = False
                    zombies.clear()
                    bullets.clear()
                    drops.clear()
                    spawn_timer = 0

        if not game_over:
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

            if spawn_timer > 2000:
                spawn_zombie()
                spawn_timer = 0

            player_vy += GRAVITY * (dt / 16)
            player.y += player_vy * (dt / 16)
            if player.y + player.h >= GROUND_Y:
                player.y = GROUND_Y - player.h
                player_vy = 0
                on_ground = True

            if player.x < 0:
                player.x = 0
            if player.x + player.w > W:
                player.x = W - player.w

            for b in bullets[:]:
                b['rect'].x += b['vx']
                if b['rect'].x > W or b['rect'].x < 0:
                    try:
                        bullets.remove(b)
                    except ValueError:
                        pass

            for z in zombies[:]:
                z['rect'].x -= z['speed'] * dt / 16
                killed = False
                for b in bullets[:]:
                    if z['rect'].colliderect(b['rect']):
                        try:
                            zombies.remove(z)
                        except ValueError:
                            pass
                        try:
                            bullets.remove(b)
                        except ValueError:
                            pass
                        drops.append({'x': z['rect'].centerx, 'y': z['rect'].centery, 'life': 180})
                        coins += 1
                        save_state({'coins': coins, 'weapon_unlocked': weapon_unlocked, 'skin': skins[skin_idx]})
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
                        continue

                if not killed and z['rect'].right < 0:
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

        # draw
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

        if skins[skin_idx] == 'blue':
            color = (100, 180, 255)
            shade = (70, 120, 180)
        elif skins[skin_idx] == 'green':
            color = (140, 255, 140)
            shade = (90, 180, 90)
        else:
            color = (255, 220, 150)
            shade = (200, 160, 110)

        pygame.draw.rect(surface, shade, (player.x, player.y + 4, player.w, player.h - 4))
        pygame.draw.rect(surface, color, (player.x + 2, player.y - 6, player.w - 4, 8))
        ex = player.x + (player.w - 6 if facing == 1 else 2)
        surface.fill((20, 20, 20), (ex, player.y - 4, 3, 3))
        pygame.draw.rect(surface, shade, (player.x + 2, player.y + player.h - 2, 4, 4))
        pygame.draw.rect(surface, shade, (player.x + player.w - 6, player.y + player.h - 2, 4, 4))
        if facing == 1:
            gun_rect = pygame.Rect(player.right, player.centery - 3, 10, 4)
        else:
            gun_rect = pygame.Rect(player.left - 10, player.centery - 3, 10, 4)
        surface.fill((60, 60, 60), gun_rect)

        for b in bullets:
            pygame.draw.rect(surface, (255, 255, 255), b['rect'])

        for z in zombies:
            zx, zy, zw, zh = z['rect'].x, z['rect'].y, z['rect'].w, z['rect'].h
            pygame.draw.rect(surface, (100, 140, 100), (zx + 1, zy + 4, zw - 2, zh - 6))
            pygame.draw.rect(surface, (90, 120, 90), (zx + 3, zy - 2, zw - 6, 6))
            surface.fill((90, 120, 90), (zx - 3, zy + 6, 4, 3))
            surface.fill((90, 120, 90), (zx + zw - 1, zy + 6, 4, 3))
            pygame.draw.rect(surface, (80, 110, 80), (zx + 2, zy + zh - 4, 4, 4))
            pygame.draw.rect(surface, (80, 110, 80), (zx + zw - 6, zy + zh - 4, 4, 4))
            side = 1 if z['rect'].centerx - player.centerx > 0 else -1
            if side == 1:
                surface.fill((20, 20, 20), (zx + zw - 5, zy + 3, 3, 3))
            else:
                surface.fill((20, 20, 20), (zx + 2, zy + 3, 3, 3))

        for d in drops:
            surface.fill((255, 204, 0), (int(d['x']), int(d['y']), 6, 6))

        pygame.draw.circle(surface, (255, 204, 0), (14, 14), 8)
        pygame.draw.circle(surface, (200, 160, 0), (18, 14), 3)
        coin_text = font.render(str(coins), True, (40, 40, 40))
        surface.blit(coin_text, (30, 6))
        wtext = font.render(('SMG' if weapon_unlocked else 'Pistol') + '  ' + skins[skin_idx], True, (50, 50, 50))
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
            inst = font.render('Click stânga pentru a trage. Apasă U pentru arma, C pentru skin, R pentru restart.', True, (80, 80, 80))
            surface.blit(inst, (6, H - 16))

        pygame.transform.scale(surface, (W * SCALE, H * SCALE), SCREEN)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
