import pygame

WIDTH = 1300
HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tech Fest '26")
clock = pygame.time.Clock()
running = True

# Idle animations
idle_down = [pygame.transform.scale(pygame.image.load("assets/MC_DOWN1.png"), (200, 200)),
             pygame.transform.scale(pygame.image.load("assets/MC_DOWN2.png"), (200, 200))]
idle_up = [pygame.transform.scale(pygame.image.load("assets/MC_UP1.png"), (200, 200)),
           pygame.transform.scale(pygame.image.load("assets/MC_UP2.png"), (200, 200))]
idle_left = [pygame.transform.scale(pygame.image.load("assets/MC_LEFT1.png"), (200, 200)),
             pygame.transform.scale(pygame.image.load("assets/MC_LEFT2.png"), (200, 200))]
idle_right = [pygame.transform.scale(pygame.image.load("assets/MC_RIGHT1.png"), (200, 200)),
              pygame.transform.scale(pygame.image.load("assets/MC_RIGHT2.png"), (200, 200))]

# Walk animations
walk_down = [pygame.transform.scale(pygame.image.load("assets/MC_DOWN3.png"), (200, 200)),
             pygame.transform.scale(pygame.image.load("assets/MC_DOWN4.png"), (200, 200))]
walk_up = [pygame.transform.scale(pygame.image.load("assets/MC_UP3.png"), (200, 200)),
           pygame.transform.scale(pygame.image.load("assets/MC_UP4.png"), (200, 200))]
walk_left = [pygame.transform.scale(pygame.image.load("assets/MC_LEFT3.png"), (200, 200)),
             pygame.transform.scale(pygame.image.load("assets/MC_LEFT4.png"), (200, 200))]
walk_right = [pygame.transform.scale(pygame.image.load("assets/MC_RIGHT3.png"), (200, 200)),
              pygame.transform.scale(pygame.image.load("assets/MC_RIGHT4.png"), (200, 200))]

character_rect = idle_down[0].get_rect(center=(WIDTH // 2, HEIGHT // 2))
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
    if keys[pygame.K_w] or keys[pygame.K_UP]:  # Move up
        character_rect.y -= speed
        current_animation = walk_up
        direction = "up"
        moving = True
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # Move down
        character_rect.y += speed
        current_animation = walk_down
        direction = "down"
        moving = True
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Move left
        character_rect.x -= speed
        current_animation = walk_left
        direction = "left"
        moving = True
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Move right
        character_rect.x += speed
        current_animation = walk_right
        direction = "right"
        moving = True

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

    screen.fill((0, 0, 0))

    screen.blit(current_animation[current_frame], character_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()