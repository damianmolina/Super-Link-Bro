from cmu_graphics import *
from PIL import Image
from Characters import *
import random

# Draws all of the blocks from level 1
def getRandomWorld(app):
    blocks = randomLevel()
    result = []
    rows, cols = len(blocks), len(blocks[0])
    for row in range(rows):
        for col in range(cols):
            if blocks[row][col] == 1:
                result.append(getCell(app, row, col))
    return result, blocks

# These methods are from CSAcademy exercises relating to drawing grids, however,
# the code is modified to help fit my game
def getCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth = cellHeight = 32
    cell = (cellLeft, cellTop, cellWidth, cellHeight)
    return cell

def getCellLeftTop(app, row, col):
    cellWidth = cellHeight = 32
    cellLeft = app.levelLeft + col * cellWidth
    cellTop = app.levelTop + row * cellHeight
    return (cellLeft, cellTop)

# Creates a randomly generated 2D list for the terrain
def randomLevel():
    result = createEmpty2DList()
    rows, cols = len(result), len(result[0])
    for col in range(cols):
        #if (col in {num for num in range(15)}): continue

        prevCol = getColAsList(result, col)
        
        if (col == 0):
            prevCol = None
        else:
             prevCol = getColAsList(result, col - 1)
        
        numOfBlocks = getBlocks(prevCol)
        
        for i in range(numOfBlocks):
            result[-i - 1][col] = 1
    
    return result

# Creates a empty 2D list with specified rows and columns
def createEmpty2DList():
    result = []
    rows = 12
    cols = 34
    for row in range(rows):
        result.append([0] * cols)
    return result


# Transforms a column into a list
def getColAsList(L, col):
    result = []
    rows = len(L)
    
    for row in range(rows):
        result.append(L[row][col])
    
    return result
    
# This randomly generates how many blocks will be in each column, which is also
# dependent on the previous column
def getBlocks(prevCol):
    if (prevCol == None):
        prevColLength = 0
    else:
        prevColLength = prevCol.count(1)
    
    prob = random.random()
    
    if (prevColLength == 0):
        return prevColLength + random.randint(1, 2)
    elif (prevColLength >= 10):
        return prevColLength - random.randint(1, 2)
    else:
        if (prob > 0.5):
            return prevColLength + random.randint(1, 2)
        else:
            return abs(prevColLength - random.randint(1, 2))

def generateRightCol(app):
    L = shiftLeft(app)
    rows, cols = len(L), len(L[0])
    prevCol = getColAsList(L, cols - 2)
    numOfNewBlocks = getBlocks(prevCol)

    for i in range(numOfNewBlocks):
        L[-i - 1][-1] = 1
    
    app.mapAs2DList = L

    generateNewWorld(app)

def generateLeftCol(app):
    L = shiftRight(app)
    rows, cols = len(L), len(L[0])
    prevCol = getColAsList(L, 1)
    numOfNewBlocks = getBlocks(prevCol)
    
    for i in range(numOfNewBlocks):
        L[-i - 1][0] = 1
    
    app.mapAs2DList = L

    generateNewWorld(app)


def shiftLeft(app):
    emptyList = createEmpty2DList()
    rows, cols = len(emptyList), len(emptyList[0])
    for i in range(rows):
        for j in range(cols - 1):
            emptyList[i][j] = app.mapAs2DList[i][j + 1]

    result = emptyList

    return result

def shiftRight(app):
    emptyList = createEmpty2DList()
    rows, cols = len(emptyList), len(emptyList[0])

    for i in range(rows):
        for j in range(cols):
            if (j == 0): continue
            emptyList[i][j] = app.mapAs2DList[i][j - 1]

    result = emptyList

    return result

def generateNewWorld(app):
    result = []
    rows, cols = len(app.mapAs2DList), len(app.mapAs2DList[0])
    for row in range(rows):
        for col in range(cols):
            if app.mapAs2DList[row][col] == 1:
                result.append(getCell(app, row, col))

    app.collisionBlocks = result
