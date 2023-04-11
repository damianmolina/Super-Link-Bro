from cmu_graphics import *
from PIL import Image
from Characters import *
from FirstLevel import *

def onAppStart(app):
    app.width = 896
    app.height = 448
    app.firstLevel = Image.open('Images/Mario 1-1.png')
    app.firstLevel = app.firstLevel.resize((app.firstLevel.width * 2, app.firstLevel.height * 2))
    app.link = Link()
    app.labelX = 0
    app.labelY = 0
    app.moveRight = False
    app.moveLeft = False


def redrawAll(app):
    drawFirstLevel(app)
    drawImage(CMUImage(app.link.image), app.link.leftX, app.link.topY)
    drawLabel(f'({app.labelX}, {app.labelY})', app.labelX, app.labelY)


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
        app.link.move(1)
    elif (app.moveLeft):
        app.link.move(-1)
    elif (app.link.isJumping):
        app.link.jump()

runApp(app.width, app.height)