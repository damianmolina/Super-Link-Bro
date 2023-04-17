from cmu_graphics import *
from PIL import Image
from FirstLevel import *

class Link:
    velocity = -25
    gravity = 2

    def __init__(self, app):
        # Gets the walk and bow sprite from Link sprite sheet
        # From https://www.pngegg.com/en/png-zygrs
        linkSpriteSheet = Image.open('Images/LinkSpriteSheet.png')
        linkSpriteSheet = linkSpriteSheet.resize((268, 228))
        linkSpriteSheet = linkSpriteSheet.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.walk = linkSpriteSheet.crop((53, 0, 106, 50))
        self.bow = linkSpriteSheet.crop((80, 121, 133, 171))

        # Sets current image of Link walking
        self.image = self.walk

        # The dimensions of Link's boundary box
        self.leftX = app.width/2 - 25
        self.topY = 358
        self.linkWidth = 50
        self.linkHeight = 45
        self.centerX = self.leftX + (self.linkWidth)/2
        self.centerY = self.topY + (self.linkHeight)/2

        # The direction that Link is looking
        self.lookingRight = True

        # Whether Link is jumping or not
        self.isJumping = False

        # Whether Link is on the ground or not
        self.isOnGround = True

        self.isFalling = False

        # Link's movement speed
        self.moveSpeed = 10


    def move(self, app, dx, dy):
        # Flip Link's image if he's looking the wrong way
        self.flip(dx)

        # Checks if Link is actually standing on top of something
        self.checkGround()

        # Check if moving right and not colliding
        if (dx > 0 and not self.isCollisionX(app, dx)):
            moveBlocks(app, -dx, dy)
            app.levelLeft -= dx
        
        # Checks if moving left and not out of bounds and is not colliding
        elif (dx < 0 and not self.isCollisionX(app, dx) and not app.levelLeft >= 0):
            moveBlocks(app, -dx, dy)
            app.levelLeft -= dx
        
        # Checks collisions on Y-axis
        if (not self.isCollisionY(app, dy)):
            # Moves Link sprite
            self.topY += dy
            self.centerY += dy

    
    # Checks for any horizontal collisions
    def isCollisionX(self, app, dx):
        # Goes through each block
        for left, top, width, height in app.collisionBlocks:
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dx > 0 and self.leftX < left and self.leftX + self.linkWidth + dx > left 
                and top < self.centerY < top + height):
                moveBlocks(app, -(left - (self.leftX + self.linkWidth)), 0)
                app.levelLeft -= (left - (self.leftX + self.linkWidth))
                return True
            elif (dx < 0 and self.leftX > left and self.leftX - dx < left + width 
                  and top < self.centerY < top + height):
                moveBlocks(app, self.leftX - (left + width), 0)
                app.levelLeft += self.leftX - (left + width)
                return True
        return False

    # Checks for any vertical collisions
    def isCollisionY(self, app, dy):
        for left, top, width, height in app.collisionBlocks:
            # Checks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dy > 0 and self.topY < top and self.topY + self.linkHeight + dy > top 
                and left < self.centerX < left + width
                or self.topY + self.linkHeight + dy > app.lowestFloor):
                # An if-statement to determine whether Link is colliding with floor
                # or with a block
                if (self.topY + self.linkHeight + dy > app.lowestFloor):
                    self.topY = app.lowestFloor - self.linkHeight
                    self.centerY = app.lowestFloor - (self.linkHeight)/2
                else:
                    self.topY = top - self.linkHeight
                    self.centerY = top - (self.linkHeight)/2
                # Link has to be standing on a ground
                self.isOnGround = True
                return True
            elif (dy < 0 and self.topY > top + height and self.topY + dy < top + height 
                  and left < self.centerX < left + width and self.isJumping):
                self.topY = top + height
                self.centerY = top + height + (self.linkHeight)/2
                # "Hitting" his head means that Link is no longer jumping but 
                # is instead falling
                self.isJumping = False
                self.isFalling = True
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
        self.move(app, 0, Link.velocity + Link.gravity)
        if (Link.velocity >= 0):
            self.isFalling = True
            self.isJumping = False
        else:
            Link.velocity += 2

    # Checking whether Link is on a ground
    def checkGround(self):
        if (self.topY + self.linkHeight + 1 > app.lowestFloor): 
            self.isOnGround = True
        else:
            for left, top, width, height in app.collisionBlocks:
                if (self.topY + self.linkHeight + 1 > top and left < self.centerX < left + width):
                    self.isOnGround = True
            self.isOnGround = False
    
    # Falling movement
    def fall(self):
        self.move(app, 0, Link.gravity)
        if (self.isOnGround):
            Link.gravity = 2
            Link.velocity = -25
        else:
            Link.gravity += 2

class Tektite:
    def __init__(self, app):
        # From https://www.pixilart.com/art/tektite-sprite-3dae6d7691bf058
        tektite = Image.open('Images/Tektite.png')
        tektite = tektite.resize((150, 150))
        self.image = tektite

class Stalfo:
    def __init__(self, app):
        # From https://www.deviantart.com/captainedwardteague/art/Original-The-Zelda-Stalfos-Sprite-858214933
        stalfo = Image.open('Images/Stalfo.png')
        stalfo = stalfo.resize((50, 50))
        self.image = stalfo