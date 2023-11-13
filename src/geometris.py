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
    if i+1 < len(blockMatrix):
        checkDepth = i+1
    else:
        checkDepth = len(blockMatrix)

    for index in range(checkDepth):
        for width in range(len(blockMatrix[index])):
            if blockMatrix[index][width][0] != "null":
                if gameMatrix[i-index][(direction+width)%60] != "black" and len(gameMatrix[i-index][(direction+width)%60]) > 2:
                    return False
            elif len(blockMatrix[index]) < len(blockMatrix[index-1]):
                checkWidth = len(blockMatrix[index]) - len(blockMatrix[index-1])
                for w in range(1, checkWidth):
                    if gameMatrix[i-index][direction+w] != "black":
                        return False
    return True

def tagMovingBrick(blockMatrix):
    for i in range(len(blockMatrix)):
        for j in range(len(blockMatrix[i])):
            if len(blockMatrix[i][j]) > 2:
                blockMatrix[i][j] = [blockMatrix[i][j], "moving"]
    return blockMatrix

def removeBrickTag(gameMatrix):
    for i in range(len(gameMatrix)):
        for width in range (len(gameMatrix[i])):
            if len(gameMatrix[i][width]) <= 2:
                gameMatrix[i][width] = gameMatrix[i][width][0]

def removeNullBricks(direction, gameMatrix):
    for i in range(len(gameMatrix)):
        for width in range(len(gameMatrix[i][direction]), 5):
            if gameMatrix[i][(direction + width)%60]  == "null":
                gameMatrix[i][(direction + width)%60] = "black"

def moveBrick(i, direction, blockMatrix):
    blockMatrix = tagMovingBrick(blockMatrix)
    if i+1 < len(blockMatrix):
        iterations = i+1
    else:
        iterations = len(blockMatrix)

    for index in range(iterations):
        for widthIndex in range(len(blockMatrix[index])): 
            if (i - index - 1) >= 0:
                gameMatrix[i-index-1][(direction+widthIndex)%60] = "black"
            if blockMatrix[index][widthIndex][0] != "null":
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
                if len(gameMatrix[i][j]) <= 2:
                    if gameMatrix[i][j][0] == "null":
                        currentBlock = blackBlock
                    else:
                        currentBlock = BLOCKS_BY_NAME[gameMatrix[i][j][0]]
                else:
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

def rotateMovingBlock(index, direction, blockMatrix):
    rotatedBlockMatrix = list(zip(*blockMatrix[::-1]))
    for i in range(len(rotatedBlockMatrix)):
        rotatedBlockMatrix[i] = list(rotatedBlockMatrix[i])
    # Ensure block starts at 0th index
    for iteration in range(2):
        #move left
        if rotatedBlockMatrix[0][0][0] == "null" and rotatedBlockMatrix[1][0][0] == "null" and rotatedBlockMatrix[2][0][0] == "null":
            for i in range(len(rotatedBlockMatrix)):
                for w in range(len(rotatedBlockMatrix[i])):
                    if w == len(rotatedBlockMatrix[i])-1:
                        rotatedBlockMatrix[i][w][0] = "null"
                    else:
                        rotatedBlockMatrix[i][w][0] = rotatedBlockMatrix[i][w+1][0]
        #move up
        if rotatedBlockMatrix[0][0][0] == "null" and rotatedBlockMatrix[1][0][0] == "null" and rotatedBlockMatrix[2][0][0] == "null":
            for i in range(1, len(rotatedBlockMatrix)):
                for w in range(len(rotatedBlockMatrix[i])):
                    rotatedBlockMatrix[i-1][w][0] = rotatedBlockMatrix[i][w][0]
    canRotate = canBlockRotate(index, direction, rotatedBlockMatrix, blockMatrix)
    if canRotate:
        return rotatedBlockMatrix
    return blockMatrix

def canBlockRotate(i, direction, rotatedMatrix, originalBlock):
    for index in range(len(rotatedMatrix)):
        for widthIndex in range(len(rotatedMatrix[index])):
            if gameMatrix[i-index][(direction+widthIndex)%60] != "black" and rotatedMatrix[index][widthIndex] != "null":
                if len(gameMatrix[i-index][(direction+widthIndex)%60]) > 2:
                    return False
    return True

    
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
                removeBrickTag(gameMatrix)
                removeNullBricks(directionToFire, gameMatrix)
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
        if event.type == KEYDOWN and event.key == K_SPACE and blockIsMoving:
            if movingBrick != "cyan" and movingBrick != "magenta":
                blockMatrix = rotateMovingBlock(index, directionToFire, blockMatrix)

    pygame.display.flip()


pygame.quit()