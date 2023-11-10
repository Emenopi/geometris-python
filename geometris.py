import pygame
from pygame.locals import *
import math
import random

pygame.init()

pygame.display.set_caption('Geometris')

SCREEN_SIZE = 900
OUTER_CIRCLE_DIM = SCREEN_SIZE*0.91
SCREEN = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

boundaryCircle = pygame.image.load('assets/circle.png')
boundaryCircle = pygame.transform.scale(boundaryCircle, (OUTER_CIRCLE_DIM, OUTER_CIRCLE_DIM))

# Load Blocks
cyanBlock = pygame.image.load('assets/cyan.png')
purpleBlock = pygame.image.load('assets/purple.png')
magentaBlock = pygame.image.load('assets/magenta.png')
orangeBlock = pygame.image.load('assets/orange.png')
yellowBlock = pygame.image.load('assets/yellow.png')
greenBlock = pygame.image.load('assets/green.png')
blackBlock = pygame.image.load('assets/black.png')
BLOCK_RECT = cyanBlock.get_rect()
BLOCKS_BY_INDEX = ["cyan", "purple", "magenta", "orange", "yellow", "green", "black"]
BLOCKS_BY_NAME = {"cyan": cyanBlock, 
                  "purple": purpleBlock, 
                  "magenta": magentaBlock, 
                  "orange": orangeBlock, 
                  "yellow": yellowBlock, 
                  "green": greenBlock,
                  "black": blackBlock}

BORDER = (SCREEN_SIZE-OUTER_CIRCLE_DIM)/2
CENTRE = SCREEN_SIZE/2
INTERNAL_RADIUS = (OUTER_CIRCLE_DIM/2)*0.88
CENTRE_CIRCLE_RADIUS = math.floor(INTERNAL_RADIUS/4)

brickSpeed = 500
fireEvent = pygame.USEREVENT+1

def gridMatrix ():
    matrix = []
    matrixHeight = math.floor((INTERNAL_RADIUS - CENTRE_CIRCLE_RADIUS)/18)
    for i in range(matrixHeight):
        matrix.append([])
        for j in range(60):
            matrix[i].append("black")
    return matrix, matrixHeight

def getNewBrick():
    blockIndex = random.randint(0, 5)
    block = BLOCKS_BY_INDEX[blockIndex]
    return block

def renderNextBrick(block):
    block = BLOCKS_BY_NAME[block]
    blockImg = pygame.transform.scale(block, (BLOCK_RECT[2]*BLOCK_MIN_SCALE[1], BLOCK_RECT[3]*BLOCK_MIN_SCALE[0]))
    blockRect = blockImg.get_rect()
    blockCentre = (blockRect[2]/2, blockRect[3]/2)
    SCREEN.blit(blockImg, (CENTRE-blockCentre[0], CENTRE-blockCentre[1]))

def fireBrick(i, direction, block):
    if gameMatrix[i][direction] == "black":
        gameMatrix[i][direction] = block
        if i > 0:
            gameMatrix[i-1][direction] = "black"

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
        scaleFactor = ((i+1)/8, (i+1)/60)
        for j in range(len(gameMatrix[i])):
                currentBlock = BLOCKS_BY_NAME[gameMatrix[i][j]]
                blockImg = pygame.transform.smoothscale(currentBlock, (minScale[0]+(minScale[0]*scaleFactor[0]), minScale[0]+(minScale[1]*scaleFactor[1])))
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
nextBrick = False     

play = True

while play:
    
    SCREEN.fill((000, 000, 000))
    SCREEN.blit(boundaryCircle, (BORDER, BORDER))
    pygame.draw.circle(SCREEN, (195, 33, 45), (CENTRE, CENTRE), CENTRE_CIRCLE_RADIUS)
    pygame.draw.circle(SCREEN, (0, 0, 0), (CENTRE, CENTRE), INTERNAL_RADIUS)

    renderBlocks()
    if nextBrick == False:
        nextBrick = getNewBrick()
    else:
        renderNextBrick(nextBrick)

    keys = pygame.key.get_pressed()    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == KEYDOWN and event.key == K_SPACE:
            movingBrick = nextBrick
            nextBrick = False
            index = 0
            pygame.time.set_timer(fireEvent, brickSpeed, len(gameMatrix))
        if event.type == fireEvent and index < len(gameMatrix):
            fireBrick(index, 0, movingBrick)
            renderBlocks()
            index += 1
            if index >= len(gameMatrix):
                index = 0

    pygame.display.flip()


pygame.quit()