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
    app.levelTop = 16
    app.levelWidth = 6768
    app.levelHeight = 400
    app.cellBorderWidth = 1

    # Lowest possible floor
    app.lowestFloor = app.levelHeight

    # Collision blocks
    app.collisionBlocks = getFirstLevel(app)


def redrawAll(app):
    # Draw all of the collision blocks
    drawBlocks(app)

    # Draws the background
    #drawImage(CMUImage(app.firstLevel), app.levelLeft, 0)

    # Draws Link's boundary box
    drawRect(app.link.leftX, app.link.topY, app.link.linkWidth, 
             app.link.linkHeight, fill = None, border = 'black',borderWidth = 2)
    
    # Draws Link
    drawImage(CMUImage(app.link.image), app.link.leftX, app.link.topY)

    # Draws pointer for (x,y) of mouse
    drawLabel(f'({app.labelX}, {app.labelY})', app.labelX, app.labelY - 10)


# To help with knowing where the mouse is
def onMouseMove(app, mouseX, mouseY):
    app.labelX = mouseX
    app.labelY = mouseY

# Draws collision blocks from list of app.collisionBlocks
def drawBlocks(app):
    for left, top, width, height in app.collisionBlocks:
        drawRect(left, top, width, height)

# Controls movements of Link
def onKeyPress(app, key):
    if (key == 'right'):
        app.moveRight = True
    elif (key == 'left'):
        app.moveLeft = True
    elif (key == 'up' and app.link.isOnGround == True):
        app.link.isOnGround = False
        app.link.isJumping = True

# Makes sure to stop moving Link
def onKeyRelease(app, key):
    if (key == 'right'):
        app.moveRight = False
    elif (key == 'left'):
        app.moveLeft = False

# Moves Link when keys are pressed
def onStep(app):
    if (app.moveRight):
        app.link.move(app, app.link.moveSpeed, 0)
    elif (app.moveLeft):
        app.link.move(app, -(app.link.moveSpeed), 0)
    if (app.link.isJumping):
        app.link.jump()

    
# Runs game
runApp(app.width, app.height)