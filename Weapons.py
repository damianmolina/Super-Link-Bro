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

        # Speed of arrow
        self.arrowSpeed = 15

        # Location/dimensions of arrow
        self.leftX = app.link.centerX
        self.topY = app.link.topY
        self.width = self.height = 32
        self.centerX = self.leftX + (self.width)/2
        self.centerY = self.topY + (self.height)/2

        # Arrow does not start off as collided with somethine
        self.hasCollided = False

        # Arrow does 1 damage once it has hit an enemy
        self.damage = 1
    
    # Moves arrow in the x-direction of whichever way that Link is facing
    def shoot(self):
        if (self.lookingRight and not self.isCollisionX(app, self.arrowSpeed)):
            self.leftX += (self.arrowSpeed)
        elif (not self.lookingRight and not self.isCollisionX(app, -self.arrowSpeed)):
            self.leftX -= (self.arrowSpeed)

    
    # Checks for any horizontal collisions (similar to Link's collision)
    def isCollisionX(self, app, dx):
        # Goes through all tektites
        for enemy in app.enemies:
            if (dx > 0 and self.leftX < enemy.leftX and self.leftX + self.width + 3 > enemy.leftX
                and abs(enemy.centerY - self.centerY) < self.height):
                self.hasCollided = True
                # Take away health from tektite
                enemy.health -= self.damage
                return True
            elif (dx < 0 and self.leftX > enemy.leftX and self.leftX - 3 < enemy.leftX + enemy.width 
                  and abs(enemy.centerY - self.centerY) < self.height):
                self.hasCollided = True
                # Take away health from tektite
                enemy.health -= self.damage
                return True

        # Goes through all blocks
        for left, top, width, height in app.allBlocks:
            blockCenterY = top + height/2
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

        # Vertical movements
        self.velocityY = -10 
        self.gravity = 2

        # Location of bomb
        self.leftX = app.width/2
        self.topY = app.link.topY
        self.width = self.height = 32
        self.centerX = self.leftX + (self.width)/2
        self.centerY = self.topY + (self.height)/2

        # Initially has not collided with anything
        self.hasCollided = False

        # Damage that it can do to enemies
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
        dy = self.velocityY + self.gravity

        # Check for any collisions and move the bomb
        if (not self.isCollisionY(app, dy) and not self.isCollisionX(app, self.velocityX)):
            self.leftX += self.velocityX 
            self.centerX += self.velocityX 
            self.topY += dy
            self.centerY += dy
            self.velocityY += 2
        else:
            # Reset bomb velocity 
            self.velocityY = -10

    # Checks for any horizontal collisions
    def isCollisionX(self, app, dx):
        # Goes through all enemies
        for enemy in app.enemies:
            if (dx > 0 and self.leftX < enemy.leftX and self.leftX + self.width + 10 > enemy.leftX
                and abs(enemy.centerY - self.centerY) < self.height - 10):
                self.hasCollided = True
                # Take away health from enemy
                enemy.health -= self.damage
                return True
            elif (dx < 0 and self.leftX > enemy.leftX and self.leftX - 10 < enemy.leftX + enemy.width 
                  and abs(enemy.centerY - self.centerY) < self.height - 10):
                self.hasCollided = True
                # Take away health from enemy
                enemy.health -= self.damage
                return True
        
         # Goes through each block
        for left, top, width, height in app.allBlocks:
            blockCenterY = top + height/2
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
        # Goes through all enemies
        for enemy in app.enemies:
            if (dy > 0 and self.topY < enemy.topY and self.topY + self.height + 10 > enemy.topY 
                and abs(enemy.centerX - self.centerX) < self.width - 10):
                self.hasCollided = True
                # Take away health from enemy
                enemy.health -= self.damage
                return True
            elif (dy < 0 and self.topY > enemy.topY  + enemy.height and self.topY - 10 < enemy.topY + enemy.height 
                  and abs(enemy.centerX - self.centerX) < self.width - 10):
                self.hasCollided = True
                # Take away health from enemy
                enemy.health -= self.damage
                return True
        
        # Goes through each block
        for left, top, width, height in app.allBlocks:
            blockCenterX = left + width/2
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
