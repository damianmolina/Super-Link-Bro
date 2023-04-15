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
            arrow = arrow.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        
        self.image = arrow

        self.arrowLeftX = app.width/2
        self.arrowTopY = app.link.topY
    
    def shoot(self):
        if (self.lookingRight):
            self.arrowLeftX += 10
        else:
            self.arrowLeftX -= 10
        
    def __eq__(self, other):
        if (not isinstance(other, Arrow)): return False
        if (self.arrowLeftX == other.arrowLeftX and self.arrowTopY == other.arrowTopY):
            return True
        else:
            return False
    
class Bomb:
    velocityY = -10 
    gravity = 2
    def __init__(self, app):
        # From https://www.pinterest.com.mx/pin/345158758920841396/
        bomb = Image.open('Images/Bomb.png')
        bomb = bomb.resize((40, 40))

        if (app.link.lookingRight):
            self.velocityX = 10
        else:
            self.velocityX = -10
            bomb = bomb.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        
        self.image = bomb
        self.bombLeftX = app.width/2
        self.bombTopY = app.link.topY
        self.bombWidth = self.bombHeight = 40
        self.bombCenterX = self.bombLeftX + (self.bombWidth)/2
        self.bombCenterY = self.bombTopY + (self.bombHeight)/2
        self.hasCollided = False

    def __eq__(self, other):
        if (not isinstance(other, Bomb)): return False

        if (self.bombLeftX == other.bombLeftX and self.bombTopY == other.bombTopY):
            return True
        else:
            return False

    
    def move(self, app):
        dy = Bomb.velocityY + Bomb.gravity
        if (not self.isCollisionY(app, dy) and not self.isCollisionX(app, self.velocityX)):
            self.bombLeftX += self.velocityX
            self.bombCenterX += self.velocityX

            self.bombTopY += dy
            self.bombCenterY += dy
            Bomb.velocityY += 2
        else:
            Bomb.velocityY = -10

    
    def isCollisionX(self, app, dx):
         # Goes through each block
        for left, top, width, height in app.collisionBlocks:
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dx > 0 and self.bombLeftX < left and self.bombLeftX + self.bombWidth + 1 > left and top < self.bombCenterY < top + height):
                self.hasCollided = True
                return True
            elif (dx < 0 and self.bombLeftX > left and self.bombLeftX - 1 < left + width and top < self.bombCenterY < top + height):
                self.hasCollided = True
                return True
        return False

    def isCollisionY(self, app, dy):
        for left, top, width, height in app.collisionBlocks:
            if (dy > 0 and self.bombTopY < top and self.bombTopY + self.bombHeight + 1 > top and left < self.bombCenterX < left + width
                or self.bombTopY + self.bombHeight + 1 > app.lowestFloor):
                self.hasCollided = True
                return True
            elif (dy < 0 and self.bombTopY > top + height and self.bombTopY + 1 < top + height and left < self.bombCenterX < left + width):
                self.hasCollided = True
                return True
        return False
    
