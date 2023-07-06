from cmu_graphics import *
from PIL import Image
from Characters import *
from Weapons import *
from RandomWorld import *
from Items import *
import random


def onAppStart(app):
    # Restart the game once Link has lost all of his health
    restartApp(app)

def restartApp(app):
    # Screen width and height
    app.width = 896
    app.height = 448
    app.stepsPerSecond = 14

    # Game begins with a start screen
    app.startScreen = True
    # Image was drawn from myself using a pixel art editor
    app.startingScreenImage = Image.open('Images/StartingScreen.png')

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

    # All blocks
    app.allBlocks = app.collisionBlocks + app.itemBlocks

    # Create Link object
    app.link = Link(app)
    
    # Link has five hearts
    app.lives = list()

    # Arrows
    app.arrows = list()
    # Timer to ensure that arrows can't be spammed when shooting
    app.arrowTimer = 0

    # Bombs
    app.bombs = list()

    # Tektites
    app.tektites = list()

    # Stalfos
    app.stalfos = list()

    # All enemies
    app.enemies = app.tektites + app.stalfos

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

    # This attribute will help determine when the background should change
    app.changeInBackground = 0

    # Timer for moving/jumping with enemies
    app.timer = 0

    # Timer to create a buffer for how often Link is attacked
    app.checkEnemyTimer = 0

    # Alternates to not make the enemies move constantly
    app.switchTimer = True

    # This is the limit for which the player can earn points from moving (it will
    # increase as time goes on)
    app.movementPointsLimit = 300
    # Makes sure that Link has killed an enemy to allow for more points when moving
    app.hasKilledEnemy = False

    # Probability for enemies to spawn
    app.prob = random.random()

    # Items that show up from item blocks
    app.items = list()

    # Accesses score text file which keeps highest score 
    scoreText = open("Score.txt", "r")
    app.highScore = int(scoreText.read())
    scoreText.close()

    # Keeps track of the current score 
    app.currentScore = 0
    


def redrawAll(app):
    if (app.startScreen):
        # Draws start screen with high score shown
        drawStartScreen(app)
        drawHighScore(app)
    else:
        # Draws the background (COMMENT THESE OUT FOR THE GAME TO RUN LONGER)
        drawImage(CMUImage(app.clouds), 0, 0)
        drawImage(CMUImage(app.ground), 0, 400)

        # Draws all of the blocks
        drawBlocks(app)

        # Draws the arrows
        drawArrows(app)

        # Draws the bombs
        drawBombs(app)   

        # Draws Link
        drawLink(app)

        # Draws the enemies
        drawEnemies(app)

        # Draws the items that appear on top of item blocks
        drawItems(app)

        # Draws hearts to represent how many more hits Link can take
        drawHealth(app)

        # Draws current score that the player has gotten so far
        drawScore(app)


def onStep(app):
    if (not app.startScreen):
        # Constantly updates location of all blocks
        app.allBlocks = app.collisionBlocks + app.itemBlocks

        # Constantly updates total number of enemies
        app.enemies = app.tektites + app.stalfos

        # Each timer increases by one when onStep(app) is called
        app.timer += 1
        app.checkEnemyTimer += 1
        app.arrowTimer += 1

        # If Link's health is <= 0, game is over --> restarts game
        if (app.link.health <= 0):
            scoreText = open('Score.txt', 'r+')
            prevHighScore = int(scoreText.read())
            # Check if current score is higher than previous high score, if so,
            # replace text file with new high score
            if (app.currentScore > prevHighScore):
                newHighScore = open('Score.txt', 'w')
                newHighScore.write(str(app.currentScore))
                newHighScore.close()
            scoreText.close()

            # Restart the game
            restartApp(app)

        # This is the buffer time for enemy movement
        if (app.timer % 32 == 0): 
            app.switchTimer = not app.switchTimer

        # Following methods move Link based on key presses
        if (app.moveRight):
            app.link.move(app, app.link.moveSpeed, 0)

        if (app.moveLeft):
            app.link.move(app, -(app.link.moveSpeed), 0)

        if (app.link.isJumping):
            app.link.jump()

        if (app.link.isFalling):
            app.link.fall()
        

        # Cycles through arrows to see whether they've collided. If not, continues
        # to move them 
        for arrow in app.arrows:
            if (arrow.hasCollided):
                app.arrows.remove(arrow)
            else:
                arrow.shoot()

        # Cycles through bombs to see whether they've collided. If not, continues
        # to move them  
        if (len(app.bombs) > 0):
            if (app.bombs[0].hasCollided):
                app.bombs.pop()
            else:
                app.bombs[0].move(app)

        totalNumOfEnemies = len(app.tektites) + len(app.stalfos)
        # Will only spawn up to five enemies max
        if (totalNumOfEnemies < 4):
            prob = random.random()
            if (prob > 0.95):
                if (prob > 0.97):
                    app.tektites.append(Tektite(app))
                else:
                    app.stalfos.append(Stalfo(app))
    
        if (app.switchTimer):
            for enemy in app.enemies:
                # 80% chance of moving toward Link, 20% of moving away
                if (app.prob > 0.2):
                    enemy.moveTowardLink(app, enemy.moveSpeed)
                else:
                    enemy.moveAwayFromLink(app, enemy.moveSpeed)

                prob = random.random()
                # 10% chance of jumping
                if (prob > 0.9 and enemy.isJumping == False):
                    enemy.isJumping = True
        else:
            # Changes the probability attribute of app
            app.prob = random.random()
        
        # Cycles through tektites and stalfos to move them or delete them 
        # if their health <= 0 or if they're out of bounds
        for tektite in app.tektites:
            if (tektite.isJumping):
                tektite.jump()
            if (tektite.isFalling):
                tektite.fall()
            
            if (tektite.leftX < -64 or tektite.leftX > 956 or tektite.topY > 400):
                app.tektites.remove(tektite)
            
            if (tektite.health <= 0):
                app.tektites.remove(tektite)
                # Add 100 points since Link killed them 
                app.currentScore += 100
                app.hasKilledEnemy = True

        for stalfo in app.stalfos:
            if (stalfo.isJumping):
                stalfo.jump()
            if (stalfo.isFalling):
                stalfo.fall()
            
            if (stalfo.leftX < -64 or stalfo.leftX > 956 or stalfo.topY > 400):
                app.stalfos.remove(stalfo)
            
            if (stalfo.health <= 0):
                app.stalfos.remove(stalfo)
                # Add 100 points since Link killed them 
                app.currentScore += 100
                app.hasKilledEnemy = True

        # Deletes items if they are offscreen
        for item in app.items:
            if (item.leftX < -96 or item.leftX > 984):
                app.items.remove(item)

        # 10 steps is the buffer time for Link to take damage
        if (app.checkEnemyTimer >= 10):
            checkEnemyCollisions(app)

        
        # Generates new terrain on either side of Link
        generateWorld(app)

# Controls movements of Link
def onKeyPress(app, key):
    # Must press 'r' to get past start screen
    if (key == 'r' or key == 'R'):
        app.startScreen = False
    elif (key == 'd'):
        app.moveRight = True
    elif (key == 'a'):
        app.moveLeft = True
    elif (key == 'w' and app.link.isOnGround == True):
        app.link.isOnGround = False
        app.link.isJumping = True
    # Shoot arrows with 'p', app.arrowTimer makes sure that arrows aren't spammed
    elif (key == 'p' and app.arrowTimer > 10):
        app.arrowTimer = 0
        app.arrows.append(Arrow(app))
        if (app.link.lookingRight):
            app.link.image = app.link.bowRight
        else:
            app.link.image = app.link.bowLeft
    # Bomb can only be thrown if Link got it from an item block
    elif (key == 'o' and app.link.hasBomb):
        app.bombs.append(Bomb(app))
        # Once thrown, Link no longer has a bomb
        app.link.hasBomb = False
    elif (key == 'm'):
        app.link.moveSpeed = 16
    elif (key == 'j' and not app.link.isJumping):
        app.link.currVelocity = -30
        app.link.originalVelocity = -30

# Makes sure to stop moving Link left or right
def onKeyRelease(app, key):
    if (key == 'd'):
        app.moveRight = False
    elif (key == 'a'):
        app.moveLeft = False
    elif (key == 'p'):
        # Makes sure that Link is looking the right way
        if (app.link.lookingRight):
            app.link.image = app.link.walkRight
        else:
            app.link.image = app.link.walkLeft

# Generates new terrain depending on how much the background has shifted
def generateWorld(app):
    if (app.changeInBackground <= -32):
        generateRightCol(app)
        app.changeInBackground = 0
    elif (app.changeInBackground >= 32):
        generateLeftCol(app)
        app.changeInBackground = 0

# Checks to see if Link has collided with enemies
def checkEnemyCollisions(app):
    for enemy in app.enemies:
        if (abs(app.link.centerX - enemy.centerX) < app.link.width and
            abs(enemy.centerY - app.link.centerY) < app.link.height):
            app.link.health -= enemy.damage
            app.checkEnemyTimer = 0
        elif (abs(app.link.centerY - enemy.centerY) < app.link.height and
              abs(enemy.centerX - app.link.centerX) < app.link.width):
            app.link.health -= enemy.damage
            app.checkEnemyTimer = 0

############ DRAWING FUNCTIONS ##############
# Draws all blocks
def drawBlocks(app):
    for left, top, width, height in app.collisionBlocks:
        drawImage(CMUImage(app.brick), left, top)
    
    for left, top, width, height in app.itemBlocks:
        drawImage(CMUImage(app.itemBlock), left, top)

# Draws the start screen
def drawStartScreen(app):
    drawImage(CMUImage(app.startingScreenImage), 0, 0)

# Draws high screen that shows up on start screen
def drawHighScore(app):
    drawLabel(app.highScore, 675, 318, size=25, fill='black', align='left')

# Draws current score that will appear top-right when playing the game
def drawScore(app):
    drawLabel('Score:', 700, 15, size=25, fill='black')
    drawLabel(str(app.currentScore), 750, 16, size=25, fill='black', align='left')

# Draws arrows
def drawArrows(app):
    for arrow in app.arrows:
        drawImage(CMUImage(arrow.image), arrow.leftX, arrow.topY)

# Draws bombs
def drawBombs(app):
    if (len(app.bombs) > 0):
        bomb = app.bombs[0]
        drawImage(CMUImage(bomb.image), bomb.leftX, bomb.topY)

# Draws Link
def drawLink(app):
    drawImage(CMUImage(app.link.image), app.link.leftX, app.link.topY)

# Draws enemies
def drawEnemies(app):
    for tektite in app.tektites:
        drawImage(CMUImage(tektite.image), tektite.leftX, tektite.topY)
    
    for stalfo in app.stalfos:
        drawImage(CMUImage(stalfo.image), stalfo.leftX, stalfo.topY)

# Draws items on top of item blocks
def drawItems(app):
    for item in app.items:
        drawImage(CMUImage(item.image), item.leftX, item.topY)

# Draw hearts to represent Link's health in the top-left
def drawHealth(app):
    # From https://opengameart.org/content/heart-pixel-art
    heart = Image.open('Images/Heart.png')
    heart = heart.resize((30, 30))
    for i in range(app.link.health):
        drawImage(CMUImage(heart), i*50, 0)

##########################################

# Runs game
runApp(app.width, app.height)