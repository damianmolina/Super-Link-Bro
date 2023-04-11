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
        self.bow = linkSpriteSheet.crop((65, 121, 130, 165))
        self.image = self.walk
        self.lookingRight = True
        self.leftX = 0
        self.topY = 355
        self.isJumping = False

    def move(self, dir):
        if (dir > 0):
            if (not self.lookingRight):
                self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                self.lookingRight = True
            self.leftX += 3
        else:
            if (self.lookingRight):
                self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                self.lookingRight = False
            self.leftX -= 3
    
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



    
        



        