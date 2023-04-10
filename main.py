from cmu_graphics import *
from PIL import Image

def onAppStart(app):
    app.image = Image.open('Mario 1-1.png')
    app.image = CMUImage(app.image)


def redrawAll(app):
    drawImage(app.image, 0, 0)

runApp(width = 448, height = 224)