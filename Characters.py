from cmu_graphics import *
from PIL import Image
from FirstLevel import *

class Link:
    velocity = 20
    gravity = -2

    def __init__(self):
        # Gets the walk and bow sprite from Link sprite sheet
        linkSpriteSheet = Image.open('Images/LinkSpriteSheet.png')
        linkSpriteSheet = linkSpriteSheet.resize((268, 228))
        linkSpriteSheet = linkSpriteSheet.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.walk = linkSpriteSheet.crop((53, 0, 106, 50))
        self.bow = linkSpriteSheet.crop((80, 121, 133, 171))

        # Sets current image of Link walking
        self.image = self.walk

        # The dimensions of Link's boundary box
        self.leftX = 0
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

        # Link's movement speed
        self.moveSpeed = 10

    def move(self, app, dx, dy):
        # Flip Link's image if he's looking the wrong way
        self.flip(dx)

        # Check if moving right and not colliding
        if (dx > 0 and not self.isCollisionX(app, dx)):
            # Checks if Link is past the middle of the screen (towards right)
            if (self.leftX + self.linkWidth >= app.width/2):
                # Moves background image and blocks
                moveBlocks(app, -dx, dy)
                app.levelLeft -= dx
            else:
                # Moves Link sprite
                self.leftX += dx
                self.centerX += dx
        
        # Checks if moving left and not out of bounds and is not colliding
        elif (dx < 0 and self.leftX > app.levelLeft and not self.isCollisionX(app, dx)):
             # Checks if Link is past the middle of the screen (towards left) and 
             # if Link is at the beginning of the level
            if (self.leftX - self.linkWidth <= app.width/2 and app.levelLeft < 0):
                # Moves background image and blocks
                moveBlocks(app, -dx, dy)
                app.levelLeft -= dx
            else:
                # Moves Link sprite
                self.leftX += dx
                self.centerX += dx
        
        # Checks collisions on Y-axis
        if (not self.isCollisionY(app, dy)):
            # Moves Link sprite
            self.topY += dy
            self.centerY += dy

    
    # Checks for any horizontal collisions
    def isCollisionX(self, app, dx):
        # Goes through each block
        for left, top, width, height in app.collisionBlocks:
            # Cheks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dx > 0 and self.leftX < left and self.leftX + self.linkWidth + dx > left and top < self.centerY < top + height):
                if (not self.leftX + self.linkWidth >= app.width/2):
                    self.leftX = left - self.linkWidth
                    self.centerX = left - (self.linkWidth)/2
                return True
            elif (dx < 0 and self.leftX > left and self.leftX - dx < left + width and top < self.centerY < top + height):
                if (self.leftX + self.linkWidth >= app.width/2):
                    self.leftX = left + width 
                    self.centerX = left + width + (self.linkWidth)/2
                return True
        return False

    def isCollisionY(self, app, dy):
        for left, top, width, height in app.collisionBlocks:
            if (dy > 0 and self.topY + self.linkHeight + 1 > top and left < self.centerX < left + width
                or self.topY + self.linkHeight + dy > app.lowestFloor):
                if (self.topY + self.linkHeight + dy > app.lowestFloor):
                    self.topY = app.lowestFloor - self.linkHeight
                    self.centerY = app.lowestFloor - (self.linkHeight)/2
                else:
                    self.topY = top - self.linkHeight
                    self.centerY = top - (self.linkHeight)/2
                self.isOnGround = True
                return True
            elif (dy < 0 and self.topY - 1 < top + height and left < self.centerX < left + width and not self.isJumping):
                self.topY = top + height
                self.centerY = top + (self.linkHeight)/2
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
        self.move(app, 0, -(Link.velocity + Link.gravity))
        if (self.isOnGround):
            self.isJumping = False
            Link.velocity = 20
        else:
            Link.velocity -= 2

