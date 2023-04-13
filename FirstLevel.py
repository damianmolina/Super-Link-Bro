from cmu_graphics import *
from PIL import Image
from Characters import *

# Draws all of the blocks from level 1
def getFirstLevel(app):
    return getCell(app, 11, 16)

# These methods are from CSAcademy exercises relating to drawing grids, however,
# the code is modified to help fit my game
def getCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth = cellHeight = 32
    cell = (cellLeft, cellTop, cellWidth, cellHeight)
    return [cell]

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


