from cmu_graphics import *
from PIL import Image
from Characters import *
from FirstLevel import *

class Arrow:
    def __init__(self, app):
        # From https://www.reddit.com/r/PixelArt/comments/ldd4fb/arrow_first_animated_work_outside_of_minecraft/
        arrow = Image.open('Images/Arrow.png')
        arrow = arrow.resize((40, 40))
        self.image = arrow
