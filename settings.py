from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# General Galactic Unicorn setup
gu = GalacticUnicorn()
gu.set_brightness(0.2)
graphics = PicoGraphics(DISPLAY)
width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

##
##   DISPLAY LOCATIONS
##

# Vertical Lines
# X location for columns
vert_lines = [10,21,32]

# Power Display (Width needed default - 10)
power_start_x = 0
## Network Bars  (Width needed default- 10)
net_start_x = 11
net_width = 10 ## If you change this, ensure there's enough entries (width / 2) in both of the net_*bars below
## DNS Blinks  (Width needed default - 10)
dns_start_x = 22
# Clock  (Width needed - 15S)
clock_start_x = 37
clock_start_y = 1

## Basic colours
white = graphics.create_pen(255, 255, 255)
lgrey = graphics.create_pen(150, 150, 150)
green = graphics.create_pen(0, 255, 0)
red = graphics.create_pen(255, 0, 0)
blue = graphics.create_pen(0, 0, 255)
yellow = graphics.create_pen(255,255,0)
purple = graphics.create_pen(128,0,128)
black = graphics.create_pen(0, 0, 0)

##
## Power Settings
##
power_width = 10
power_rows = 10 # (note - you need top 1 for the power bar, so for the GU - "11 rows - 1 for power bar"
power_animation_delay = 75
power_map = { '5000' : red,
              '500' : yellow,
              '0' : green,
              }

##
## DNS Blink Settings
##

## Min/maxblinks for each colour, adjust here, will render "min" at program start
dot_maxes = { 'blues' : 60, 'oranges': 5, 'reds': 5 }
dot_mins = { 'blues' : 10, 'oranges': 1, 'reds': 1 }

## Map the string we're going to search for in MQTT to a set of colours defined further down
dns_colourmap = { 'no_error' : 'blues',
              'blocked' :'oranges',
              'servfail' : 'reds',
}

## Settings - Clock
ntp_pool = "pool.ntp.org"

# Colour for the bar - This gets adjusted by "fade" upwards, so this is the colour for the darkest pixels
vert_start_colour = 90
# How much to increase the colour by each step
vert_fade = 40

## Fudge so I can fade lights on the internet graphs, I can't work out how to directly edit a pen (or make a temp one, soo...)
# Each colour should increase through the array, we've got 5 columns for each colour, so we need 5 entries

net_upload = [graphics.create_pen(0, 0, 30),
        graphics.create_pen(0, 0, 60),
        graphics.create_pen(0, 0, 80),
        graphics.create_pen(0, 0, 100),
        graphics.create_pen(0, 0, 255),
]

net_download = [graphics.create_pen(0, 30, 0),
        graphics.create_pen(0, 60, 0),
        graphics.create_pen(0, 80, 0),
        graphics.create_pen(0, 100, 0),
        graphics.create_pen(0, 255, 0),
]

## DNS Blinkies colours, same as above, but you should always start with (0,0,0)

dns_colours = {
'blues' : [graphics.create_pen(0, 0, 0),
        graphics.create_pen(0, 0, 60),
        graphics.create_pen(0, 0, 80),
        graphics.create_pen(0, 0, 100),
        graphics.create_pen(0, 0, 255),
        ],
'greens' : [graphics.create_pen(0, 0, 0),
        graphics.create_pen(0, 60, 0),
        graphics.create_pen(0, 80, 0),
        graphics.create_pen(0, 100, 0),
        graphics.create_pen(0, 255, 0),
        ],
'oranges' : [graphics.create_pen(0, 0, 0),
        graphics.create_pen(150, 64, 0),
        graphics.create_pen(203, 92, 13),
        graphics.create_pen(252, 102, 0),
        graphics.create_pen(255, 191, 0),
        ],
'reds' : [graphics.create_pen(0, 0, 0),
        graphics.create_pen(60, 0, 0),
        graphics.create_pen(100, 0, 0),
        graphics.create_pen(175, 0, 0),
        graphics.create_pen(255, 0, 0),
        ],
}