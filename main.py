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


    # Attributes to track where the mouse is
    app.labelX = 0
    app.labelY = 0

    # Tells whether Link is moving right or left
    app.moveRight = False
    app.moveLeft = False

    # Attributes for grid in the background
    app.rows = 13
    app.cols = 212
    app.levelLeft = -96
    app.levelTop = 16
    app.levelWidth = 6768
    app.levelHeight = 400
    app.cellBorderWidth = 1

    # Lowest possible floor
    app.lowestFloor = app.levelHeight

    # Collision blocks
    app.collisionBlocks, app.mapAs2DList = getRandomWorld(app)

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

    # Brick image from https://www.vhv.rs/viewpic/TihwJTi_mario-brick-png-super-mario-bros-block-pixel/
    app.brick = Image.open('Images/Brick.png')
    app.brick = app.brick.crop((40, 40, 830, 830))
    app.brick = app.brick.resize((32,32))

    # From https://ian-albert.com/games/super_mario_bros_maps/
    app.clouds = Image.open('Images/Background.png')
    app.clouds = app.clouds.crop((0, 0, 3384, 200))
    app.clouds = app.clouds.resize((app.clouds.width * 2, app.clouds.height * 2))

    # From https://www.wallpaperflare.com/super-mario-walk-mustache-grass-vector-backgrounds-illustration-wallpaper-sate/download/2880x1800
    app.ground = Image.open('Images/Ground.jpg')
    app.ground = app.ground.crop((0, 1550, 2880, 1800))
    app.ground = app.ground.resize((app.ground.width//3, app.ground.height//3))

    app.changeInBackground = 0

    

def redrawAll(app):
    # Draws the background
    #drawImage(CMUImage(app.firstLevel), app.levelLeft, 0)
    drawImage(CMUImage(app.clouds), 0, 0)

    drawImage(CMUImage(app.ground), 0, 400)

    # Draw all of the collision blocks
    drawBlocks(app)

    drawArrows(app)

    drawBombs(app)   

    drawLink(app)

    # Draws pointer for (x,y) of mouse
    drawLabel(f'({app.labelX}, {app.labelY})', app.labelX, app.labelY - 10)


# To help with knowing where the mouse is
def onMouseMove(app, mouseX, mouseY):
    app.labelX = mouseX
    app.labelY = mouseY

# Draws collision blocks from list of app.collisionBlocks
def drawBlocks(app):
    for left, top, width, height in app.collisionBlocks:
        drawImage(CMUImage(app.brick), left, top)

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

    if (app.moveLeft):
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
    
    generateWorld(app)
    

def drawArrows(app):
    for arrow in app.arrows:
        drawImage(CMUImage(arrow.image), arrow.arrowLeftX, arrow.arrowTopY)

def drawBombs(app):
    if (len(app.bombs) > 0):
        bomb = app.bombs[0]
        drawImage(CMUImage(bomb.image), bomb.bombLeftX, bomb.bombTopY)

def drawLink(app):
    # Draws Link's boundary box
    drawRect(app.link.leftX, app.link.topY, app.link.linkWidth, 
             app.link.linkHeight, fill = None, border = 'black',borderWidth = 2)
    
    # Draws Link
    drawImage(CMUImage(app.link.image), app.link.leftX, app.link.topY)

def generateWorld(app):
    outOfBoundsLimit = 96
    for left, top, width, height in app.collisionBlocks:
        if (left < -outOfBoundsLimit):
            generateRightCol(app)
        elif (left + width > app.width + outOfBoundsLimit):
            #generateLeftCol(app)
            return 42

    
# Runs game
runApp(app.width, app.height)