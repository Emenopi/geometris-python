import pygame
from pygame.locals import *
import math
import random
from init import *
from score import *

pygame.init()

pygame.display.set_caption('Geometris')
DEFAULTFONT = pygame.font.Font('freesansbold.ttf', 20)

score = 0

brickSpeed = 500
fireEvent = pygame.USEREVENT+1
rotateCentreBlockEvent = pygame.USEREVENT+2

def getNewBrick(BLOCKS_BY_INDEX):
    blockIndex = random.randint(0, 5)
    block = BLOCKS_BY_INDEX[blockIndex]
    return block

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

def getBlockMatrix(blockName):
    if blockName == "cyan":
        blockMatrix = [["cyan"]]
    elif blockName == "purple":
        blockMatrix = [["purple", "null", "null"], 
                       ["purple", "null", "null"], 
                       ["purple", "null", "null"]]
    elif blockName == "magenta":
        blockMatrix = [["magenta", "magenta"], 
                       ["magenta", "magenta"]]
    elif blockName == "orange":
        blockMatrix = [["orange", "null", "null"], 
                       ["orange", "orange", "null"],
                       ["null", "null", "null"]]
    elif blockName == "yellow":
        blockMatrix = [["yellow", "yellow", "null"], 
                       ["yellow", "null", "null"], 
                       ["yellow", "null", "null"]]
    elif blockName == "green":
        blockMatrix = [["green", "null", "null"], 
                       ["green", "green", "null"], 
                       ["green", "null", "null"]]
    else:
        blockMatrix = [["black"]]
    return blockMatrix

def getMatrixWidth(matrix):
    width = 0
    for i in range(len(matrix)):
        if len(matrix[i]) > width:
            width = len(matrix[i])
    return width
    
def canBlockMove(i, direction, blockMatrix):
    checkDepth = len(blockMatrix)
    for index in range(checkDepth):
        for width in range(len(blockMatrix[index])):
            if index == 0 and gameMatrix[i][(direction+width)%60] != "black":
                return False
            elif len(blockMatrix[index]) - len(blockMatrix[index-1]):
                checkWidth = len(blockMatrix[index]) - len(blockMatrix[index-1])
                for w in range(1, checkWidth):
                    if gameMatrix[i-index][direction+w] != "black":
                        return False
    return True

def moveBrick(i, direction, blockMatrix):
    if i+1 < len(blockMatrix):
        iterations = i+1
    else:
        iterations = len(blockMatrix)

    for index in range(iterations):
        for widthIndex in range(len(blockMatrix[index])): 
            if (i - index - 1) >= 0:
                gameMatrix[i-index-1][(direction+widthIndex)%60] = "black"
            if blockMatrix[index][widthIndex] != "null":
                gameMatrix[i-index][(direction+widthIndex)%60] = blockMatrix[index][widthIndex]

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

def setRotationRate(rotationRate, score):
    if rotationRate >= 5:
        rotationRate -= math.floor(score/60)*5
    return rotationRate

def rotateMovingBlock(blockMatrix):
    canRotate = True
    if canRotate:
        rotatedBlock = list(zip(*blockMatrix[::-1]))
        for i in range(len(rotatedBlock)):
            rotatedBlock[i] = list(rotatedBlock[i])
        # Ensure block starts at 0th index
        for iteration in range(2):
            #move left
            if rotatedBlock[0][0] == "null" and rotatedBlock[1][0] == "null" and rotatedBlock[2][0] == "null":
                for i in range(len(rotatedBlock)):
                    for w in range(len(rotatedBlock[i])):
                        if w == len(rotatedBlock[i])-1:
                            rotatedBlock[i][w] = "null"
                        else:
                            rotatedBlock[i][w] = rotatedBlock[i][w+1]
            #move up
            if rotatedBlock[0][0] == "null" and rotatedBlock[1][0] == "null" and rotatedBlock[2][0] == "null":
                for i in range(1, len(rotatedBlock)):
                    for w in range(len(rotateCentreBlockEvent[i])):
                        rotatedBlock[i-1][w] = rotatedBlock[i][w]
        return rotatedBlock
    return blockMatrix
        
    
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

    renderScore(score, DEFAULTFONT, SCREEN)
    renderBlocks()
    score = deleteFullLines(score, gameMatrix)
    rotationRate = setRotationRate(rotationRate, score)
    if nextBrick == False:
        nextBrick = getNewBrick(BLOCKS_BY_INDEX)
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
            blockMatrix = getBlockMatrix(movingBrick)
            nextBrick = False
            index = 0
            maxBlockMoves = len(gameMatrix)
            pygame.time.set_timer(fireEvent, brickSpeed, maxBlockMoves)
        if event.type == fireEvent and index < len(gameMatrix):
            canMove = canBlockMove(index, directionToFire, blockMatrix)
            if canMove:
                moveBrick(index, directionToFire, blockMatrix)
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
        if event.type == KEYDOWN and event.key == K_d and blockIsMoving:
            if movingBrick != "cyan" and movingBrick != "magenta":
                blockMatrix = rotateMovingBlock(blockMatrix)

    pygame.display.flip()


pygame.quit()