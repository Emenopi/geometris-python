import pygame
import math

pygame.init()

pygame.display.set_caption('Geometris')

SCREEN_DIM = 800
CIRCLE_DIM = SCREEN_DIM*0.85
screen = pygame.display.set_mode((SCREEN_DIM, SCREEN_DIM))

circle = pygame.image.load('assets/circle.png')
circle = pygame.transform.scale(circle, (CIRCLE_DIM, CIRCLE_DIM))
circleRect = circle.get_rect()

BORDER = (SCREEN_DIM-CIRCLE_DIM)/2
CENTRE = SCREEN_DIM/2
INTERNAL_RADIUS = (CIRCLE_DIM/2)*0.88
CENTRE_RADIUS = math.floor(INTERNAL_RADIUS/10)
if INTERNAL_RADIUS % 10 != 0:
    CENTRE_RADIUS += INTERNAL_RADIUS % 10

def gridMatrix ():
    #init 60x? grid, determine ? based on how many will fit in radius
    matrix = []
    matrixHeight = math.floor((INTERNAL_RADIUS - CENTRE_RADIUS)/40)
    for i in range(matrixHeight):
        GAME_MATRIX.append([])
        for j in range(60):
            GAME_MATRIX[i].append(0)
    return matrix


#def playCircle ():
    #game loop for circle tetris

play = True

while play:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            play = False

    screen.fill((000, 000, 000))

    screen.blit(circle, (BORDER, BORDER))
    pygame.draw.circle(screen, (195, 33, 45), (CENTRE, CENTRE), CENTRE_RADIUS)

    GAME_MATRIX = gridMatrix()

    pygame.display.flip()


pygame.quit()