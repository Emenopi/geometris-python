def renderScore(score, font, SCREEN):
    scoreImg = font.render("SCORE: %s" % str(score), 1, (255, 0, 128))
    scoreRect = scoreImg.get_rect()
    SCREEN.blit(scoreImg, (scoreRect[0]+10, scoreRect[1]+10))
    
def checkFullLines(matrix):
    fullLine = False
    lineIndex = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "black":
                break
            elif j == (len(matrix[i])-1) and matrix[i][j] != "black":
                fullLine = True
                lineIndex = i
        if fullLine == True:
            break
    return fullLine, lineIndex

def deleteFullLines(score, matrix):
    fullLine, lineIndex = checkFullLines(matrix)
    if fullLine == True:
        for i in range(lineIndex, -1, -1):
            for j in range(len(matrix[i])):
                if i == 0:
                    matrix[i][j] = "black"
                else:
                    matrix[i][j] = matrix[i-1][j]
        score += 60
    return score
