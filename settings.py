from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# General Galactic Unicorn setup
gu = GalacticUnicorn()
gu.set_brightness(0.3)
graphics = PicoGraphics(DISPLAY)
width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

## Basic colours - called by various scripts, placed here to be available below
## If you need a new colour, add it here, and then into the "<thing>_colour_map" for the relevant section
## Note: they need to be run through "graphics.create_pen(rgb) to make an actual pen to use, if you're adding
## new outside of the maps, make sure it gets called.
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

## Convert all of the rgbs to "pens" so we can call them quickly and easily with pens['white'] etc
pens = {}
for key in rgbs:
     pens[key] = graphics.create_pen(rgbs[key][0],rgbs[key][1],rgbs[key][2])

# white = graphics.create_pen(255, 255, 255)
# lgrey = graphics.create_pen(150, 150, 150)
# green = graphics.create_pen(0, 255, 0)
# spring = graphics.create_pen(20,225,148)
# neon_green = graphics.create_pen(77,255,77)
# red = graphics.create_pen(255, 0, 0)
# blue = graphics.create_pen(0, 0, 255)
# yellow = graphics.create_pen(255,255,0)
# purple = graphics.create_pen(128,0,128)
# plum = graphics.create_pen(137,40,143)
# black = graphics.create_pen(0, 0, 0)

## Function to take an RGB value and return a list of fading colours, so we don't have to specify all the rows manually
def build_colour_fade (colour, lines = 5, inc_zero = True, sharp_fade = True):
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



##
##   DISPLAY LOCATIONS
##

# Vertical Lines
# X location for columns
vert_lines = [10,21,32]
# Colour for the bar - This gets adjusted by "fade" upwards, so this is the colour for the darkest pixels
vert_start_colour = 90
# How much to increase the colour by each step
vert_fade = 20

##
## Settings - Display Locations
## 

# Power Display (Width needed default - 10)
power_start_x = 0
## Network Bars  (Width needed default- 10)
net_start_x = 11
## If you change this, ensure there's enough entries (width / 2) in both of the net_*bars below
net_width = 10 
## DNS Blinks  (Width needed default - 10)
dns_start_x = 22
dns_width = 10
# Clock  (Width needed - 15)
clock_start_x = 37
clock_start_y = 1

##
## Settings - Power
##

power_width = 10
power_rows = 10 # (note - you need top 1 for the power bar, so for the GU - "11 rows - 1 for power bar"
power_animation_delay = 60
# Threshold powers for what colour to make the top bar
power_map = { 5000 : 'red',
              500 : 'yellow',
              0 : 'spring',
              }
# bar_colours
power_bar_fg = pens['plum']
power_bar_bg = pens['black']

## Use the selected colours to create a dict of colours with all their scalings etc
## For each one, we'll make an array of "'colour': [100%Colour,80%Colour,....']"
power_colours = {}
for entry in power_map.values():
    power_colours[entry] = pens[entry]


##
## Settings - Clock
##

ntp_pool = "pool.ntp.org"

clock_time_fg = pens['lgrey']
clock_time_bg = pens['black']

# map what colour to use for each time unit:
## Change this and make sure the colours are in "rgbs" above to change anything in the clock
clock_colour_map = { 'hrs': 'spring_greens',
                     'min': 'sea_greens',
                     'sec': 'blues',
}

## Use the selected colours to create a dict of colours with all their scalings etc
## For each one, we'll make an array of "'colour': [100%Colour,80%Colour,....']"
clock_colours = {}
for entry in clock_colour_map.values():
    clock_colours[entry] = build_colour_fade(rgbs[entry], sharp_fade= False, inc_zero= True)

##
## Settings - Network
##

# ms to wait before drawing next pixel up in network display
net_animation_delay = 100

net_colour_map = { 'download': 'spring_greens',
                     'upload': 'honolulu',
}

# Colours for the network bars each colour should increase through the array, we've got 5 columns for each colour, so we need 5 entries
net_colours = {}
for entry in net_colour_map.values():
    net_colours[entry] = build_colour_fade(rgbs[entry], sharp_fade= True, inc_zero = False)

net_upload = net_colours[(net_colour_map['upload'])]
net_download = net_colours[(net_colour_map['download'])]

## Scales - map a bps rate for each number of dots to draw, adjust to match connection
net_download_scale = {
    1 : 0,
    2 : 2000,
    3 : 5000,
    4 : 10000, 
    5 : 50000,
    6 : 500000,
    7 : 2000000,
    8 : 2000000,
    9 : 4000000,
    10 : 8000000,
}

net_upload_scale = {
    1 : 0,
    2 : 1000,
    3 : 4000,
    4 : 10000, 
    5 : 25000,
    6 : 250000,
    7 : 500000,
    8 : 700000,
    9 : 900000,
    10 : 1000000,
}

##
## Settings - DNS Blink
##

# Flag to use data from mqtt or generate random data for the blinks
dns_use_mqtt = True

## Map the string we're going to search for in MQTT to a set of colours defined further down
dns_colour_map = { 'no_error' : 'honolulu',
              'blocked' : 'mango',
              'servfail' : 'red',
}

## Min/maxblinks for each colour, adjust here, will render "min" at program start
## This needs to be updated with the colours when changed, but it really should just be "no_error", etc, work to do....
dot_maxes = { 'honolulu' : 60, 'mango': 5, 'red': 5 }
dot_mins = { 'honolulu' : 10, 'mango': 0, 'red': 0 }

## Number of dot brightness levels (Must match the number of entries in the colours list in dns_colours['colour'])
dot_levels = 5

## Take the DNS queries and divide by X to give the number of dots (default 10 for all 3), will be adjusted to between min and max if necessary
dns_scale_factors = { 'no_error' : 10,
              'blocked' : 10,
              'servfail' : 10,
}

## Generate the internal colour lists for us to call later
dns_colours = {}
for entry in dns_colour_map.values():
    dns_colours[entry] = build_colour_fade(rgbs[entry], sharp_fade= True, inc_zero = True)
