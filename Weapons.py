from cmu_graphics import *
from PIL import Image
from Characters import *
from FirstLevel import *

class Arrow:
    def __init__(self, app):
        # From https://www.reddit.com/r/PixelArt/comments/ldd4fb/arrow_first_animated_work_outside_of_minecraft/
        arrow = Image.open('Images/Arrow.png')
        arrow = arrow.resize((32, 32))

        # Determines the direction in which the arrow is pointing
        if (app.link.lookingRight):
            self.lookingRight = True
        else:
            self.lookingRight = False
            arrow = arrow.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        self.image = arrow

        self.arrowSpeed = 15

        # Location of arrow
        self.arrowLeftX = app.width/2
        self.arrowTopY = app.link.topY
        self.arrowWidth = self.arrowHeight = 32
        self.arrowCenterX = self.arrowLeftX + (self.arrowWidth)/2
        self.arrowCenterY = self.arrowTopY + (self.arrowHeight)/2

        # Link's distance from beginning of level which will be used for later offsets
        self.linkDistanceFromLevel = app.link.leftX - app.levelLeft

        self.hasCollided = False
    
    def shoot(self):
        # This is the amount that Link has moved since shooting the arrow
        offset = (app.link.leftX - app.levelLeft) - self.linkDistanceFromLevel
        self.linkDistanceFromLevel = app.link.leftX - app.levelLeft

        # Moves arrow in the direction that Link was facing 
        if (self.lookingRight and not self.isCollisionX(app, self.arrowSpeed)):
            self.arrowLeftX += (self.arrowSpeed - offset)
        elif (not self.lookingRight and not self.isCollisionX(app, -self.arrowSpeed)):
            self.arrowLeftX -= (self.arrowSpeed + offset)

    
    # Checks for any horizontal collisions
    def isCollisionX(self, app, dx):
        # Goes through each block
        for left, top, width, height in app.collisionBlocks:
            blockCenterY = top + height/2
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dx > 0 and self.arrowLeftX < left and self.arrowLeftX + self.arrowWidth + 1 > left
                and abs(blockCenterY - self.arrowCenterY) < self.arrowHeight):
                self.hasCollided = True
                return True
            elif (dx < 0 and self.arrowLeftX > left and self.arrowLeftX - 1 < left + width 
                  and abs(blockCenterY - self.arrowCenterY) < self.arrowHeight):
                self.hasCollided = True
                return True
        return False
    
    # # Checks for any horizontal collisions
    # def isCollisionX(self, app, dx):
    #      # Goes through each block
    #     for left, top, width, height in app.collisionBlocks:
    #         # Checks direction of movement, whether it will collide and whether 
    #         # the bomb's center is in the right spot for a collision to occur
    #         if (dx > 0 and self.arrowLeftX < left and self.arrowLeftX + self.arrowWidth + 1 > left 
    #             and top < self.arrowCenterY < top + height
    #             or self.arrowLeftX > app.width):
    #             self.hasCollided = True
    #             return True
    #         elif (dx < 0 and self.arrowLeftX > left and self.arrowLeftX - 1 < left + width 
    #               and top < self.arrowCenterY < top + height
    #               or self.arrowLeftX + self.arrowWidth < 0):
    #             self.hasCollided = True
    #             return True
    #     return False
        
    # Arrows are equal to each other when they're at the same location
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

        # Determines the direction in which the bomb is pointing as well as velocity
        # in the x-direction
        if (app.link.lookingRight):
            self.velocityX = 10
        else:
            self.velocityX = -10
            bomb = bomb.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        
        self.image = bomb

        # Location of bomb
        self.bombLeftX = app.width/2
        self.bombTopY = app.link.topY
        self.bombWidth = self.bombHeight = 40
        self.bombCenterX = self.bombLeftX + (self.bombWidth)/2
        self.bombCenterY = self.bombTopY + (self.bombHeight)/2

        # Initially has not collided with anything
        self.hasCollided = False

        # Link's distance from beginning of level which will be used for later offsets
        self.linkDistanceFromLevel = app.link.leftX - app.levelLeft

    # Bombs are equal to each other when they're at the same location
    def __eq__(self, other):
        if (not isinstance(other, Bomb)): return False

        if (self.bombLeftX == other.bombLeftX and self.bombTopY == other.bombTopY):
            return True
        else:
            return False

    
    def move(self, app):
        # Current change in y-direction
        dy = Bomb.velocityY + Bomb.gravity

        # This is the amount that Link has moved since throwing the bomb
        offset = (app.link.leftX - app.levelLeft) - self.linkDistanceFromLevel
        self.linkDistanceFromLevel = app.link.leftX - app.levelLeft

        # Check for any collisions
        if (not self.isCollisionY(app, dy) and not self.isCollisionX(app, self.velocityX)):
            self.bombLeftX += (self.velocityX - offset)
            self.bombCenterX += (self.velocityX - offset)
            self.bombTopY += dy
            self.bombCenterY += dy
            Bomb.velocityY += 2
        else:
            # Reset bomb velocity 
            Bomb.velocityY = -10

    # Checks for any horizontal collisions
    def isCollisionX(self, app, dx):
         # Goes through each block
        for left, top, width, height in app.collisionBlocks:
            # Checks direction of movement, whether it will collide and whether 
            # the bomb's center is in the right spot for a collision to occur
            if (dx > 0 and self.bombLeftX < left and self.bombLeftX + self.bombWidth + 1 > left 
                and top < self.bombCenterY < top + height):
                self.hasCollided = True
                return True
            elif (dx < 0 and self.bombLeftX > left and self.bombLeftX - 1 < left + width 
                  and top < self.bombCenterY < top + height):
                self.hasCollided = True
                return True
        return False

    # Checks for any vertical collisions
    def isCollisionY(self, app, dy):
         # Goes through each block
        for left, top, width, height in app.collisionBlocks:
            # Checks direction of movement, whether it will collide and whether 
            # the bomb's center is in the right spot for a collision to occur
            if (dy > 0 and self.bombTopY < top and self.bombTopY + self.bombHeight + 1 > top and left < self.bombCenterX < left + width
                or self.bombTopY + self.bombHeight + 1 > app.lowestFloor):
                self.hasCollided = True
                return True
            elif (dy < 0 and self.bombTopY > top + height and self.bombTopY + 1 < top + height and left < self.bombCenterX < left + width):
                self.hasCollided = True
                return True
        return False
    
