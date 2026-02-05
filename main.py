import pygame

pygame.init()

window = pygame.display.set_mode((800, 600))

pygame.display.set_caption("AI Business Tracker")

BG = (189, 244, 255) # Light blue

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill(BG)

    pygame.display.flip()

pygame.quit()