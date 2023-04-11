from cmu_graphics import *
from PIL import Image
from Characters import *

def drawFirstLevel(app):
    # First draw the background
    drawImage(CMUImage(app.firstLevel), 0, 0)
    for col in range(app.cols):
        drawCell(app, app.rows, col)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill = 'black',
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

