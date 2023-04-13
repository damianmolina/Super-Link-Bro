from cmu_graphics import *
from PIL import Image
from Characters import *

def drawFirstLevel(app):
    drawImage(CMUImage(app.firstLevel), app.levelLeft, 0)
    drawCell(app, 8, 20)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth = cellHeight = 32
    app.collisionBlocks.append((cellLeft, cellTop, cellWidth, cellHeight))
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill = 'black',
             border='black', borderWidth = app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth = cellHeight = 32
    cellLeft = app.levelLeft + col * cellWidth
    cellTop = app.levelTop + row * cellHeight
    return (cellLeft, cellTop)


