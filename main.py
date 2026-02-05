import pygame

pygame.init()

window = pygame.display.set_mode((800, 500))

pygame.display.set_caption("AI Business Tracker")

HEADER_COLOR = (59, 190, 255)
BG = (255, 255, 255) # Light blue

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill(BG)
    pygame.draw.rect(window, HEADER_COLOR, (0, 0, 800, 75))

    pygame.display.flip()

pygame.quit()