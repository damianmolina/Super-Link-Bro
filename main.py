from cmu_graphics import *
from PIL import Image

def onAppStart(app):
    app.width = 896
    app.height = 448
    app.image = Image.open('Images/Mario 1-1.png')
    app.image = app.image.resize((app.image.width * 2, app.image.height * 2))
    app.image = CMUImage(app.image)


def redrawAll(app):
    drawImage(app.image, 0, 0)

runApp(app.width, app.height)