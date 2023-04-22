from cmu_graphics import *
from PIL import Image
from Characters import *
from Weapons import *
import random

class Item:
    def __init__(self, app, itemBlock):
        left, top, width, height = itemBlock
        prob = random.random()
        if (app.link.moveSpeed == 16 and app.link.originalVelocity == -30):
            self.item = 0
        elif (app.link.moveSpeed == 16):
            if (prob > 0.7):
                self.item = 1
            else:
                self.item = 0
        elif (app.link.originalVelocity == -30):
            if (prob > 0.7):
                self.item = 2
            else:
                self.item = 0
        else:
            if (prob > 0.7):
                self.item = random.randint(1,2)
            else:
                self.item = 0

        if (self.item == 0):
            self.image = Image.open('Images/Bomb.png').resize((32, 32))
        elif (self.item == 1):
            # From https://www.cleanpng.com/png-portable-network-graphics-pixel-art-clip-art-power-7279751/
            self.image = Image.open('Images/JumpBoost.png').resize((32, 32))
        elif (self.item == 2):
            self.image = Image.open('Images/MoveBoost.png').resize((32, 32))

        self.leftX = left
        self.topY = top - 32
        self.delete = False
        self.used = False

    def __eq__(self, other):
        if (not isinstance(other, Item)): return False

        if (self.leftX == other.leftX and self.topY == other.topY):
            return True
        else:
            return False        
        