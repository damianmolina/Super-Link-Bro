from cmu_graphics import *
from PIL import Image
from Characters import *
import random


def getRandomWorld(app):
    blocks = randomLevel()
    floor = []
    items = []
    rows, cols = len(blocks), len(blocks[0])
    for row in range(rows):
        for col in range(cols):
            if blocks[row][col] == 1:
                floor.append(getCell(app, row, col))
            elif blocks[row][col] == 2:
                items.append(getCell(app, row, col))
    return floor, items, blocks

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

        prevCol = getColAsList(result, col)
        
        if (col == 0):
            prevCol = None
        else:
             prevCol = getColAsList(result, col - 1)
        
        blocks = getBlocks(prevCol)
        
        for i in range(len(blocks)):
            result[-i - 1][col] = blocks[i]

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
    
    for row in range(-1, -rows, -1):
        result.append(L[row][col])
    
    return result
    

def getBlocks(prevCol):
    result = []
    if (prevCol == None):
        prevColLength = 0
    else:
        prevColLength = prevCol.count(1)
    
    prob = random.random()

    if (prevColLength == 0):
        for i in range(random.randint(1, 2)):
            result.append(1)
    elif (prevColLength >= 7):
        for i in range(prevColLength - random.randint(1, 2)):
            result.append(1)
    else:
        if (prob > 0.5):
            for i in range(prevColLength + random.randint(1, 2)):
                result.append(1)
        else:
            for i in range(prevColLength - random.randint(1, 2)):
                result.append(1)

    itemBlockPos = len(result) + random.randint(2, 3)
    if (prevCol != None and prob > 0.9):
        if (itemBlockPos < len(prevCol) 
            and not prevCol[itemBlockPos] in {1, 2}
            and not prevCol[itemBlockPos - 1] == 2):
            for i in range(itemBlockPos - len(result)):
                result.append(0)
            result.append(2)
    elif (prob > 0.9):
        for i in range(itemBlockPos - len(result)):
            result.append(0)
        result.append(2)
        
    return result

def generateRightCol(app):
    L = app.mapAs2DList
    newLevel = shiftLeft(L)
    rows, cols = len(newLevel), len(newLevel[0])
    prevCol = getColAsList(newLevel, cols - 2)
    newBlocks = getBlocks(prevCol)
    
    for i in range(len(newBlocks)):
        newLevel[-i - 1][-1] = newBlocks[i]
    
    app.mapAs2DList = newLevel

    generateNewWorld(app)

def generateLeftCol(app):
    L = app.mapAs2DList
    newLevel = shiftRight(L)
    prevCol = getColAsList(newLevel, 1)
    newBlocks = getBlocks(prevCol)
    
    for i in range(len(newBlocks)):
        newLevel[-i - 1][0] = newBlocks[i]

    app.mapAs2DList = newLevel

    generateNewWorld(app)


def shiftLeft(L):
    emptyList = createEmpty2DList()
    rows, cols = len(emptyList), len(emptyList[0])
    for i in range(rows):
        for j in range(cols - 1):
            emptyList[i][j] = L[i][j + 1]

    result = emptyList

    return result

def shiftRight(L):
    emptyList = createEmpty2DList()
    rows, cols = len(emptyList), len(emptyList[0])

    for i in range(rows):
        for j in range(cols):
            if (j == 0): continue
            emptyList[i][j] = L[i][j - 1]

    result = emptyList

    return result

def generateNewWorld(app):
    floor = []
    items = []
    rows, cols = len(app.mapAs2DList), len(app.mapAs2DList[0])
    for row in range(rows):
        for col in range(cols):
            if app.mapAs2DList[row][col] == 1:
                floor.append(getCell(app, row, col))
            elif app.mapAs2DList[row][col] == 2:
                items.append(getCell(app, row, col))
    app.collisionBlocks = floor
    app.itemBlocks = items

def moveEverything(app, dx, dy):
    for i in range(len(app.collisionBlocks)):
        left, top, width, height = app.collisionBlocks[i]
        newLeft, newTop = left + dx, top + dy
        app.collisionBlocks[i] = (newLeft, newTop, width, height)
    
    for i in range(len(app.itemBlocks)):
        left, top, width, height = app.itemBlocks[i]
        newLeft, newTop = left + dx, top + dy
        app.itemBlocks[i] = (newLeft, newTop, width, height)

    for tektite in app.tektites:
        tektite.leftX += dx
        tektite.centerX += dx
    
    for arrow in app.arrows:
        arrow.arrowLeftX += dx
        arrow.arrowCenterX += dx

    for bomb in app.bombs:
        bomb.bombLeftX += dx
        bomb.bombCenterX += dx