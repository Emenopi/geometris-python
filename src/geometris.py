import pygame
from pygame.locals import *
import math


class Geometris():    
    def __init__(self):
        self.SCREEN_SIZE = 900
        self.SCREEN = pygame.display.set_mode((self.SCREEN_SIZE, self.SCREEN_SIZE))
        self.OUTER_CIRCLE_DIM = self.SCREEN_SIZE*0.91
        self.CENTRE = self.SCREEN_SIZE/2
        self.boundaryCircle = pygame.image.load('assets/circle.png')
        self.boundaryCircle = pygame.transform.scale(self.boundaryCircle, (self.OUTER_CIRCLE_DIM, self.OUTER_CIRCLE_DIM))
        pygame.display.set_icon(self.boundaryCircle)
        self.INTERNAL_RADIUS = (self.OUTER_CIRCLE_DIM/2)*0.88
        self.CENTRE_CIRCLE_RADIUS = math.floor(self.INTERNAL_RADIUS/4)
        self.load_blocks()

        self.BLOCKS_BY_NAME = {"cyan": self.cyanBlock, 
                        "purple": self.purpleBlock, 
                        "magenta": self.magentaBlock, 
                        "orange": self.orangeBlock, 
                        "yellow": self.yellowBlock, 
                        "green": self.greenBlock,
                        "black": self.blackBlock}

    def load_blocks(self): 
        self.cyanBlock = pygame.image.load('assets/cyan.png')
        self.purpleBlock = pygame.image.load('assets/purple.png')
        self.magentaBlock = pygame.image.load('assets/magenta.png')
        self.orangeBlock = pygame.image.load('assets/orange.png')
        self.yellowBlock = pygame.image.load('assets/yellow.png')
        self.greenBlock = pygame.image.load('assets/green.png')
        self.blackBlock = pygame.image.load('assets/black.png')

    def getBlocks(self):
        return self.BLOCKS_BY_NAME

    def getInternalRadius(self):
        return self.INTERNAL_RADIUS
    
    def getCentreCircleRadius(self):
        return self.CENTRE_CIRCLE_RADIUS
    
    def getScreen(self):
        return self.SCREEN
    
    def getScreenSize(self):
        return self.SCREEN_SIZE
    
    def getCentre(self):
        return self.CENTRE
    
    def getBoundaryCircle(self):
        return self.boundaryCircle
    
    def getOuterCircleDim(self):
        return self.OUTER_CIRCLE_DIM
    


