from cmu_graphics import *
from PIL import Image
from Characters import *
from Weapons import *
import random

class Item:
    def __init__(self, app, itemBlock):
        left, top, width, height = itemBlock
        self.item = 0
        if (self.item == 0):
            self.image = Image.open('Images/Bomb.png').resize((32, 32))
        self.leftX = left
        self.topY = top - 32
        self.delete = False
        self.used = False

    def __eq__(self, other):
        if (not isinstance(other, Item)): return False

        if (self.item == other.item):
            return True
        else:
            return False        
        