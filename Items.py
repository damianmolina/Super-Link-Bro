from cmu_graphics import *
from PIL import Image
from Characters import *
from Weapons import *
import random

class Item:
    def __init__(self, app, itemBlock):
        # Dimensions of item block that was hit
        left, top, width, height = itemBlock
        prob = random.random()
        # If movement and jump boost is already applied, only spawn bomb
        if (app.link.moveSpeed == 16 and app.link.originalVelocity == -30):
            self.item = 0
        # If movement boost already applied, only give either bomb or jump boost
        elif (app.link.moveSpeed == 16):
            if (prob > 0.7):
                self.item = 1
            else:
                self.item = 0
        # If jump boost already applied, only give either bomb or movement boost
        elif (app.link.originalVelocity == -30):
            if (prob > 0.7):
                self.item = 2
            else:
                self.item = 0
        # Give any of the power ups
        else:
            if (prob > 0.7):
                self.item = random.randint(1,2)
            else:
                self.item = 0

        # Loads up image of power up
        if (self.item == 0):
            self.image = Image.open('Images/Bomb.png').resize((32, 32))
        elif (self.item == 1):
            # From https://www.cleanpng.com/png-portable-network-graphics-pixel-art-clip-art-power-7279751/
            self.image = Image.open('Images/JumpBoost.png').resize((32, 32))
        elif (self.item == 2):
            # From https://icons-for-free.com/1-131982518547162326/
            self.image = Image.open('Images/MoveBoost.png').resize((32, 32))

        # Location of item 
        self.leftX = left
        self.topY = top - 32


    # Items are equal to each other if their locations are equal
    def __eq__(self, other):
        if (not isinstance(other, Item)): return False

        if (self.leftX == other.leftX and self.topY == other.topY):
            return True
        else:
            return False        
        