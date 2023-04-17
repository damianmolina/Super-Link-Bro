from cmu_graphics import *
from PIL import Image
from Characters import *
from FirstLevel import *
from Weapons import *
from RandomWorld import *

def onAppStart(app):
    # Screen width and height
    app.width = 896
    app.height = 448
    app.stepsPerSecond = 15

    # Get the first level image
    app.firstLevel = Image.open('Images/Mario 1-1.png')
    app.firstLevel = app.firstLevel.resize((app.firstLevel.width * 2, app.firstLevel.height * 2))

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

    # Create Link object
    app.link = Link(app)

    # Arrows
    app.arrows = list()

    # Bombs
    app.bombs = list()

    # Tektite
    app.tektite = Tektite(app)

    # Stalfo
    app.stalfo = Stalfo(app)
    

def redrawAll(app):
    # Draws the background
    drawImage(CMUImage(app.firstLevel), app.levelLeft, 0)

    # Draw all of the collision blocks
    drawBlocks(app)

    drawArrows(app)

    drawBombs(app)   

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
    if (key == 'd'):
        app.moveRight = True
    elif (key == 'a'):
        app.moveLeft = True
    elif (key == 'w' and app.link.isOnGround == True):
        app.link.isOnGround = False
        app.link.isJumping = True
    elif (key == 'p'):
        app.arrows.append(Arrow(app))
    elif (key == 'o'):
        app.bombs.append(Bomb(app))

# Makes sure to stop moving Link
def onKeyRelease(app, key):
    if (key == 'd'):
        app.moveRight = False
    elif (key == 'a'):
        app.moveLeft = False

# Moves Link when keys are pressed
def onStep(app):
    if (app.moveRight):
        app.link.move(app, app.link.moveSpeed, 0)
    elif (app.moveLeft):
        app.link.move(app, -(app.link.moveSpeed), 0)

    if (app.link.isJumping):
        app.link.jump()
    if (app.link.isFalling):
        app.link.fall()
    
    for arrow in app.arrows:
        if (arrow.arrowLeftX < 0 or arrow.arrowLeftX > app.width):
            app.arrows.remove(arrow)
        else:
            arrow.shoot()
    
    if (len(app.bombs) > 0):
        if (app.bombs[0].hasCollided):
            app.bombs.pop()
        else:
            app.bombs[0].move(app)

def drawArrows(app):
    for arrow in app.arrows:
        drawImage(CMUImage(arrow.image), arrow.arrowLeftX, arrow.arrowTopY)

def drawBombs(app):
    if (len(app.bombs) > 0):
        bomb = app.bombs[0]
        drawImage(CMUImage(bomb.image), bomb.bombLeftX, bomb.bombTopY)        

    
# Runs game
runApp(app.width, app.height)