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
rotateCentreBlockEvent = pygame.USEREVENT+2

def gridMatrix ():
    matrix = []
    matrixHeight = math.floor((INTERNAL_RADIUS - CENTRE_CIRCLE_RADIUS)/18)
    for i in range(matrixHeight):
        matrix.append([])
        for j in range(60):
            matrix[i].append("black")
    return matrix, matrixHeight

def getBlockMatrix(blockName):
    if blockName == "cyan":
        blockMatrix = [["cyan"]]
    elif blockName == "purple":
        blockMatrix = [["purple"], 
                       ["purple"], 
                       ["purple"]]
    elif blockName == "magenta":
        blockMatrix = [["magenta", "magenta"], 
                       ["magenta", "magenta"]]
    elif blockName == "orange":
        blockMatrix = [["orange"], 
                       ["orange", "orange"]]
    elif blockName == "yellow":
        blockMatrix = [["yellow", "yellow"], 
                       ["yellow"], 
                       ["yellow"]]
    elif blockName == "green":
        blockMatrix = [["green"], 
                       ["green", "green"], 
                       ["green"]]
    else:
        blockMatrix = [["black"]]
    return blockMatrix

def getNewBrick():
    blockIndex = random.randint(0, 5)
    block = BLOCKS_BY_INDEX[blockIndex]
    return block

def getMatrixWidth(matrix):
    width = 0
    for i in range(len(matrix)):
        if len(matrix[i]) > width:
            width = len(matrix[i])
    return width

def renderNextBrick(direction, activeBrick):
    block = pygame.image.load('assets/%s_full.png' % activeBrick)
    block = pygame.transform.rotate(block, direction*-6)
    blockSize = block.get_size()
    block = pygame.transform.smoothscale(block, (blockSize[0]*0.3, blockSize[1]*0.3))
    adjustedBlockSize = block.get_size()
    blockCentre = [adjustedBlockSize[0]/2, adjustedBlockSize[1]/2]
    offsetX = (CENTRE_CIRCLE_RADIUS-adjustedBlockSize[0]-5)*getOffset(direction ,'x')
    offsetY = (-CENTRE_CIRCLE_RADIUS+adjustedBlockSize[1]-5)*getOffset(direction, 'y')
    SCREEN.blit(block, (CENTRE-blockCentre[0]+offsetX, CENTRE-blockCentre[1]+offsetY))
    
def canBlockMove(i, direction, blockMatrix):
    checkDepth = len(blockMatrix)
    for index in range(checkDepth):
        for width in range(len(blockMatrix[index])):
            if index == 0 and gameMatrix[i][direction+width] != "black":
                return False
            elif len(blockMatrix[index]) - len(blockMatrix[index-1]):
                checkWidth = len(blockMatrix[index]) - len(blockMatrix[index-1])
                for w in range(1, checkWidth):
                    if gameMatrix[i-index][direction+w] != "black":
                        return False
    return True

def fireBrick(i, direction, blockMatrix):
    if i+1 < len(blockMatrix):
        iterations = i+1
    else:
        iterations = len(blockMatrix)

    for index in range(iterations):
        for widthIndex in range(len(blockMatrix[index])):
            if (i - index - 1) >= 0:
                gameMatrix[i-index-1][direction-widthIndex] = "black"
            gameMatrix[i-index][direction-widthIndex] = blockMatrix[0][0]

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
blockIsMoving = False
rotationRate = 1000
directionToFire = 0
pygame.time.set_timer(rotateCentreBlockEvent, rotationRate, 60)

while play:

    SCREEN.fill((000, 000, 000))
    SCREEN.blit(boundaryCircle, (BORDER, BORDER))
    pygame.draw.circle(SCREEN, (0, 0, 0), (CENTRE, CENTRE), INTERNAL_RADIUS)
    pygame.draw.circle(SCREEN, (195, 33, 45), (CENTRE, CENTRE), CENTRE_CIRCLE_RADIUS)

    renderBlocks()
    if nextBrick == False:
        nextBrick = getNewBrick()
    else:
        renderNextBrick(directionToFire, nextBrick)

    keys = pygame.key.get_pressed()
    maxBlockMoves = len(gameMatrix)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == KEYDOWN and event.key == K_SPACE and not blockIsMoving:
            blockIsMoving = True
            movingBrick = nextBrick
            nextBrick = False
            index = 0
            maxBlockMoves = len(gameMatrix)
            pygame.time.set_timer(fireEvent, brickSpeed, maxBlockMoves)
        if event.type == fireEvent and index < len(gameMatrix):
            blockMatrix = getBlockMatrix(movingBrick)
            canMove = canBlockMove(index, directionToFire, blockMatrix)
            if canMove:
                fireBrick(index, directionToFire, blockMatrix)
            index += 1
            if index >= len(gameMatrix) or not canMove:
                index = 0
                blockIsMoving = False
                pygame.time.set_timer(fireEvent, 0)            
            renderBlocks()
        if event.type == rotateCentreBlockEvent and not blockIsMoving:
            directionToFire += 1
            if directionToFire == 60:
                directionToFire = 0
            pygame.time.set_timer(rotateCentreBlockEvent, rotationRate, 0)
            pygame.time.set_timer(rotateCentreBlockEvent, rotationRate, 60)

    pygame.display.flip()


pygame.quit()