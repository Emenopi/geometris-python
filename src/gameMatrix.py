import math


class GameMatrix():
    def __init__(self, INTERNAL_RADIUS, CENTRE_CIRCLE_RADIUS):
        self.matrix = []
        self.matrixHeight = math.floor((INTERNAL_RADIUS - CENTRE_CIRCLE_RADIUS)/18)
        for i in range(self.matrixHeight):
            self.matrix.append([])
            for j in range(60):
                self.matrix[i].append("black")

    def getHeight(self):
        return self.matrixHeight
    
    def getMatrix(self):
        return self.matrix