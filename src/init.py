import pygame
from pygame.locals import *
import math

SCREEN_SIZE = 900
OUTER_CIRCLE_DIM = SCREEN_SIZE*0.91
SCREEN = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
boundaryCircle = pygame.image.load('assets/circle.png')
boundaryCircle = pygame.transform.scale(boundaryCircle, (OUTER_CIRCLE_DIM, OUTER_CIRCLE_DIM))
pygame.display.set_icon(boundaryCircle)
BORDER = (SCREEN_SIZE-OUTER_CIRCLE_DIM)/2
CENTRE = SCREEN_SIZE/2
INTERNAL_RADIUS = (OUTER_CIRCLE_DIM/2)*0.88
CENTRE_CIRCLE_RADIUS = math.floor(INTERNAL_RADIUS/4)

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


def gridMatrix ():
    matrix = []
    matrixHeight = math.floor((INTERNAL_RADIUS - CENTRE_CIRCLE_RADIUS)/18)
    for i in range(matrixHeight):
        matrix.append([])
        for j in range(60):
            matrix[i].append("black")
    return matrix, matrixHeight

gameMatrix, MATRIX_HEIGHT = gridMatrix()
BLOCK_MIN_SCALE = ((MATRIX_HEIGHT/100)*1.5, (MATRIX_HEIGHT/100)*3)
MARGIN = 25