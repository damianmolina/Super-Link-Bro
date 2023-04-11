from cmu_graphics import *
from PIL import Image

class Link:
    def __init__(self):
        linkSpriteSheet = Image.open('Images/LinkSpriteSheet.png')
        linkSpriteSheet = linkSpriteSheet.resize((268, 228))
        linkSpriteSheet = linkSpriteSheet.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.walk = linkSpriteSheet.crop((53, 0, 106, 50))
        self.bow = linkSpriteSheet.crop((65, 121, 130, 165))
        self.image = self.walk
        self.leftX = 0
        self.topY = 355

    def move(self, dir):
        if (dir > 0):
            self.leftX += 3
        else:
            self.leftX -= 3
    
        



        