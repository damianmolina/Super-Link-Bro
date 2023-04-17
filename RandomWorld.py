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
    return result

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
        if (col in {num for num in range(15)}): continue

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
    cols = 50
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