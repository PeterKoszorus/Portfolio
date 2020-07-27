import pygame

WIDTH = 540
HEIGHT = 600
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]

pygame.init()

main_window = pygame.display.set_mode((WIDTH, HEIGHT))
main_window.fill(WHITE)
pygame.display.set_caption("Sudoku")
pygame.display.set_icon(pygame.image.load("Logo.png"))

run = True
#Main loop
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
