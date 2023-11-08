import pygame
from pygame.locals import *
import math

pygame.init()

pygame.display.set_caption('Geometris')

SCREEN_DIM = 800
CIRCLE_DIM = SCREEN_DIM*0.85
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
CENTRE_RADIUS = math.floor(INTERNAL_RADIUS/10)
if INTERNAL_RADIUS % 10 != 0:
    CENTRE_RADIUS += INTERNAL_RADIUS % 10

def gridMatrix ():
    matrix = []
    matrixHeight = math.floor((INTERNAL_RADIUS - CENTRE_RADIUS)/30)
    for i in range(matrixHeight):
        matrix.append([])
        for j in range(60):
            matrix[i].append(BLOCKS[0])
    return matrix, matrixHeight

def getBrick(block):
    blockImg = pygame.transform.scale(block, (BLOCK_RECT[2]*BLOCK_MIN_SCALE, BLOCK_RECT[3]*BLOCK_MIN_SCALE))
    SCREEN.blit(blockImg, (BLOCK_OFFSET_X+CENTRE_RADIUS, BLOCK_OFFSET_Y))

def fireBrick(direction, block):
    #take index for direction
    #iterate over loop to change value
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
    #render bricks as matrix updates, alter scale
    minScale = (BLOCK_RECT[2]*BLOCK_MIN_SCALE, BLOCK_RECT[3]*BLOCK_MIN_SCALE*1.6)
    additionalOffset = 0
    for i in range(len(gameMatrix)):
        for j in range(len(gameMatrix[i])):
                blockImg = pygame.transform.smoothscale(gameMatrix[i][j], (minScale[0]+(minScale[0]*((i+1)*0.22)), minScale[0]+(minScale[1]*((i+1)*0.1))))
                blockRect = blockImg.get_rect()
                blockImg = pygame.transform.rotate(blockImg, j*-6)
                blockRectRotated = blockImg.get_rect()
                offsetDefaultX = CENTRE-(blockRectRotated[2]/2)
                offsetDefaultY = CENTRE-(blockRectRotated[3]/2)
                offsetX = offsetDefaultX+((CENTRE_RADIUS+MARGIN+additionalOffset)*getOffset(j, 'x'))
                offsetY = offsetDefaultY+((-CENTRE_RADIUS-MARGIN-additionalOffset)*getOffset(j, 'y'))
                if j%1 == 0:
                    SCREEN.blit(blockImg, (offsetX, offsetY))
        additionalOffset += blockRect[3]+5

            

play = True

while play:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            play = False
    
    SCREEN.fill((000, 000, 000))

    SCREEN.blit(circle, (BORDER, BORDER))
    pygame.draw.circle(SCREEN, (195, 33, 45), (CENTRE, CENTRE), CENTRE_RADIUS)

    gameMatrix, MATRIX_HEIGHT = gridMatrix()
    BLOCK_MIN_SCALE = (MATRIX_HEIGHT/100)*2.5
    BLOCK_OFFSET_X = CENTRE-((BLOCK_RECT[2]*BLOCK_MIN_SCALE)/2)
    BLOCK_OFFSET_Y = CENTRE-CENTRE_RADIUS-((BLOCK_RECT[3]*BLOCK_MIN_SCALE))
    MARGIN = 100
    activeBlock = BLOCKS[1]
    #getBrick(activeBlock)
    renderBlocks()

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            play = False
        if event.type == KEYDOWN and event.key == K_SPACE:
            gameMatrix[0][0] = blackBlock

    pygame.display.flip()


pygame.quit()