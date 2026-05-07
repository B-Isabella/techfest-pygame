import pygame
import random
import math

WIDTH = 1000
HEIGHT = 700

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tech Fest '26")
clock = pygame.time.Clock()
running = True

#Menu elements...

menu_font = pygame.font.Font("assets/PixelifySans-VariableFont_wght.ttf", 40)

background = pygame.image.load("assets/background.png")
menu_background = pygame.image.load("assets/menu_background.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

title_font = pygame.font.Font("assets/PixelifySans-VariableFont_wght.ttf", 80)
title_text = title_font.render("SEQUENCE COOKING", True, (255, 255, 255))
title_rect = title_text.get_rect(center=(WIDTH // 2, 150))

sage_green = (156, 175, 136)
light_red = (255, 120, 120)
white = (255, 255, 255)

start_button = pygame.Rect(WIDTH // 2 - 125, 300, 250, 70)
start_button_text = menu_font.render("Start Game", True, white)
start_button_rect = start_button_text.get_rect(center=start_button.center)

quit_rect = pygame.Rect(WIDTH // 2 - 125, 400, 250, 70)
quit_text = menu_font.render("QUIT", True, white)
quit_text_rect = quit_text.get_rect(center=quit_rect.center)



menu = ["Croissant", "Cinnamon Roll", "Strawberry Shortcake", "Coffee Cake", "Carrot Cake"]
coffee_menu = ["Latte", "Cappuccino", "Cold Brew"]
inventory = []
MAX_CARRY = 3
score = 0
font       = pygame.font.SysFont("Arial", 28, bold=True)
small_font = pygame.font.SysFont("Arial", 20, bold=True)
order_font = pygame.font.SysFont("Arial", 20, bold=True)
tiny_font  = pygame.font.SysFont("Arial", 14, bold=True)

coffee_step = None  

def generate_order():
    pastry_pick = random.sample(menu, random.randint(1, 2))
    coffee_pick = random.sample(coffee_menu, 1) if random.random() > 0.4 else []
    order = pastry_pick + coffee_pick
    random.shuffle(order)
    return order[:random.randint(2, 3)]

current_order = generate_order()

# Idle animations
idle_down  = [pygame.transform.scale(pygame.image.load("assets/character/MC_DOWN1.png"),  (225, 275)),
              pygame.transform.scale(pygame.image.load("assets/character/MC_DOWN2.png"),  (225, 275))]
idle_up    = [pygame.transform.scale(pygame.image.load("assets/character/MC_UP1.png"),    (225, 275)),
              pygame.transform.scale(pygame.image.load("assets/character/MC_UP2.png"),    (225, 275))]
idle_left  = [pygame.transform.scale(pygame.image.load("assets/character/MC_LEFT1.png"), (225, 275)),
              pygame.transform.scale(pygame.image.load("assets/character/MC_LEFT2.png"), (225, 275))]
idle_right = [pygame.transform.scale(pygame.image.load("assets/character/MC_RIGHT1.png"),(225, 275)),
              pygame.transform.scale(pygame.image.load("assets/character/MC_RIGHT2.png"),(225, 275))]

# Walk animations
walk_down  = [pygame.transform.scale(pygame.image.load("assets/character/MC_DOWN3.png"),  (225, 275)),
              pygame.transform.scale(pygame.image.load("assets/character/MC_DOWN4.png"),  (225, 275))]
walk_up    = [pygame.transform.scale(pygame.image.load("assets/character/MC_UP3.png"),    (225, 275)),
              pygame.transform.scale(pygame.image.load("assets/character/MC_UP4.png"),    (225, 275))]
walk_left  = [pygame.transform.scale(pygame.image.load("assets/character/MC_LEFT3.png"), (225, 275)),
              pygame.transform.scale(pygame.image.load("assets/character/MC_LEFT4.png"), (225, 275))]
walk_right = [pygame.transform.scale(pygame.image.load("assets/character/MC_RIGHT3.png"),(225, 275)),
              pygame.transform.scale(pygame.image.load("assets/character/MC_RIGHT4.png"),(225, 275))]


trashcan       = pygame.transform.scale(pygame.image.load("assets/objects/zafacon_lol.png"),     (70,  70))
pastries_img   = pygame.transform.scale(pygame.image.load("assets/objects/pastries.png"),        (200, 220))
# Coffee station assets:
def pixelate(surface, pixel_size=4):
    w, h = surface.get_size()
    small = pygame.transform.scale(surface, (max(1, w // pixel_size), max(1, h // pixel_size)))
    return pygame.transform.scale(small, (w, h))

# Counters: 
counters       = pixelate(pygame.transform.scale(
    pygame.image.load("assets/objects/counters.png"), (800, 260)), pixel_size=2)

coffee_grinder = pixelate(pygame.transform.scale(
    pygame.image.load("assets/objects/grinder.png"),        (200, 140)))
coffee_machine = pixelate(pygame.transform.scale(
    pygame.image.load("assets/objects/coffee_machine.png"), (200, 140)))

#COFFEE CUP SPRITES
def draw_latte_cup(surf, x, y):
    cup_color    = (210, 170, 120)
    foam_color   = (245, 235, 215)
    handle_color = (180, 130, 80)
    pygame.draw.polygon(surf, cup_color,    [(x+8,y+20),(x+52,y+20),(x+46,y+60),(x+14,y+60)])
    pygame.draw.arc(surf, handle_color,     (x+44, y+28, 18, 22), math.pi*1.5, math.pi*0.5, 4)
    pygame.draw.ellipse(surf, foam_color,   (x+6, y+12, 48, 16))
    pygame.draw.arc(surf, (160, 100, 50),   (x+16, y+15, 22, 10), 0, math.pi, 2)
    pygame.draw.ellipse(surf, handle_color, (x+2, y+57, 56, 10))
    lbl = tiny_font.render("Latte", True, (80, 40, 0))
    surf.blit(lbl, (x + 30 - lbl.get_width()//2, y + 64))

def draw_cappuccino_cup(surf, x, y):
    cup_color    = (200, 150, 100)
    foam_color   = (240, 230, 210)
    handle_color = (160, 110, 60)
    choc_color   = (120, 70, 30)
    pygame.draw.polygon(surf, cup_color,    [(x+10,y+20),(x+50,y+20),(x+44,y+58),(x+16,y+58)])
    pygame.draw.arc(surf, handle_color,     (x+42, y+26, 16, 20), math.pi*1.5, math.pi*0.5, 4)
    pygame.draw.ellipse(surf, foam_color,   (x+8, y+12, 44, 16))
    for dx, dy in [(18,16),(26,14),(34,16),(22,19),(30,18)]:
        pygame.draw.circle(surf, choc_color, (x+dx, y+dy), 2)
    pygame.draw.ellipse(surf, handle_color, (x+4, y+55, 52, 9))
    lbl = tiny_font.render("Cappuccino", True, (80, 40, 0))
    surf.blit(lbl, (x + 30 - lbl.get_width()//2, y + 62))

def draw_coldbrew_cup(surf, x, y):
    cup_color   = (180, 220, 240)
    liquid      = (60,  35,  15)
    ice_color   = (220, 240, 255)
    straw_color = (255, 100, 150)
    pygame.draw.polygon(surf, cup_color, [(x+10,y+5),(x+50,y+5),(x+46,y+65),(x+14,y+65)])
    pygame.draw.polygon(surf, liquid,    [(x+13,y+22),(x+47,y+22),(x+46,y+65),(x+14,y+65)])
    for ix, iy in [(x+15,y+25),(x+30,y+28),(x+20,y+38)]:
        pygame.draw.rect(surf, ice_color,       (ix, iy, 10, 10), border_radius=2)
        pygame.draw.rect(surf, (180,210,230),   (ix, iy, 10, 10), 1,  border_radius=2)
    pygame.draw.rect(surf, straw_color,     (x+36, y+2, 5, 45), border_radius=3)
    pygame.draw.ellipse(surf, (150,200,230),(x+8, y+1, 44, 10))
    lbl = tiny_font.render("Cold Brew", True, (30, 60, 100))
    surf.blit(lbl, (x + 30 - lbl.get_width()//2, y + 68))

# coffee panel
COFFEE_PANEL_W = 95
COFFEE_PANEL_H = 290
COFFEE_PANEL_X = 25  
COFFEE_PANEL_Y = 220    

coffee_panel_surf = pygame.Surface((COFFEE_PANEL_W, COFFEE_PANEL_H), pygame.SRCALPHA)

def build_coffee_panel():
    coffee_panel_surf.fill((0, 0, 0, 0))
    pygame.draw.rect(coffee_panel_surf, (200, 170, 130, 220),
                     (0, 0, COFFEE_PANEL_W, COFFEE_PANEL_H), border_radius=14)
    pygame.draw.rect(coffee_panel_surf, (140, 100, 60, 255),
                     (0, 0, COFFEE_PANEL_W, COFFEE_PANEL_H), 2, border_radius=14)
    draw_latte_cup(coffee_panel_surf,      5,   5)
    draw_cappuccino_cup(coffee_panel_surf, 5,  98)
    draw_coldbrew_cup(coffee_panel_surf,   5, 195)

build_coffee_panel()

# slots for coffee panel 
coffee_click_slots = [
    (pygame.Rect(COFFEE_PANEL_X + 2, COFFEE_PANEL_Y + 2,   COFFEE_PANEL_W - 4, 90), 0),  # Latte
    (pygame.Rect(COFFEE_PANEL_X + 2, COFFEE_PANEL_Y + 95,  COFFEE_PANEL_W - 4, 90), 1),  # Cappuccino
    (pygame.Rect(COFFEE_PANEL_X + 2, COFFEE_PANEL_Y + 190, COFFEE_PANEL_W - 4, 95), 2),  # Cold Brew
]

#Pixel art cafe window drawing function
def draw_cafe_window(surf):
    wx, wy, ww, wh = 360, 110, 240, 165
    B = 8  # pixel block size

    # Sky  
    sky_rows = (wh - 20) // B + 1
    sky_cols = (ww - 20) // B + 1
    for row in range(sky_rows):
        t = row / max(1, sky_rows - 1)
        sky_c = (int(130 + t * 25), int(190 + t * 15), int(235 - t * 15))
        for col in range(sky_cols):
            pygame.draw.rect(surf, sky_c,
                             (wx + 10 + col * B, wy + 10 + row * B, B, B))

    # Ground 
    ground_y = wy + wh - 44
    cobble_colors = [(195, 170, 135), (180, 155, 120), (205, 178, 140)]
    for col in range((ww - 20) // B + 1):
        for row in range(5):
            c = cobble_colors[(col + row) % len(cobble_colors)]
            pygame.draw.rect(surf, c,
                             (wx + 10 + col * B, ground_y + row * B, B, B))

    # Cafe table
    tx, ty = wx + ww // 2 - 32, ground_y - B * 2
    for col in range(8):   # tabletop
        pygame.draw.rect(surf, (145, 95, 50),  (tx + col * B, ty,      B, B))
        pygame.draw.rect(surf, (115, 70, 30),  (tx + col * B, ty + B,  B, B // 2))
    pygame.draw.rect(surf, (125, 80, 40), (tx + 4,      ty + B,     8, B * 2))  # left leg
    pygame.draw.rect(surf, (125, 80, 40), (tx + 52, ty + B,     8, B * 2))  # right leg

    # Chair
    cx, cy = tx + 44, ty + B
    for col in range(3):   # seat
        pygame.draw.rect(surf, (175, 115, 55), (cx + col * B, cy, B, B))
    for row in range(3):   # back rest
        pygame.draw.rect(surf, (175, 115, 55), (cx + 2 * B, cy - row * B, B, B))

    # Tiny coffee cup on table
    ccx, ccy = tx + 12, ty - B
    pygame.draw.rect(surf, (215, 175, 125), (ccx, ccy + 4, B, B))
    pygame.draw.ellipse(surf, (240, 215, 175), (ccx - 1, ccy, 10, 5))
    pygame.draw.rect(surf, (160, 100, 50), (ccx - 2, ccy + B + 2, 12, 2))

    # Flower pot 
    fpx, fpy = wx + 22, ground_y - B * 2
    pygame.draw.rect(surf, (180, 80, 50),  (fpx, fpy + B,     B * 2, B))   # pot
    pygame.draw.rect(surf, (160, 60, 30),  (fpx - 2, fpy + B * 2, B * 2 + 4, B // 2))
    pygame.draw.circle(surf, (80, 160, 60),  (fpx + B, fpy),      5)       # foliage
    pygame.draw.circle(surf, (60, 140, 50),  (fpx + B - 4, fpy + 3), 4)
    pygame.draw.circle(surf, (100, 180, 70), (fpx + B + 4, fpy + 2), 3)
    # Small flowers
    for fx_, fy_ in [(fpx + B - 3, fpy - 4), (fpx + B + 2, fpy - 6)]:
        pygame.draw.circle(surf, (240, 100, 140), (fx_, fy_), 2)

    # Window frame 
    frame_col = (155, 100, 48)
    pygame.draw.rect(surf, frame_col, (wx, wy, ww, wh), 10)
    # Cross dividers
    pygame.draw.rect(surf, frame_col, (wx + ww // 2 - 5, wy,         10, wh))
    pygame.draw.rect(surf, frame_col, (wx,               wy + wh // 2 - 5, ww, 10))
    # Highlight edge
    pygame.draw.rect(surf, (200, 145, 78), (wx, wy, ww, wh), 3)
    # Window sill
    pygame.draw.rect(surf, (175, 118, 60), (wx - 10, wy + wh - 4, ww + 20, 14))
    pygame.draw.rect(surf, (135, 88, 38),  (wx - 10, wy + wh + 10, ww + 20,  4))

trashcan_rect = pygame.Rect(
    *trashcan.get_rect(topleft=(950, 620)).topleft,
    trashcan.get_width(), trashcan.get_height() // 4
).inflate(-40, -20)

counters_rect = pygame.Rect(
    *counters.get_rect(topleft=(160, 270)).topleft,
    counters.get_width(), counters.get_height() // 4
).inflate(-20, -10)

pastries_rect = pygame.Rect(
    pastries_img.get_rect(topleft=(-15, 518)).x,
    pastries_img.get_rect(topleft=(-15, 518)).y,
    int(pastries_img.get_width() // 1.3), pastries_img.get_height()
).inflate(-20, -10)

grinder_rect = pygame.Rect(
    coffee_grinder.get_rect(topleft=(780, 220)).x,
    coffee_grinder.get_rect(topleft=(670, 205)).y,
    coffee_grinder.get_width(), coffee_grinder.get_height()
).inflate(-20, -10)

coffee_machine_rect = pygame.Rect(
    coffee_machine.get_rect(topleft=(620, 240)).x,
    coffee_machine.get_rect(topleft=(620, 200)).y,
    coffee_machine.get_width(), coffee_machine.get_height()
).inflate(-20, -10)

character_rect = idle_down[0].get_rect(center=(WIDTH // 2, HEIGHT // 1.4)).inflate(-80, -150)

object_rects = [coffee_machine_rect, grinder_rect,
                trashcan_rect, counters_rect, pastries_rect]

# Interaction zones
dropoff_rect           = pygame.Rect(380, 580, 240, 60)
pastries_interact_zone = pygame.Rect(0, 470, 250, 230)
trashcan_interact_zone = pygame.Rect(870, 580, 130, 120)
grinder_interact_zone  = pygame.Rect(650, 330, 200, 120)
machine_interact_zone  = pygame.Rect(490, 320, 155, 120)

coffee_panel_zone      = pygame.Rect(COFFEE_PANEL_X - 20, COFFEE_PANEL_Y - 10,
COFFEE_PANEL_W + 60, COFFEE_PANEL_H + 40)

# Pastry click slots
PANEL_X = -15
PANEL_Y = 500
pastry_click_slots = [
    (pygame.Rect(PANEL_X,      PANEL_Y + 140, 185, 80), 0),  # Croissant
    (pygame.Rect(PANEL_X + 95, PANEL_Y + 65,   90, 75), 1),  # Cinnamon Roll
    (pygame.Rect(PANEL_X,      PANEL_Y + 65,   90, 75), 2),  # Strawberry SC
    (pygame.Rect(PANEL_X,      PANEL_Y,         90, 65), 3),  # Coffee Cake
    (pygame.Rect(PANEL_X + 95, PANEL_Y,         90, 65), 4),  # Carrot Cake
]


# load main menu

def main_menu():
    menu_running = True
    while menu_running:
        screen.blit(menu_background, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(menu_mouse_pos):
                    return "GAME"
                elif quit_rect.collidepoint(menu_mouse_pos):
                    return "QUIT"
                
        pygame.draw.rect(screen, sage_green, start_button)
        screen.blit(start_button_text, start_button_rect)

        pygame.draw.rect(screen, light_red, quit_rect)
        screen.blit(quit_text, quit_text_rect)

        screen.blit(title_text, title_rect)

        pygame.display.flip()
        clock.tick(60)

def play_game():
    global running, score, coffee_step, current_order, character_rect
    speed             = 5
    animation_timer   = 0
    idle_animation_timer = 0
    current_frame     = 0
    current_animation = idle_down
    direction         = "down"

    near_pastries     = False
    near_dropoff      = False
    near_trash        = False
    near_grinder      = False
    near_machine      = False
    near_coffee_panel = False

    feedback_msg   = ""
    feedback_timer = 0

    def set_feedback(msg, duration=120):
        nonlocal feedback_msg, feedback_timer
        feedback_msg, feedback_timer = msg, duration

    def add_to_inventory(item):
        if len(inventory) < MAX_CARRY:
            inventory.append(item)
            set_feedback(f"Picked up {item}!")
        else:
            set_feedback(f"Hands full! (max {MAX_CARRY})")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Pastry panel 
                if near_pastries:
                    for slot_rect, idx in pastry_click_slots:
                        if slot_rect.collidepoint(mx, my):
                            add_to_inventory(menu[idx])
                            break

                # Coffee cup panel(only after brewing)
                elif near_coffee_panel and coffee_step == "brewed":
                    for slot_rect, idx in coffee_click_slots:
                        if slot_rect.collidepoint(mx, my):
                            add_to_inventory(coffee_menu[idx])
                            coffee_step = None     
                            build_coffee_panel()
                            break

                #Trash
                elif near_trash:
                    for i in range(len(inventory)):
                        item_rect = pygame.Rect(22, 78 + (i + 1) * 28, 270, 26)
                        if item_rect.collidepoint(mx, my):
                            removed = inventory.pop(i)
                            set_feedback(f"Trashed {removed}!")
                            break

                #Drop-off 
                elif near_dropoff:
                    delivered = []
                    for item in list(inventory):
                        if item in current_order:
                            current_order.remove(item)
                            score += 15
                            delivered.append(item)
                        else:
                            score -= 5
                    for item in delivered:
                        inventory.remove(item)
                    if delivered:
                        set_feedback(f"Served: {', '.join(delivered)}! +{15*len(delivered)} pts", 160)
                    else:
                        set_feedback("Wrong items! Click them in your list near the trash.", 160)
                    if not current_order:
                        current_order = generate_order()
                        set_feedback("Order complete! New order up!", 180)

                elif near_grinder:
                    if coffee_step is None:
                        coffee_step = "ground"
                        set_feedback("Beans ground! Now brew at the coffee machine.")
                    else:
                        set_feedback("Already ground — head to the coffee machine next.")

                elif near_machine:
                    if coffee_step == "ground":
                        coffee_step = "brewed"
                        set_feedback("Coffee brewed! Pick your drink from the panel (top left).")
                    elif coffee_step is None:
                        set_feedback("Grind the beans first!")
                    else:
                        set_feedback("Already brewed! Pick a drink from the top-left panel.")

        #Movement
        keys   = pygame.key.get_pressed()
        moving = False
        new_rect = character_rect.copy()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_rect.y -= speed; current_animation = walk_up;    direction = "up";    moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_rect.y += speed; current_animation = walk_down;  direction = "down";  moving = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            new_rect.x -= speed; current_animation = walk_left;  direction = "left";  moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            new_rect.x += speed; current_animation = walk_right; direction = "right"; moving = True

        if not any(new_rect.colliderect(obj) for obj in object_rects):
            character_rect = new_rect

        character_rect.x = max(0, min(character_rect.x, WIDTH  - character_rect.width))
        character_rect.y = max(0, min(character_rect.y, HEIGHT - character_rect.height))

        near_pastries     = character_rect.colliderect(pastries_interact_zone)
        near_dropoff      = character_rect.colliderect(dropoff_rect.inflate(60, 60))
        near_trash        = character_rect.colliderect(trashcan_interact_zone)
        near_grinder      = character_rect.colliderect(grinder_interact_zone)
        near_machine      = character_rect.colliderect(machine_interact_zone)
        near_coffee_panel = character_rect.colliderect(coffee_panel_zone)

        if feedback_timer > 0:
            feedback_timer -= 1

        if not moving:
            if   direction == "up":    current_animation = idle_up
            elif direction == "down":  current_animation = idle_down
            elif direction == "left":  current_animation = idle_left
            elif direction == "right": current_animation = idle_right
            idle_animation_timer += clock.get_time()
            if idle_animation_timer > 500:
                current_frame = (current_frame + 1) % len(current_animation)
                idle_animation_timer = 0
        else:
            animation_timer += clock.get_time()
            if animation_timer > 200:
                current_frame = (current_frame + 1) % len(current_animation)
                animation_timer = 0

        
        # DRAW 
        screen.blit(background, (0, 0))

        # Pixel-art cafe window 
        draw_cafe_window(screen)

        
        screen.blit(trashcan,       (900, 620))
        screen.blit(counters,       (160, 250))
        screen.blit(pastries_img,   (-15, 500))
        screen.blit(coffee_grinder, (680, 260))
        screen.blit(coffee_machine, (535, 240))
    

        # Coffee step indicator labels
        step_labels = {
            None:     ("1. GRIND",    (695, 248), (160, 100, 40)),
            "ground": ("2. BREW",     (550, 228), (40,  120, 40)),
            "brewed": ("3. PICK ↑",   (370, 100), (40,   80, 160)),  # points up toward panel
        }
        label_text, label_pos, label_color = step_labels[coffee_step]
        step_surf = small_font.render(label_text, True, label_color)
        pygame.draw.rect(screen, (255, 255, 220),
                        (label_pos[0], label_pos[1] - 2,
                        step_surf.get_width() + 10, step_surf.get_height() + 4),
                        border_radius=6)
        screen.blit(step_surf, (label_pos[0] + 5, label_pos[1]))

        # Coffee panel 
        panel_alpha = 255 if coffee_step == "brewed" else 140
        coffee_panel_surf.set_alpha(panel_alpha)
        screen.blit(coffee_panel_surf, (COFFEE_PANEL_X, COFFEE_PANEL_Y))
        panel_title = tiny_font.render(
            "DRINKS" if coffee_step != "brewed" else "← PICK DRINK",
            True,
            (80, 40, 0) if coffee_step != "brewed" else (40, 80, 160)
        )
        screen.blit(panel_title, (COFFEE_PANEL_X + COFFEE_PANEL_W // 2 - panel_title.get_width() // 2,
                                COFFEE_PANEL_Y - 16))

        # serivice window/drop-off
        drop_color = (190, 145, 90) if near_dropoff else (165, 120, 68)
        pygame.draw.rect(screen, drop_color, dropoff_rect, border_radius=10)
        pygame.draw.rect(screen, (110, 72, 28), dropoff_rect, 3, border_radius=10)


        # Label
        dl = small_font.render("SERVE  [click]", True, (255, 240, 200))
        screen.blit(dl, (dropoff_rect.x + 48, dropoff_rect.centery - dl.get_height() // 2))

        # Character
        screen.blit(current_animation[current_frame], character_rect.inflate(100, 100).topleft)

        # Inventory box (top left)
        inv_lines = (
            [f"Carrying ({len(inventory)}/{MAX_CARRY}):"] + [f"  - {item}" for item in inventory]
            if inventory else ["Carrying: Nothing"]
        )
        box_h = 20 + len(inv_lines) * 28 + 36
        pygame.draw.rect(screen, (255, 255, 255), (10, 70, 310, box_h), border_radius=12)
        pygame.draw.rect(screen, (180, 180, 180), (10, 70, 310, box_h), 2, border_radius=12)
        for i, line in enumerate(inv_lines):
            color = (0, 0, 0) if i == 0 else (60, 60, 150)
            txt = small_font.render(line, True, color)
            screen.blit(txt, (22, 78 + i * 28))
            if near_trash and i > 0:
                h = tiny_font.render("[click to trash]", True, (180, 60, 60))
                screen.blit(h, (22 + txt.get_width() + 6, 78 + i * 28 + 4))
        screen.blit(font.render(f"Tips: ${score}", True, (0, 150, 0)), (22, 78 + len(inv_lines) * 28))

        # Current order box (top right)
        order_lines = ["Current Order:"] + [f"  - {item}" for item in current_order]
        max_w = max(order_font.size(l)[0] for l in order_lines) + 30
        order_box_h = 14 + len(order_lines) * 28 + 10
        obx = WIDTH - max_w - 14
        pygame.draw.rect(screen, (255, 245, 220), (obx, 70, max_w, order_box_h), border_radius=12)
        pygame.draw.rect(screen, (180, 120,  60), (obx, 70, max_w, order_box_h), 2, border_radius=12)
        for i, line in enumerate(order_lines):
            color = (100, 50, 0) if i == 0 else (60, 20, 0)
            screen.blit(order_font.render(line, True, color), (obx + 12, 70 + 10 + i * 28))

        # Context hints
        hint_text = None
        if near_pastries:
            hint_text = "Click a pastry to pick it up"
        elif near_grinder and coffee_step is None:
            hint_text = "Click the grinder to start coffee!"
        elif near_machine and coffee_step == "ground":
            hint_text = "Click the machine to brew!"
        elif near_coffee_panel and coffee_step == "brewed":
            hint_text = "Click a drink on the left panel to pick it up!"
        elif near_dropoff:
            hint_text = "Click to serve your order!"

        if hint_text:
            h = small_font.render(hint_text, True, (80, 40, 0))
            pygame.draw.rect(screen, (255, 240, 210),
                            (WIDTH // 2 - h.get_width() // 2 - 10, HEIGHT - 50,
                            h.get_width() + 20, 36), border_radius=10)
            screen.blit(h, (WIDTH // 2 - h.get_width() // 2, HEIGHT - 44))

        # Feedback toast
        if feedback_timer > 0:
            fb = small_font.render(feedback_msg, True, (20, 80, 20))
            fb_bg = pygame.Surface((fb.get_width() + 20, fb.get_height() + 10), pygame.SRCALPHA)
            fb_bg.fill((220, 255, 220, 200))
            screen.blit(fb_bg, (WIDTH // 2 - fb_bg.get_width() // 2, HEIGHT - 100))
            screen.blit(fb,    (WIDTH // 2 - fb.get_width() // 2,    HEIGHT -  96))

        pygame.display.flip()
        clock.tick(60)
    return "MENU"
        

state = "MENU"
while state != "QUIT":
    if state == "MENU":
        state = main_menu()
    elif state == "GAME":
        state = play_game()

pygame.quit()