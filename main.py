from cmu_graphics import *
from PIL import Image
from Characters import *
from FirstLevel import *

def onAppStart(app):
    # Screen width and height
    app.width = 896
    app.height = 448
    app.stepsPerSecond = 15

    # Get the first level image
    app.firstLevel = Image.open('Images/Mario 1-1.png')
    app.firstLevel = app.firstLevel.resize((app.firstLevel.width * 2, app.firstLevel.height * 2))
    print(app.firstLevel.size)
    
    # Create Link object
    app.link = Link()

    # Attributes to track where the mouse is
    app.labelX = 0
    app.labelY = 0

    # Tells whether Link is moving right or left
    app.moveRight = False
    app.moveLeft = False

    # Attributes for grid in the background
    app.rows = 13
    app.cols = 212
    app.levelLeft = 0
    app.levelTop = 0
    app.levelWidth = 6768
    app.levelHeight = 400
    app.cellBorderWidth = 1

    # Collision blocks
    app.collisionBlocks = []


def redrawAll(app):
    drawFirstLevel(app)
    drawRect(app.link.leftX, app.link.topY, app.link.linkWidth, 
             app.link.linkHeight, fill = None, border = 'black',borderWidth = 2)
    drawImage(CMUImage(app.link.image), app.link.leftX, app.link.topY)
    drawLabel(f'({app.labelX}, {app.labelY})', app.labelX, app.labelY - 10)


def onMouseMove(app, mouseX, mouseY):
    app.labelX = mouseX
    app.labelY = mouseY

def onKeyPress(app, key):
    if (key == 'right'):
        app.moveRight = True
    elif (key == 'left'):
        app.moveLeft = True
    elif (key == 'up' and app.link.isJumping == False):
        app.link.isJumping = True

def onKeyRelease(app, key):
    if (key == 'right'):
        app.moveRight = False
    elif (key == 'left'):
        app.moveLeft = False


def onStep(app):
    if (app.moveRight):
        app.link.move(app, app.link.moveSpeed, 0)
    elif (app.moveLeft):
        app.link.move(app, -(app.link.moveSpeed), 0)
    if (app.link.isJumping):
        app.link.jump()

    

runApp(app.width, app.height)