from cmu_graphics import *
from PIL import Image
from Characters import *

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
        self.leftX = app.width/2
        self.topY = app.link.topY
        self.width = self.height = 32
        self.centerX = self.leftX + (self.width)/2
        self.centerY = self.topY + (self.height)/2


        self.hasCollided = False

        self.damage = 1
    
    def shoot(self):
        # Moves arrow in the direction that Link was facing 
        if (self.lookingRight and not self.isCollisionX(app, self.arrowSpeed)):
            self.leftX += (self.arrowSpeed)
        elif (not self.lookingRight and not self.isCollisionX(app, -self.arrowSpeed)):
            self.leftX -= (self.arrowSpeed)

    
    # Checks for any horizontal collisions
    def isCollisionX(self, app, dx):
        for tektite in app.tektites:
            if (dx > 0 and self.leftX < tektite.leftX and self.leftX + self.width + 3 > tektite.leftX
                and abs(tektite.centerY - self.centerY) < self.height):
                self.hasCollided = True
                tektite.health -= self.damage
                return True
            elif (dx < 0 and self.leftX > tektite.leftX and self.leftX - 3 < tektite.leftX + tektite.width 
                  and abs(tektite.centerY - self.centerY) < self.height):
                self.hasCollided = True
                tektite.health -= self.damage
                return True
    
        # Goes through each block
        for left, top, width, height in app.allBlocks:
            blockCenterY = top + height/2
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dx > 0 and self.leftX < left and self.leftX + self.width + 1 > left
                and abs(blockCenterY - self.centerY) < self.height):
                self.hasCollided = True
                return True
            elif (dx < 0 and self.leftX > left and self.leftX - 1 < left + width 
                  and abs(blockCenterY - self.centerY) < self.height):
                self.hasCollided = True
                return True

        return False
    
        
    # Arrows are equal to each other when they're at the same location
    def __eq__(self, other):
        if (not isinstance(other, Arrow)): return False
        if (self.leftX == other.leftX and self.topY == other.topY):
            return True
        else:
            return False
        
    
class Bomb:
    velocityY = -10 
    gravity = 2
    def __init__(self, app):
        # From https://www.pinterest.com.mx/pin/345158758920841396/
        bomb = Image.open('Images/Bomb.png')
        bomb = bomb.resize((32, 32))

        # Determines the direction in which the bomb is pointing as well as velocity
        # in the x-direction
        if (app.link.lookingRight):
            self.velocityX = 15
        else:
            self.velocityX = -15
            bomb = bomb.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        
        self.image = bomb

        # Location of bomb
        self.leftX = app.width/2
        self.topY = app.link.topY
        self.width = self.height = 32
        self.centerX = self.leftX + (self.width)/2
        self.centerY = self.topY + (self.height)/2

        # Initially has not collided with anything
        self.hasCollided = False

        self.damage = 2

    # Bombs are equal to each other when they're at the same location
    def __eq__(self, other):
        if (not isinstance(other, Bomb)): return False

        if (self.leftX == other.leftX and self.topY == other.topY):
            return True
        else:
            return False

    
    def move(self, app):
        # Current change in y-direction
        dy = Bomb.velocityY + Bomb.gravity

        # Check for any collisions
        if (not self.isCollisionY(app, dy) and not self.isCollisionX(app, self.velocityX)):
            self.leftX += self.velocityX 
            self.centerX += self.velocityX 
            self.topY += dy
            self.centerY += dy
            Bomb.velocityY += 2
        else:
            # Reset bomb velocity 
            Bomb.velocityY = -10

    # Checks for any horizontal collisions
    def isCollisionX(self, app, dx):
        for tektite in app.tektites:
            if (dx > 0 and self.leftX < tektite.leftX and self.leftX + self.width + 10 > tektite.leftX
                and abs(tektite.centerY - self.centerY) < self.height - 10):
                self.hasCollided = True
                tektite.health -= self.damage
                return True
            elif (dx < 0 and self.leftX > tektite.leftX and self.leftX - 10 < tektite.leftX + tektite.width 
                  and abs(tektite.centerY - self.centerY) < self.height - 10):
                self.hasCollided = True
                tektite.health -= self.damage
                return True
        
         # Goes through each block
        for left, top, width, height in app.allBlocks:
            blockCenterY = top + height/2
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dx > 0 and self.leftX < left and self.leftX + self.width + 1 > left
                and abs(blockCenterY - self.centerY) < self.height):
                self.hasCollided = True
                return True
            elif (dx < 0 and self.leftX > left and self.leftX - 1 < left + width 
                  and abs(blockCenterY - self.centerY) < self.height):
                self.hasCollided = True
                return True
            
        return False

    # Checks for any vertical collisions
    def isCollisionY(self, app, dy):
        for tektite in app.tektites:
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dy > 0 and self.topY < tektite.topY and self.topY + self.height + 10 > tektite.topY 
                and abs(tektite.centerX - self.centerX) < self.width - 10):
                self.hasCollided = True
                tektite.health -= self.damage
                return True
            elif (dy < 0 and self.topY > tektite.topY  + tektite.height and self.topY - 10 < tektite.topY + tektite.height 
                  and abs(tektite.centerX - self.centerX) < self.width - 10):
                self.hasCollided = True
                tektite.health -= self.damage
                return True
            
        for left, top, width, height in app.allBlocks:
            blockCenterX = left + width/2
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dy > 0 and self.topY < top and self.topY + self.height + 1 > top 
                and abs(blockCenterX - self.centerX) < self.width - 5
                or (self.topY + self.height + 1 > app.lowestFloor)):
                self.hasCollided = True
                return True
            elif (dy < 0 and self.topY > top + height and self.topY + 1 < top + height 
                  and abs(blockCenterX - self.centerX) < self.width - 5):
                self.hasCollided = True
                return True
        
        return False
