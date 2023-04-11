from cmu_graphics import *
from PIL import Image
from Characters import *

def drawFirstLevel(app):
    # First draw the background
    drawImage(CMUImage(app.firstLevel), app.levelLeft, 0)
    for col in range(app.cols):
        drawCell(app, app.rows, col)

def drawCell(app, row, col):
    if (col % 2 == 0):
        color = 'black'
    else:
        color = 'red'
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    app.collisionBlocks.append((cellLeft, cellTop, cellWidth, cellHeight))
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill = color,
             border='black', borderWidth = app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.levelLeft + col * cellWidth
    cellTop = app.levelTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.levelWidth / app.cols
    cellHeight = app.levelHeight / app.rows
    return (cellWidth, cellHeight)

