import pygame
from pygame.locals import *
import math

pygame.init()

pygame.display.set_caption('Geometris')

SCREEN_DIM = 900
CIRCLE_DIM = SCREEN_DIM*0.91
SCREEN = pygame.display.set_mode((SCREEN_DIM, SCREEN_DIM))

circle = pygame.image.load('assets/circle.png')
circle = pygame.transform.scale(circle, (CIRCLE_DIM, CIRCLE_DIM))
circleRect = circle.get_rect()

cyanBlock = pygame.image.load('assets/cyan.png')
purpleBlock = pygame.image.load('assets/purple.png')
magentaBlock = pygame.image.load('assets/magenta.png')
orangeBlock = pygame.image.load('assets/orange.png')
yellowBlock = pygame.image.load('assets/yellow.png')
greenBlock = pygame.image.load('assets/green.png')
blackBlock = pygame.image.load('assets/black.png')
BLOCK_RECT = cyanBlock.get_rect()
BLOCKS = [cyanBlock, purpleBlock, magentaBlock, orangeBlock, yellowBlock, greenBlock, blackBlock]

BORDER = (SCREEN_DIM-CIRCLE_DIM)/2
CENTRE = SCREEN_DIM/2
INTERNAL_RADIUS = (CIRCLE_DIM/2)*0.88
CENTRE_CIRCLE_RADIUS = math.floor(INTERNAL_RADIUS/3) + (INTERNAL_RADIUS % 10)

def gridMatrix ():
    matrix = []
    matrixHeight = math.floor((INTERNAL_RADIUS - CENTRE_CIRCLE_RADIUS)/18)
    for i in range(matrixHeight):
        matrix.append([])
        for j in range(60):
            matrix[i].append(BLOCKS[0])
    return matrix, matrixHeight

def getBrick(block):
    blockImg = pygame.transform.scale(block, (BLOCK_RECT[2]*BLOCK_MIN_SCALE, BLOCK_RECT[3]*BLOCK_MIN_SCALE))
    SCREEN.blit(blockImg, (BLOCK_OFFSET_X+CENTRE_CIRCLE_RADIUS, BLOCK_OFFSET_Y))

def fireBrick(direction, block):
    getBrick(blackBlock)
    for i in range(len(gameMatrix)):
        gameMatrix[i][direction] = block
        if i > 0:
            gameMatrix[i-1][direction] = blackBlock
        renderBlocks()
        pygame.time.delay(100)

def getOffset(n, dim):
    num = (n*6)*(math.pi/180)
    if dim == 'x':
        offset = math.sin(num)
    else:
        offset = math.cos(num)
    return offset


def renderBlocks ():
    minScale = (BLOCK_RECT[2]*BLOCK_MIN_SCALE[0], BLOCK_RECT[3]*BLOCK_MIN_SCALE[1])
    additionalOffset = 0
    for i in range(len(gameMatrix)):
        centerOffset = CENTRE_CIRCLE_RADIUS+MARGIN+additionalOffset
        scaleFactor = ((i+1)/6, (i+1)/28)
        for j in range(len(gameMatrix[i])):
                blockImg = pygame.transform.smoothscale(gameMatrix[i][j], (minScale[0]+(minScale[0]*scaleFactor[0]), minScale[0]+(minScale[1]*scaleFactor[1])))
                blockRect = blockImg.get_rect()
                blockImg = pygame.transform.rotate(blockImg, j*-6)
                blockRectRotated = blockImg.get_rect()

                offsetDefaultX = CENTRE-(blockRectRotated[2]/2)
                offsetDefaultY = CENTRE-(blockRectRotated[3]/2)
                offsetX = offsetDefaultX+(centerOffset*getOffset(j, 'x'))
                offsetY = offsetDefaultY+(-centerOffset*getOffset(j, 'y'))

                SCREEN.blit(blockImg, (offsetX, offsetY))
        additionalOffset += blockRect[3]+3

gameMatrix, MATRIX_HEIGHT = gridMatrix()
BLOCK_MIN_SCALE = ((MATRIX_HEIGHT/100)*1.5, (MATRIX_HEIGHT/100)*3)
BLOCK_OFFSET_X = CENTRE-((BLOCK_RECT[2]*BLOCK_MIN_SCALE[0])/2)
BLOCK_OFFSET_Y = CENTRE-CENTRE_CIRCLE_RADIUS-((BLOCK_RECT[3]*BLOCK_MIN_SCALE[0]))
MARGIN = 25        

play = True

while play:
    
    SCREEN.fill((000, 000, 000))

    SCREEN.blit(circle, (BORDER, BORDER))
    pygame.draw.circle(SCREEN, (195, 33, 45), (CENTRE, CENTRE), CENTRE_CIRCLE_RADIUS)

    renderBlocks()

    keys = pygame.key.get_pressed()    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == KEYDOWN and event.key == K_SPACE:
            gameMatrix[0][0] = blackBlock

    pygame.display.flip()


pygame.quit()