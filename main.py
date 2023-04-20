from cmu_graphics import *
from PIL import Image
from Characters import *
from Weapons import *
from RandomWorld import *
import random

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
    app.collisionBlocks, app.itemBlocks, app.mapAs2DList = getRandomWorld(app)
    app.allBlocks = app.collisionBlocks + app.itemBlocks

    # Create Link object
    app.link = Link(app)

    # Arrows
    app.arrows = list()

    # Bombs
    app.bombs = list()

    # Tektites
    app.tektites = list()

    # Stalfos
    app.stalfos = list()

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

    # From https://www.pixilart.com/art/mario-block-pixel-79dace9a1d2f29a
    app.itemBlock = Image.open('Images/ItemBlock.png')
    app.itemBlock = app.itemBlock.resize((32, 32))

    app.changeInBackground = 0

    app.timer = 0
    app.switchTimer = True
    app.prob = random.random()

    

def redrawAll(app):
    # Draws the background
    drawImage(CMUImage(app.clouds), 0, 0)

    drawImage(CMUImage(app.ground), 0, 400)

    # Draw all of the blocks
    drawBlocks(app)

    drawArrows(app)

    drawBombs(app)   

    drawLink(app)

    drawEnemies(app)

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
    
    for left, top, width, height in app.itemBlocks:
        drawImage(CMUImage(app.itemBlock), left, top)


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

# Makes sure to stop moving Link left or rightd.a
def onKeyRelease(app, key):
    if (key == 'd'):
        app.moveRight = False
    elif (key == 'a'):
        app.moveLeft = False

def onStep(app):
    app.allBlocks = app.collisionBlocks + app.itemBlocks
    app.timer += 1
    if (app.timer % 32 == 0): 
        app.switchTimer = not app.switchTimer

    if (app.moveRight):
        app.link.move(app, app.link.moveSpeed, 0)

    if (app.moveLeft):
        app.link.move(app, -(app.link.moveSpeed), 0)

    if (app.link.isJumping):
        app.link.jump()

    if (app.link.isFalling):
        app.link.fall()
    
    for arrow in app.arrows:
        if (arrow.hasCollided):
            app.arrows.remove(arrow)
        else:
            arrow.shoot()

    
    if (len(app.bombs) > 0):
        if (app.bombs[0].hasCollided):
            app.bombs.pop()
        else:
            app.bombs[0].move(app)

    totalNumOfEnemies = len(app.tektites) + len(app.stalfos)
    if (totalNumOfEnemies < 4):
        prob = random.random()
        if (prob > 0.9):
            if (prob > 0.95):
                app.tektites.append(Tektite(app))
  
    if (app.switchTimer):
        for tektite in app.tektites:
            if (app.prob > 0.3):
                tektite.moveTowardLink(app, tektite.moveSpeed)
            else:
                tektite.moveAwayFromLink(app, tektite.moveSpeed)

            prob = random.random()
            if (prob > 0.98):
                tektite.isJumping = True
    else:
        app.prob = random.random()
    
    for tektite in app.tektites:
        if (tektite.isJumping):
            tektite.jump()
        if (tektite.isFalling):
            tektite.fall()
        
        
        if (tektite.leftX < -64 or tektite.leftX > 928 or tektite.topY > 400):
            app.tektites.remove(tektite)
        
        if (tektite.health == 0):
            app.tektites.remove(tektite)
    
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
             app.link.linkHeight, fill = None, border = 'black', borderWidth = 2)
    
    # Draws Link
    drawImage(CMUImage(app.link.image), app.link.leftX, app.link.topY)

def drawEnemies(app):
    for tektite in app.tektites:
        drawImage(CMUImage(tektite.image), tektite.leftX, tektite.topY)
        #drawRect(tektite.leftX, tektite.topY, tektite.width, tektite.height, fill=None, border='black')
    
    for stalfo in app.stalfos:
        drawImage(CMUImage(stalfo.image), stalfo.stalfoLeftX, stalfo.stalfoTopY)

def generateWorld(app):
    if (app.changeInBackground == -32):
        generateRightCol(app)
        app.changeInBackground = 0
    elif (app.changeInBackground == 32):
        generateLeftCol(app)
        app.changeInBackground = 0

    
# Runs game
runApp(app.width, app.height)