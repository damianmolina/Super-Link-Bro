from cmu_graphics import *
from PIL import Image
from RandomWorld import *
from Items import *
import random

class Link:
    originalVelocity = -25
    currVelocity = -25
    gravity = 2

    def __init__(self, app):
        # Gets the walk and bow sprite from Link sprite sheet
        # From https://www.pngegg.com/en/png-zygrs
        linkSpriteSheet = Image.open('Images/LinkSpriteSheet.png')
        linkSpriteSheet = linkSpriteSheet.resize((268, 228))
        linkSpriteSheet = linkSpriteSheet.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.walk = linkSpriteSheet.crop((53, 0, 106, 50))
        self.walk = self.walk.resize((40, 40))
        self.bow = linkSpriteSheet.crop((80, 121, 133, 171))

        # Sets current image of Link walking
        self.image = self.walk

        # The dimensions of Link's boundary box
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

        self.isFalling = True

        # Link's movement speed
        self.moveSpeed = 8


    def move(self, app, dx, dy):
        # Flip Link's image if he's looking the wrong way
        self.flip(dx)

        # Checks if Link is actually standing on top of something
        self.checkGround()


        # Check if moving right and not colliding
        if (dx > 0 and not self.isCollisionX(app, dx)):
            moveEverything(app, -dx, dy)
            app.changeInBackground -= dx
        
        # Checks if moving left and not out of bounds and is not colliding
        if (dx < 0 and not self.isCollisionX(app, dx)):
            moveEverything(app, -dx, dy)
            app.changeInBackground -= dx
        
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
                and abs(blockCenterY - self.centerY) < self.height - 6):
                moveEverything(app, -(left - (self.leftX + self.width)), 0)
                app.changeInBackground -= (left - (self.leftX + self.width))
                self.checkGround()
                return True
            elif (dx < 0 and self.leftX > left and self.leftX - 1 < left + width 
                  and abs(blockCenterY - self.centerY) < self.height - 6):
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
                and abs(blockCenterX - self.centerX) < self.width - 10
                or (self.topY + self.height + dy > app.lowestFloor and self.isFalling)):
                # An if-statement to determine whether Link is colliding with floor
                # or with a block
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
                # or with a block
                if (self.topY + self.height + dy > app.lowestFloor):
                    self.topY = app.lowestFloor - self.height
                    self.centerY = app.lowestFloor - (self.height)/2
                else:
                    self.topY = top - self.height
                    self.centerY = top - (self.height)/2
                # Link has to be standing on a ground
                self.isOnGround = True
                return True
            elif (dy < 0 and self.topY > top + height and self.topY - 10 < top + height 
                  and abs(blockCenterX - self.centerX) < self.width and self.isJumping):
                self.topY = top + height
                self.centerY = top + height + (self.height)/2
                # "Hitting" his head means that Link is no longer jumping but 
                # is instead falling
                self.isJumping = False
                self.isFalling = True
                app.items.append(Item(app, app.itemBlocks[i]))
                
                return True
        return False

    

    # Flips Link's image if he's not looking in the correct direction
    def flip(self, dx):
        if (dx > 0 and not self.lookingRight):
            self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            self.lookingRight = True
        elif (dx < 0 and self.lookingRight):
            self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            self.lookingRight = False

    # Causes Link to jump
    def jump(self):
        self.isFalling = False
        self.move(app, 0, Link.currVelocity + Link.gravity)
        if (Link.currVelocity >= 0):
            self.isFalling = True
            self.isJumping = False
        else:
            Link.currVelocity += 2

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
        self.move(app, 0, Link.gravity)
        if (self.isOnGround):
            Link.gravity = 2
            Link.currVelocity = Link.originalVelocity
        else:
            Link.gravity += 2
        

class Tektite:

    def __init__(self, app):
        # From https://displate.com/displate/1407487
        tektite = Image.open('Images/Tektite.png')
        tektite = tektite.resize((32, 32))
        self.image = tektite
        probOfSide = random.random()
        if (probOfSide > 0.5):
            self.leftX = 928
        else:
            self.leftX = -64
        
        self.topY = 0
        self.width = self.height = 32
        self.centerX = self.leftX + (self.width)/2
        self.centerY = self.topY + (self.height)/2

        self.isJumping = False
        self.isOnGround = False
        self.isFalling = True
        self.moveSpeed = 5

        self.originalVelocity = -25
        self.currVelocity = -25
        self.gravity = 1

        self.health = 2
    
    def moveTowardLink(self, app, dx):
        self.checkGround()
        if (self.leftX > app.link.leftX and not self.isCollisionX(app, -dx)):
            self.leftX -= dx
            self.centerX -= dx
        elif (not self.isCollisionX(app, dx)):
            self.leftX += dx
            self.centerX += dx

    def moveAwayFromLink(self, app, dx):
        self.checkGround()
        if (self.leftX > app.link.leftX and not self.isCollisionX(app, dx)):
            self.leftX += dx
            self.centerX += dx
        elif (not self.isCollisionX(app, -dx)):
            self.leftX -= dx
            self.centerX -= dx
    
       # Causes Link to jump
    def jump(self):
        self.isFalling = False
        if (not self.isCollisionY(app, self.currVelocity + self.gravity)):
            self.topY += self.currVelocity + self.gravity
            self.centerY += self.currVelocity + self.gravity

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
            self.gravity += 2

    def isCollisionX(self, app, dx):
        # Goes through each block
        for left, top, width, height in app.allBlocks:
            blockCenterY = top + height/2
            # Checks direction of movement, whether it will collide and whether Link's center
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
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dy > 0 and self.topY < top and self.topY + self.height + dy > top 
                and abs(blockCenterX - self.centerX) < self.width - 10
                or (self.topY + self.height + dy > app.lowestFloor and self.isFalling)):
                # An if-statement to determine whether Link is colliding with floor
                # or with a block
                if (self.topY + self.height + dy > app.lowestFloor):
                    self.topY = app.lowestFloor - self.height
                    self.centerY = app.lowestFloor - (self.height)/2
                else:
                    self.topY = top - self.height
                    self.centerY = top - (self.height)/2
                # Link has to be standing on a ground
                self.isOnGround = True
                return True
            elif (dy < 0 and self.topY > top + height and self.topY + dy < top + height 
                  and abs(blockCenterX - self.centerX) < self.width - 1 and self.isJumping):
                self.topY = top + height
                self.centerY = top + height + (self.height)/2
                # "Hitting" his head means that Link is no longer jumping but 
                # is instead falling
                self.isJumping = False
                self.isFalling = True
                return True
        return False


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

        probOfSide = random.random()
        if (probOfSide > 0.5):
            self.stalfoLeftX = 928
        else:
            self.stalfoLeftX = -64
        
        self.stalfoTopY = 0