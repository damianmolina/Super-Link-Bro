from cmu_graphics import *
from PIL import Image
from Characters import Link

def onAppStart(app):
    app.width = 896
    app.height = 448
    app.image = Image.open('Images/Mario 1-1.png')
    app.image = app.image.resize((app.image.width * 2, app.image.height * 2))
    app.image = CMUImage(app.image)
    app.link = Link()
    app.labelX = 0
    app.labelY = 0
    app.moveRight = False
    app.moveLeft = False
    app.jump = False


def redrawAll(app):
    drawImage(app.image, 0, 0)
    drawImage(CMUImage(app.link.image), app.link.leftX, app.link.topY)
    drawLabel( f'({app.labelX}, {app.labelY})', app.labelX, app.labelY)

def onMouseMove(app, mouseX, mouseY):
    app.labelX = mouseX
    app.labelY = mouseY

def onKeyPress(app, key):
    if (key == 'right'):
        app.moveRight = True
    elif (key == 'left'):
        app.moveLeft = True

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

runApp(app.width, app.height)