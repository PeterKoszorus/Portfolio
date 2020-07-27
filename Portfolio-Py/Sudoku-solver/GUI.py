import pygame

pygame.init()

main_window = pygame.display.set_mode((400, 400))
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
