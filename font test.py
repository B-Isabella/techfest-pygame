import pygame

pygame.init()
# This gets the list of all available system font names
all_fonts = pygame.font.get_fonts()

# Print them all to your terminal
for font_name in all_fonts:
    print(font_name)