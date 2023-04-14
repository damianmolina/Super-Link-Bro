from cmu_graphics import *
from PIL import Image
from Characters import *
from FirstLevel import *

class Arrow:
    def __init__(self, app):
        # From https://www.reddit.com/r/PixelArt/comments/ldd4fb/arrow_first_animated_work_outside_of_minecraft/
        arrow = Image.open('Images/Arrow.png')
        arrow = arrow.resize((40, 40))

        if (app.link.lookingRight):
            self.lookingRight = True
        else:
            self.lookingRight = False
            arrow = arrow.transpose(Image.FLIP_LEFT_RIGHT)
        
        self.image = arrow

        self.arrowLeftX = app.link.leftX
        self.arrowTopY = app.link.topY
        self.arrowCenterX = app.link.centerX
        self.arrowCenterY = app.link.centerY
    
    def shoot(self):
        if (self.lookingRight):
            self.arrowCenterX += 10
            self.arrowLeftX += 10
        else:
            self.arrowCenterX -= 10
            self.arrowLeftX -= 10
        
    def __eq__(self, other):
        if (not isinstance(other, Arrow)): return False

        if (self.arrowCenterX == other.arrowCenterX and self.arrowCenterY == other.arrowCenterY):
            return True
        else:
            return False
        
    
