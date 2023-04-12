from cmu_graphics import *
from PIL import Image

class Link:
    velocity = 9
    mass = 1

    def __init__(self):
        linkSpriteSheet = Image.open('Images/LinkSpriteSheet.png')
        linkSpriteSheet = linkSpriteSheet.resize((268, 228))
        linkSpriteSheet = linkSpriteSheet.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.walk = linkSpriteSheet.crop((53, 0, 106, 50))
        self.bow = linkSpriteSheet.crop((80, 121, 133, 171))
        self.image = self.walk
        self.leftX = 0
        self.topY = 358
        self.linkWidth = 50
        self.linkHeight = 45
        self.lookingRight = True
        self.isJumping = False
        self.moveSpeed = 75

    def move(self, app, dx, dy):
        self.flip(dx)
        if (dx > 0 and self.leftX + self.linkWidth < app.levelLeft + app.levelWidth):
            if (self.leftX + self.linkWidth >= app.width//2 and app.levelLeft > -(app.levelWidth)):
                app.levelLeft -= dx
            else:
                self.leftX += dx

        elif (dx < 0 and self.leftX > app.levelLeft):
            if (self.leftX - self.linkWidth <= app.width//2 and app.levelLeft < 0):
                app.levelLeft -= dx
            else:
                self.leftX += dx
    
        self.topY += dy
    
    def flip(self, dx):
        if (dx > 0 and not self.lookingRight):
            self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            self.lookingRight = True
        elif (dx < 0 and self.lookingRight):
            self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            self.lookingRight = False

    
    def jump(self):
        force = 0.5 * Link.mass * (Link.velocity**2)
        self.topY -= force
        Link.velocity = Link.velocity - 1

        if Link.velocity < 0:
            Link.mass = -1
        
        if (Link.velocity == -10):
            self.isJumping = False
            Link.velocity = 9
            Link.mass = 1



    
        



        