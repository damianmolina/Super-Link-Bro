from cmu_graphics import *
from PIL import Image
from FirstLevel import *

class Link:
    velocity = 9
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
        self.isOnGround = False

        # Link's movement speed
        self.moveSpeed = 10

    def move(self, app, dx, dy):
        # Flip Link's image if he's looking the wrong way
        self.flip(dx)

        # Check if moving right and not colliding
        if (dx > 0 and not self.isCollisionX(app, dx)):
            # Checks if Link is past the middle of the screen (towards right)
            if (self.leftX + self.linkWidth >= app.width//2):
                # Moves background image and blocks
                moveBlocks(app, -dx, dy)
                app.levelLeft -= dx
            else:
                # Moves Link sprite
                self.leftX += dx
        
        # Checks if moving left and not out of bounds and is not colliding
        elif (dx < 0 and self.leftX > app.levelLeft and not self.isCollisionX(app, dx)):
             # Checks if Link is past the middle of the screen (towards left) and 
             # if Link is at the beginning of the level
            if (self.leftX - self.linkWidth <= app.width//2 and app.levelLeft < 0):
                # Moves background image and blocks
                moveBlocks(app, -dx, dy)
                app.levelLeft -= dx
            else:
                # Moves Link sprite
                self.leftX += dx
        
        # Checks collisions on Y-axis
        if (not self.isCollisionY(app, dy)):
            # Moves Link sprite
            self.topY += dy
    
    # Checks for any horizontal collisions
    def isCollisionX(self, app, dx):
        # Goes through each block
        for left, top, width, height in app.collisionBlocks:
            # Cheks direction of movement, whether it will collide and whether Link's center
            # is in the right spot for a collision to occur
            if (dx > 0 and self.leftX < left and self.leftX + self.linkWidth + dx > left and top < self.centerY < top + height):
                return True
            elif (dx < 0 and self.leftX > left and self.leftX - dx < left + width and top < self.centerY < top + height):
                return True
        return False

    def isCollisionY(self, app, dy):
        return 42

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
        force = 0.5 * Link.mass * (Link.velocity**2)
        self.topY -= force
        Link.velocity = Link.velocity - 1

        if Link.velocity < 0:
            Link.mass = -1
        
        if (Link.velocity == -10):
            self.isJumping = False
            Link.velocity = 9
            Link.mass = 1
