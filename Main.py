import pygame

WIDTH = 1000
HEIGHT = 700

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tech Fest '26")
clock = pygame.time.Clock()
running = True

background = pygame.image.load("assets/background.png")

# Idle animations
idle_down = [pygame.transform.scale(pygame.image.load("assets/character/MC_DOWN1.png"), (225, 275)),
             pygame.transform.scale(pygame.image.load("assets/character/MC_DOWN2.png"), (225, 275))]
idle_up = [pygame.transform.scale(pygame.image.load("assets/character/MC_UP1.png"), (225, 275)),
           pygame.transform.scale(pygame.image.load("assets/character/MC_UP2.png"), (225, 275))]
idle_left = [pygame.transform.scale(pygame.image.load("assets/character/MC_LEFT1.png"), (225, 275)),
             pygame.transform.scale(pygame.image.load("assets/character/MC_LEFT2.png"), (225, 275))]
idle_right = [pygame.transform.scale(pygame.image.load("assets/character/MC_RIGHT1.png"), (225, 275)),
              pygame.transform.scale(pygame.image.load("assets/character/MC_RIGHT2.png"), (225, 275))]

# Walk animations
walk_down = [pygame.transform.scale(pygame.image.load("assets/character/MC_DOWN3.png"), (225, 275)),
             pygame.transform.scale(pygame.image.load("assets/character/MC_DOWN4.png"), (225, 275))]
walk_up = [pygame.transform.scale(pygame.image.load("assets/character/MC_UP3.png"), (225, 275)),
           pygame.transform.scale(pygame.image.load("assets/character/MC_UP4.png"), (225, 275))]
walk_left = [pygame.transform.scale(pygame.image.load("assets/character/MC_LEFT3.png"), (225, 275)),
             pygame.transform.scale(pygame.image.load("assets/character/MC_LEFT4.png"), (225, 275))]
walk_right = [pygame.transform.scale(pygame.image.load("assets/character/MC_RIGHT3.png"), (225, 275)),
              pygame.transform.scale(pygame.image.load("assets/character/MC_RIGHT4.png"), (225, 275))]

# Objects
trashcan = pygame.transform.scale(pygame.image.load("assets/objects/zafacon_lol.png"), (70, 70))
order_slide = pygame.transform.scale(pygame.image.load("assets/objects/orderslide.png"), (1015, 80))
computer = pygame.transform.scale(pygame.image.load("assets/objects/computer.png"), (75, 75))
counters = pygame.transform.scale(pygame.image.load("assets/objects/counters.png"), (800, 260))
pastries = pygame.transform.scale(pygame.image.load("assets/objects/pastries.png"), (200, 220))
verjas = pygame.transform.scale(pygame.image.load("assets/objects/verjitas.png"), (200, 100))

coffee_grinder = pygame.transform.scale(pygame.image.load("assets/objects/grinder.png"), (200, 140))
coffee_machine = pygame.transform.scale(pygame.image.load("assets/objects/coffee_machine.png"), (200, 140))
drink_station = pygame.transform.scale(pygame.image.load("assets/objects/drinkprep.png"), (200, 140))

trashcan_rect = pygame.Rect(
    trashcan.get_rect(topleft=(950, 620)).x,
    trashcan.get_rect(topleft=(950, 620)).y,
    trashcan.get_width(),
    trashcan.get_height() // 4
).inflate(-40, -20)

order_slide_rect = pygame.Rect(
    order_slide.get_rect(topleft=(-5, 25)).x,
    order_slide.get_rect(topleft=(-5, 25)).y,
    order_slide.get_width(),
    order_slide.get_height() // 2
).inflate(-40, -20)

computer_rect = pygame.Rect(
    computer.get_rect(topleft=(850, 280)).x,
    computer.get_rect(topleft=(850, 280)).y,
    computer.get_width(),
    computer.get_height() // 4
).inflate(-20, -10)

counters_rect = pygame.Rect(
    counters.get_rect(topleft=(160, 250)).x,
    counters.get_rect(topleft=(160, 270)).y,
    counters.get_width(),
    counters.get_height() // 4
).inflate(-20, -10)

pastries_rect = pygame.Rect(
    pastries.get_rect(topleft=(-15, 300)).x,
    pastries.get_rect(topleft=(-15, 518)).y,
    pastries.get_width() // 1.3,
    pastries.get_height()
).inflate(-20, -10)

verjas_rect = pygame.Rect(
    verjas.get_rect(topleft=(-5, 370)).x,
    verjas.get_rect(topleft=(-5, 370)).y,
    verjas.get_width() // 1.2,
    verjas.get_height() // 8
).inflate(-20, -10)

grinder_rec = pygame.Rect(
    coffee_grinder.get_rect(topleft=(780, 220)).x,
    coffee_grinder.get_rect(topleft=(670, 205)).y,
    coffee_grinder.get_width(),
    coffee_grinder.get_height()
).inflate(-20, -10)

coffee_machine_rect = pygame.Rect(
    coffee_machine.get_rect(topleft=(620, 240)).x,
    coffee_machine.get_rect(topleft=(620, 200)).y,
    coffee_machine.get_width(),
    coffee_machine.get_height()
).inflate(-20, -10)

drink_station_rect = pygame.Rect(
    drink_station.get_rect(topleft=(400, 240)).x,
    drink_station.get_rect(topleft=(400, 200)).y,
    drink_station.get_width(),
    drink_station.get_height()
).inflate(-20, -10)

character_rect = idle_down[0].get_rect(center=(WIDTH // 2, HEIGHT // 1.4)).inflate(-80, -150)

# List of object rectangles for collision detection
object_rects = [drink_station_rect, coffee_machine_rect, grinder_rec, computer_rect, trashcan_rect,
                order_slide_rect, counters_rect, pastries_rect, verjas_rect]

speed = 5
animation_timer = 0
idle_animation_timer = 0
current_frame = 0
current_animation = idle_down
direction = "down"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    moving = False
    new_rect = character_rect.copy()

    if keys[pygame.K_w] or keys[pygame.K_UP]:  # Move up
        new_rect.y -= speed
        current_animation = walk_up
        direction = "up"
        moving = True
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # Move down
        new_rect.y += speed
        current_animation = walk_down
        direction = "down"
        moving = True
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Move left
        new_rect.x -= speed
        current_animation = walk_left
        direction = "left"
        moving = True
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Move right
        new_rect.x += speed
        current_animation = walk_right
        direction = "right"
        moving = True

    # Check for collisions with objects
    if not any(new_rect.colliderect(obj) for obj in object_rects):
        character_rect = new_rect

    # World borders
    character_rect.x = max(0, min(character_rect.x, WIDTH - character_rect.width))
    character_rect.y = max(0, min(character_rect.y, HEIGHT - character_rect.height))

    if not moving:
        if direction == "up":
            current_animation = idle_up
        elif direction == "down":
            current_animation = idle_down
        elif direction == "left":
            current_animation = idle_left
        elif direction == "right":
            current_animation = idle_right

        idle_animation_timer += clock.get_time()
        if idle_animation_timer > 500:
            current_frame = (current_frame + 1) % len(current_animation)
            idle_animation_timer = 0
    else:
        animation_timer += clock.get_time()
        if animation_timer > 200:
            current_frame = (current_frame + 1) % len(current_animation)
            animation_timer = 0

    # Draw everything
    screen.blit(background, (0, 0))

    screen.blit(verjas, (-5, 370))
    screen.blit(trashcan, (900, 620))
    screen.blit(order_slide, (-5, 30))
    screen.blit(counters, (160, 250))
    screen.blit(computer, (850, 300))
    screen.blit(pastries, (-15, 500))

    screen.blit(coffee_grinder, (680, 260))
    screen.blit(coffee_machine, (535, 240))
    screen.blit(drink_station, (360, 240))

    screen.blit(current_animation[current_frame], character_rect.inflate(100, 100).topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()