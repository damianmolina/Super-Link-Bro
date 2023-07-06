from cmu_graphics import *
from PIL import Image
from Characters import *
import random

# Generates initial random world when game is loaded
def getRandomWorld(app):
    # Main helper function to create world. Outputs a 2D list with 1's for ground/brick
    # and 2's for item blocks
    blocks = randomLevel()

    # These will be used to store location of blocks on the screen grid
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
# the code is modified to help fit the game
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
    # First creates an empty 2D list
    result = createEmpty2DList()
    rows, cols = len(result), len(result[0])

    for col in range(cols):
        # Gets the previous column from terrain
        prevCol = getColAsList(result, col)
        
        # If at first column, there is no previous column
        if (col == 0):
            prevCol = None
        else:
             # Gets column as a 1D list
             prevCol = getColAsList(result, col - 1)
        
        # Helper function that gets the next column of blocks
        blocks = getBlocks(prevCol)
        
        # Places the new blocks into the empty 2D list
        for i in range(len(blocks)):
            result[-i - 1][col] = blocks[i]

    return result

# Creates a empty 2D list with specified rows and columns
def createEmpty2DList():
    result = []
    rows = 12
    cols = 34
    for _ in range(rows):
        result.append([0] * cols)
    return result

# Transforms a column into a list
def getColAsList(L, col):
    result = []
    rows = len(L)
    
    for row in range(-1, -rows, -1):
        result.append(L[row][col])
    
    return result

# Gets a new, randomly generates column of both bricks and item blocks
def getBlocks(prevCol):
    result = []
    # If there was no previous column, the length of it is automatically 0
    if (prevCol == None):
        prevColLength = 0
    else:
        # Gets the number of bricks from column
        prevColLength = prevCol.count(1)
    
    prob = random.random()

    # If previous column had no ground, add 1-2 bricks in this column
    if (prevColLength == 0):
        for _ in range(random.randint(1, 2)):
            result.append(1)
    # If previous column already had quite a few bricks, add 1-2 bricks FEWER
    # into this column
    elif (prevColLength >= 7):
        for _ in range(prevColLength - random.randint(1, 2)):
            result.append(1)
    else:
        # Either add more or fewer bricks than the previous column
        if (prob > 0.5):
            for _ in range(prevColLength + random.randint(1, 2)):
                result.append(1)
        else:
            for _ in range(prevColLength - random.randint(1, 2)):
                result.append(1)

    # Position of item block
    itemBlockPos = len(result) + random.randint(2, 3)

    # If there is a previous column, make sure that two item blocks won't be
    # right next to each other (same applies for item block being next to brick)
    if (prevCol != None and prob > 0.95):
        if (itemBlockPos < len(prevCol) 
            and not prevCol[itemBlockPos] in {1, 2}
            and not prevCol[itemBlockPos - 1] == 2):
            for _ in range(itemBlockPos - len(result)):
                result.append(0)
            result.append(2)
    elif (prob > 0.95):
        for _ in range(itemBlockPos - len(result)):
            result.append(0)
        result.append(2)
        
    return result

# Generates new column to the right of the level
def generateRightCol(app):
    L = app.mapAs2DList
    # Shifts old level to the left
    newLevel = shiftLeft(L)
    cols = len(newLevel[0])
    # Gets previous column (which is the furthest right col in level)
    prevCol = getColAsList(newLevel, cols - 2)
    # Gets new, random column
    newBlocks = getBlocks(prevCol)
    # Adds this new column into the new level
    for i in range(len(newBlocks)):
        newLevel[-i - 1][-1] = newBlocks[i]
    
    # Assigns new level to app atribute
    app.mapAs2DList = newLevel

    # Loads up this new world
    generateNewWorld(app)

# Generates new column to the left of the level
def generateLeftCol(app):
    L = app.mapAs2DList
    # Shifts old level to the right
    newLevel = shiftRight(L)
    # Gets previous column (which is the furthest left col in level)
    prevCol = getColAsList(newLevel, 1)
    # Gets new, random column
    newBlocks = getBlocks(prevCol)
    # Adds this new column into the new level
    for i in range(len(newBlocks)):
        newLevel[-i - 1][0] = newBlocks[i]

    # Assigns new level to app atribute
    app.mapAs2DList = newLevel

    # Loads up this new world
    generateNewWorld(app)

# Shifts 2D level list to the left
def shiftLeft(L):
    # Gets empty list first
    emptyList = createEmpty2DList()
    rows, cols = len(emptyList), len(emptyList[0])
    # Copies over necessary values 
    for i in range(rows):
        for j in range(cols - 1):
            emptyList[i][j] = L[i][j + 1]

    result = emptyList

    return result

# Shifts 2D level list to the right
def shiftRight(L):
    # Gets empty list first
    emptyList = createEmpty2DList()
    rows, cols = len(emptyList), len(emptyList[0])
    # Copies over necessary values 
    for i in range(rows):
        for j in range(cols):
            if (j == 0): continue
            emptyList[i][j] = L[i][j - 1]

    result = emptyList

    return result

# Loads up new world once new column has been generated
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
    # Re-assigns app atributes to new blocks
    app.collisionBlocks = floor
    app.itemBlocks = items
    app.allBlocks = app.collisionBlocks + app.itemBlocks

# Moves all blocks and enemies when Link is moving
def moveEverything(app, dx, dy):
    # Moves bricks
    for i in range(len(app.collisionBlocks)):
        left, top, width, height = app.collisionBlocks[i]
        newLeft, newTop = left + dx, top + dy
        app.collisionBlocks[i] = (newLeft, newTop, width, height)
    # Moves item blocks
    for i in range(len(app.itemBlocks)):
        left, top, width, height = app.itemBlocks[i]
        newLeft, newTop = left + dx, top + dy
        app.itemBlocks[i] = (newLeft, newTop, width, height)
    # Moves items on top of item blocks
    for item in app.items:
        item.leftX += dx
        
    # Moves tektites
    for tektite in app.tektites:
        tektite.leftX += dx
        tektite.centerX += dx
    
    for stalfo in app.stalfos:
        stalfo.leftX += dx
        stalfo.centerX += dx
        
    # Moves arrows
    for arrow in app.arrows:
        arrow.leftX += dx
        arrow.centerX += dx

    # Moves bombs
    for bomb in app.bombs:
        bomb.leftX += dx
        bomb.centerX += dx