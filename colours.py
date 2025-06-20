from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
import utils

graphics = utils.graphics

rgbs = {
    'spring_greens' : [20,225,148],
    'sea_greens' : [0,169,165],
    'blues' : [153, 203, 255],
    'mango' : [255,119,51],
    'white' : [255, 255, 255],
    'lgrey' : [150, 150, 150],
    'green' : [0, 255, 0],
    'spring' : [20,225,148],
    'neon_green' : [77,255,77],
    'red' : [255, 0, 0],
    'blue' : [0, 0, 255],
    'yellow' : [255,255,0],
    'purple' : [128,0,128],
    'plum' : [137,40,143],
    'black' : [0, 0, 0],
    'honolulu' : [14, 129, 200]
}

def create_pens(graphics):
     
    ## Convert all of the rgbs to "pens" so we can call them quickly and easily with pens['white'] etc
    c_pens = {}
    for key in rgbs:
        c_pens[key] = graphics.create_pen(rgbs[key][0],rgbs[key][1],rgbs[key][2])
    
    return c_pens

## Function to take an RGB value and return a list of fading colours, so we don't have to specify all the rows manually
def build_colour_fade (graphics, colour, lines = 5, inc_zero = True, sharp_fade = True):
    ## Set the rate of fading, hard coded for now
    if sharp_fade:
        fade = [20,30,40,50,100]
    else:
        fade = [40,55,70,85,100]

    # If we need to, start off with a line of 0's
    if inc_zero:
        temp_colour = [graphics.create_pen(0, 0, 0)]
    else:
        temp_colour = []

    for i in range(lines):
        scale = fade[i] / 100
        temp_colour.append(graphics.create_pen(round(scale * colour[0]), round(scale * colour[1]), round(scale * colour[2])))

    return temp_colour