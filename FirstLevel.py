from cmu_graphics import *
from PIL import Image

# Draws all of the blocks from level 1
def getFirstLevel(app):
    blocks = getRowsAndCols()
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

# Moves all of the blocks from level 1
def moveBlocks(app, dx, dy):
    for i in range(len(app.collisionBlocks)):
        left, top, width, height = app.collisionBlocks[i]
        newLeft, newTop = left + dx, top + dy
        app.collisionBlocks[i] = (newLeft, newTop, width, height)

# Creates a 2D list with "1" where blocks are to be placed
def getRowsAndCols():
    result = []
    for row in range(app.rows):
        currRow = []
        for col in range(app.cols):
            if (row in {0, 1, 2, 3}):
                currRow.append(0)
            elif (row == 11 and col == 16):
                currRow.append(1)
            elif (row == 8 and col == 20):
                currRow.append(1)
            elif (row == 8 and col == 21):
                currRow.append(1)
            elif (row == 8 and col == 22):
                currRow.append(1)
            elif (row == 8 and col == 23):
                currRow.append(1)
            elif (row == 8 and col == 24):
                currRow.append(1)
            elif (row == 4 and col == 22):
                currRow.append(1)
            else:
                currRow.append(0)
        result.append(currRow)
    return result


