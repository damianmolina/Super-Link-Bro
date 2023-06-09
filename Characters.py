from cmu_graphics import *
from PIL import Image
from RandomWorld import *
from Items import *
import random

class Link:
    def __init__(self, app):
        # Gets the walk and bow sprite from Link sprite sheet
        # From https://www.pngegg.com/en/png-zygrs
        linkSpriteSheet = Image.open('Images/LinkSpriteSheet.png')
        linkSpriteSheet = linkSpriteSheet.resize((268, 228))
        linkSpriteSheet = linkSpriteSheet.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.walk = linkSpriteSheet.crop((53, 0, 106, 50))
        self.walk = self.walk.resize((40, 40))
        self.walkRight = self.walk
        self.walkLeft = self.walkRight.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.bowRight = linkSpriteSheet.crop((80, 121, 133, 171))
        self.bowRight = self.bowRight.resize((40, 40))
        self.bowLeft = self.bowRight.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        # Sets current image of Link walking
        self.image = self.walk

        # The dimensions of Link's boundary box and his location
        self.width = 32
        self.height = 32
        self.leftX = app.width/2 - (self.width)/2
        self.topY = 0
        self.centerX = self.leftX + (self.width)/2
        self.centerY = self.topY + (self.height)/2

        # The direction that Link is looking
        self.lookingRight = True

        # Whether Link is jumping or not
        self.isJumping = False

        # Whether Link is on the ground or not
        self.isOnGround = False

        # Link starts off falling
        self.isFalling = True

        # Link's movement speed
        self.moveSpeed = 8
        self.originalVelocity = -25
        self.currVelocity = -25
        self.gravity = 2

        # Link's health
        self.health = 5

        self.hasBomb = False


    def move(self, app, dx, dy):
        # Flip Link's image if he's looking the wrong way
        self.flip(dx)

        # Checks if Link is actually standing on top of something
        self.checkGround()


        # Check if moving right and not colliding
        if (dx > 0 and not self.isCollisionX(app, dx)):
            # Moves everything in relation to Link
            moveEverything(app, -dx, dy)
            app.changeInBackground -= dx
            # If movement score hasn't reached its max, its fine to continue
            # adding points
            if (app.currentScore <= app.movementPointsLimit):
                app.currentScore += (abs(dx))//5
            # Otherwise, we need to make sure that the player has killed an enemy
            # before adding more movement points
            elif (app.hasKilledEnemy):
                app.hasKilledEnemy = False
                app.movementPointsLimit = app.currentScore + 300
        
        # Checks if moving left and not out of bounds and is not colliding
        if (dx < 0 and not self.isCollisionX(app, dx)):
            # Moves everything in relation to Link
            moveEverything(app, -dx, dy)
            app.changeInBackground -= dx
            # If movement score hasn't reached its max, its fine to continue
            # adding points
            if (app.currentScore <= app.movementPointsLimit):
                app.currentScore += (abs(dx))//5
            # Otherwise, we need to make sure that the player has killed an enemy
            # before adding more movement points
            elif (app.hasKilledEnemy):
                app.hasKilledEnemy = False
                app.movementPointsLimit = app.currentScore + 300
        
        # Checks collisions on Y-axis
        if (not self.isCollisionY(app, dy)):
            # Moves Link sprite
            self.topY += dy
            self.centerY += dy

    # Checks for any horizontal collisions
    def isCollisionX(self, app, dx):
        # Goes through each block
        for left, top, width, height in app.allBlocks:
            blockCenterY = top + height/2
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dx > 0 and self.leftX < left and self.leftX + self.width + 1 > left
                and abs(blockCenterY - self.centerY) < self.height):
                # Moves entire background and checks to make sure Link is still
                # on ground
                moveEverything(app, -(left - (self.leftX + self.width)), 0)
                app.changeInBackground -= (left - (self.leftX + self.width))
                self.checkGround()
                return True
            elif (dx < 0 and self.leftX > left and self.leftX - 1 < left + width 
                  and abs(blockCenterY - self.centerY) < self.height - 6):
                # Moves entire background and checks to make sure Link is still
                # on ground
                moveEverything(app, self.leftX - (left + width), 0)
                app.changeInBackground += self.leftX - (left + width)
                self.checkGround()
                return True
        return False
        
    # Checks for any vertical collisions
    def isCollisionY(self, app, dy):
        for left, top, width, height in app.collisionBlocks:
            blockCenterX = left + width/2
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dy > 0 and self.topY < top and self.topY + self.height + dy > top 
                and abs(blockCenterX - self.centerX) < self.width - 5
                or (self.topY + self.height + dy > app.lowestFloor and self.isFalling)):
                # An if-statement to determine whether Link is colliding with lowestFloor
                # or with a brick
                if (self.topY + self.height + dy > app.lowestFloor):
                    self.topY = app.lowestFloor - self.height
                    self.centerY = app.lowestFloor - (self.height)/2
                else:
                    self.topY = top - self.height
                    self.centerY = top - (self.height)/2
                # Link has to be standing on a ground
                self.isOnGround = True
                return True
        
        for i in range(len(app.itemBlocks)):
            left, top, width, height = app.itemBlocks[i]
            blockCenterX = left + width/2
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dy > 0 and self.topY < top and self.topY + self.height + dy > top 
                and abs(blockCenterX - self.centerX) < self.width - 10
                or (self.topY + self.height + dy > app.lowestFloor and self.isFalling)):
                # An if-statement to determine whether Link is colliding with floor
                # or with a item block
                if (self.topY + self.height + dy > app.lowestFloor):
                    self.topY = app.lowestFloor - self.height
                    self.centerY = app.lowestFloor - (self.height)/2
                else:
                    self.topY = top - self.height
                    self.centerY = top - (self.height)/2
                # Link has to be standing on a ground
                self.isOnGround = True
                return True
            elif (dy < 0 and self.topY >= top + height and self.topY + dy < top + height 
                  and abs(blockCenterX - self.centerX) < self.width - 10 and self.isJumping):
                self.topY = top + height - 5
                self.centerY = top + height + (self.height)/2 - 5
                # "Hitting" his head means that Link is no longer jumping but 
                # is instead falling
                self.isJumping = False
                self.isFalling = True
                # New item appears on top of item block
                item = Item(app, app.itemBlocks[i])
                # Makes sure that item is not already on top of block
                if (not findItem(item, app)):
                    # 0 --> bomb, 1 --> jump booost, 2 --> movement boost
                    if (item.item == 1):
                        self.currVelocity = -30
                        self.originalVelocity = -30
                    elif (item.item == 2):
                        self.moveSpeed = 16
                    else:
                        self.hasBomb = True
                    app.items.append(item)
                return True
            
        return False

    
    # Flips Link's image to look in correct direction
    def flip(self, dx):
        if (dx > 0):
            self.image = self.walkRight
            self.lookingRight = True
        elif (dx < 0):
            self.image = self.walkLeft
            self.lookingRight = False

    # Causes Link to jump
    def jump(self):
        self.isFalling = False
        self.move(app, 0, self.currVelocity + self.gravity)
        # Once velocity is at or above zero, Link starts falling
        if (self.currVelocity >= 0):
            self.isFalling = True
            self.isJumping = False
        else:
            self.currVelocity += 2

    # Checking whether Link is on a ground
    def checkGround(self):
        if (self.topY + self.height + 1 > app.lowestFloor): 
            self.isOnGround = True
        else:
            for left, top, width, _ in app.allBlocks:
                if (self.topY + self.height + 1 > top and left < self.centerX < left + width):
                    self.isOnGround = True
            self.isOnGround = False
    
    # Falling movement
    def fall(self):
        self.move(app, 0, self.gravity)
        if (self.isOnGround):
            self.gravity = 2
            self.currVelocity = self.originalVelocity
        else:
            if (self.gravity < 20):
                self.gravity += 2
        

class Tektite:
    def __init__(self, app):
        # Gets tektite sprite from https://displate.com/displate/1407487
        tektite = Image.open('Images/Tektite.png')
        tektite = tektite.resize((32, 32))
        self.image = tektite

        # Determines which side of the screen the tektite spawns
        probOfSide = random.random()
        if (probOfSide > 0.5):
            self.leftX = 928
        else:
            self.leftX = -64
        
        # Dimensions of tektite
        self.topY = 0
        self.width = self.height = 32
        self.centerX = self.leftX + (self.width)/2
        self.centerY = self.topY + (self.height)/2

        # Charcteristics of tektite
        self.isJumping = False
        self.isOnGround = False
        self.isFalling = True
        self.moveSpeed = 5

        # Tektite can jump for a longer period of time than Link
        self.originalVelocity = -25
        self.currVelocity = -25
        self.gravity = 1

        # Amount of damage that a Tektite can do
        self.damage = 1

        # Amount of health that a Tektite has
        self.health = 2
    
    # Detrmines where Link is in relation to Tektite, then moves towards Link
    def moveTowardLink(self, app, dx):
        self.checkGround()
        if (self.leftX > app.link.leftX and not self.isCollisionX(app, -dx)):
            self.leftX -= dx
            self.centerX -= dx
        elif (not self.isCollisionX(app, dx)):
            self.leftX += dx
            self.centerX += dx

    # Detrmines where Link is in relation to Tektite, then moves away from Link
    def moveAwayFromLink(self, app, dx):
        self.checkGround()
        if (self.leftX > app.link.leftX and not self.isCollisionX(app, dx)):
            self.leftX += dx
            self.centerX += dx
        elif (not self.isCollisionX(app, -dx)):
            self.leftX -= dx
            self.centerX -= dx
    
    def isCollisionX(self, app, dx):
        # Goes through each block
        for left, top, width, height in app.allBlocks:
            blockCenterY = top + height/2
            # Checks direction of movement, whether it will collide and whether Tektite's center
            # is in the right spot for a collision to occur
            if (dx > 0 and self.leftX < left and self.leftX + self.width + 1 > left
                and abs(blockCenterY - self.centerY) < self.height):
                self.leftX = left - self.width
                self.centerX = self.leftX + self.width/2
                return True
            elif (dx < 0 and self.leftX > left and self.leftX - 1 < left + width 
                  and abs(blockCenterY - self.centerY) < self.height):
                self.leftX = left + width
                self.centerX = self.leftX + self.width/2
                return True
        return False
    
    def isCollisionY(self, app, dy):
        for left, top, width, height in app.allBlocks:
            blockCenterX = left + width/2
            # Checks direction of movement, whether it will collide and whether Tektites's center
            # is in the right spot for a collision to occur
            if (dy > 0 and self.topY < top and self.topY + self.height + dy > top 
                and abs(blockCenterX - self.centerX) < self.width - 10
                or (self.topY + self.height + dy > app.lowestFloor)):
                # An if-statement to determine whether Tektite is colliding with floor
                # or with a block
                if (self.topY + self.height + dy > app.lowestFloor):
                    self.topY = app.lowestFloor - self.height
                    self.centerY = app.lowestFloor - (self.height)/2
                else:
                    self.topY = top - self.height
                    self.centerY = top - (self.height)/2
                # Tektite has to be standing on a ground
                self.isOnGround = True
                return True
            elif (dy < 0 and self.topY > top + height and self.topY + dy < top + height 
                  and abs(blockCenterX - self.centerX) < self.width - 1 and self.isJumping):
                self.topY = top + height
                self.centerY = top + height + (self.height)/2
                # "Hitting" his head means that Tektite is no longer jumping but 
                # is instead falling
                self.isJumping = False
                self.isFalling = True
                return True
        return False

    # Causes Tektite to jump
    def jump(self):
        self.isFalling = False
        if (not self.isCollisionY(app, self.currVelocity + self.gravity)):
            self.topY += self.currVelocity + self.gravity
            self.centerY += self.currVelocity + self.gravity
        # Once velocity is at or above zero, Tektite starts falling
        if (self.currVelocity >= 0):
            self.isFalling = True
            self.isJumping = False
        else:
            self.currVelocity += 2

    # Checking whether Link is on a ground
    def checkGround(self):
        if (self.topY + self.height + 1 > app.lowestFloor): 
            self.isOnGround = True
        else:
            for left, top, width, height in app.allBlocks:
                if (self.topY + self.height + 1 > top and left < self.centerX < left + width):
                    self.isOnGround = True
            self.isOnGround = False
    
    # Falling movement
    def fall(self):
        if (not self.isCollisionY(app, self.gravity)):
            self.topY += self.gravity
            self.centerY += self.gravity

        if (self.isOnGround):
            self.gravity = 1
            self.currVelocity = self.originalVelocity
        else:
            if (self.gravity < 20):
                self.gravity += 2

    # Tektites are equal to each other if they have the same x and y coordinates
    def __eq__(self, other):
        if (not isinstance(other, Tektite)): return False

        if (self.leftX == other.leftX and self.topY == other.topY):
            return True
        else:
            return False
    
class Stalfo:
    def __init__(self, app):
        # From https://www.deviantart.com/captainedwardteague/art/Original-The-Zelda-Stalfos-Sprite-858214933
        stalfo = Image.open('Images/Stalfo.png')
        stalfo = stalfo.resize((32, 32))
        self.image = stalfo

        # Determines which side of the screen the stalfo spawns
        probOfSide = random.random()
        if (probOfSide > 0.5):
            self.leftX = 928
        else:
            self.leftX = -64
        
        # Dimensions of stalfo
        self.topY = 0
        self.width = self.height = 32
        self.centerX = self.leftX + (self.width)/2
        self.centerY = self.topY + (self.height)/2

        # Charcteristics of stalfo
        self.isJumping = False
        self.isOnGround = False
        self.isFalling = True
        self.moveSpeed = 3

        # Stalfo has the same jumping speed as Link
        self.originalVelocity = -20
        self.currVelocity = -20
        self.gravity = 2

        # Amount of damage that a Stalfo can do
        self.damage = 1

        # Amount of health that a Stalfo has
        self.health = 2
    
    # Determines where Link is in relation to Stalfo, then moves towards Link
    def moveTowardLink(self, app, dx):
        self.checkGround()
        if (self.leftX > app.link.leftX and not self.isCollisionX(app, -dx)):
            self.leftX -= dx
            self.centerX -= dx
        elif (not self.isCollisionX(app, dx)):
            self.leftX += dx
            self.centerX += dx

    # Determines where Link is in relation to Stalfo, then moves away from Link
    def moveAwayFromLink(self, app, dx):
        self.checkGround()
        if (self.leftX > app.link.leftX and not self.isCollisionX(app, dx)):
            self.leftX += dx
            self.centerX += dx
        elif (not self.isCollisionX(app, -dx)):
            self.leftX -= dx
            self.centerX -= dx

    def isCollisionX(self, app, dx):
        # Goes through each block
        for left, top, width, height in app.allBlocks:
            blockCenterY = top + height/2
            # Checks direction of movement, whether it will collide and whether Stalfo's center
            # is in the right spot for a collision to occur
            if (dx > 0 and self.leftX < left and self.leftX + self.width + 1 > left
                and abs(blockCenterY - self.centerY) < self.height):
                self.leftX = left - self.width
                self.centerX = self.leftX + self.width/2
                return True
            elif (dx < 0 and self.leftX > left and self.leftX - 1 < left + width 
                  and abs(blockCenterY - self.centerY) < self.height):
                self.leftX = left + width
                self.centerX = self.leftX + self.width/2
                return True
        return False
    
    def isCollisionY(self, app, dy):
        for left, top, width, height in app.allBlocks:
            blockCenterX = left + width/2
            # Checks direction of movement, whether it will collide and whether Stalfo's center
            # is in the right spot for a collision to occur
            if (dy > 0 and self.topY < top and self.topY + self.height + dy > top 
                and abs(blockCenterX - self.centerX) < self.width - 10
                or (self.topY + self.height + dy > app.lowestFloor)):
                # An if-statement to determine whether Stalfo is colliding with floor
                # or with a block
                if (self.topY + self.height + dy > app.lowestFloor):
                    self.topY = app.lowestFloor - self.height
                    self.centerY = app.lowestFloor - (self.height)/2
                else:
                    self.topY = top - self.height
                    self.centerY = top - (self.height)/2
                # Stalfo has to be standing on a ground
                self.isOnGround = True
                return True
            elif (dy < 0 and self.topY > top + height and self.topY + dy < top + height 
                  and abs(blockCenterX - self.centerX) < self.width - 1 and self.isJumping):
                self.topY = top + height
                self.centerY = top + height + (self.height)/2
                # "Hitting" his head means that Stalfo is no longer jumping but 
                # is instead falling
                self.isJumping = False
                self.isFalling = True
                return True
        return False
    
    # Causes Stalfo to jump
    def jump(self):
        self.isFalling = False
        if (not self.isCollisionY(app, self.currVelocity + self.gravity)):
            self.topY += self.currVelocity + self.gravity
            self.centerY += self.currVelocity + self.gravity
        # Once velocity is at or above zero, Stalfo starts falling
        if (self.currVelocity >= 0):
            self.isFalling = True
            self.isJumping = False
        else:
            self.currVelocity += 2

    # Checking whether Link is on a ground
    def checkGround(self):
        if (self.topY + self.height + 1 > app.lowestFloor): 
            self.isOnGround = True
        else:
            for left, top, width, height in app.allBlocks:
                if (self.topY + self.height + 1 > top and left < self.centerX < left + width):
                    self.isOnGround = True
            self.isOnGround = False
    
    # Falling movement
    def fall(self):
        if (not self.isCollisionY(app, self.gravity)):
            self.topY += self.gravity
            self.centerY += self.gravity
        if (self.isOnGround):
            self.gravity = 1
            self.currVelocity = self.originalVelocity
        else:
            if (self.gravity < 20):
                self.gravity += 2

    # Stalfos are equal to each other if they have the same x and y coordinates
    def __eq__(self, other):
        if (not isinstance(other, Stalfo)): return False

        if (self.leftX == other.leftX and self.topY == other.topY):
            return True
        else:
            return False

# Helper function to determine whether item is already on top of item block
def findItem(o, app):
    for v in app.items:
        if (o == v):
            return True
    return False