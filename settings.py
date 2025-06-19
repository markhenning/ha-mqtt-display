from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# General Galactic Unicorn setup
gu = GalacticUnicorn()
gu.set_brightness(0.2)
graphics = PicoGraphics(DISPLAY)
width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

## Basic colours - called by various scripts, placed here to be available below
white = graphics.create_pen(255, 255, 255)
lgrey = graphics.create_pen(150, 150, 150)
green = graphics.create_pen(0, 255, 0)
spring = graphics.create_pen(20,225,148)
neon_green = graphics.create_pen(77,255,77)
red = graphics.create_pen(255, 0, 0)
blue = graphics.create_pen(0, 0, 255)
yellow = graphics.create_pen(255,255,0)
purple = graphics.create_pen(128,0,128)
plum = graphics.create_pen(137,40,143)
black = graphics.create_pen(0, 0, 0)

##
##   DISPLAY LOCATIONS
##

# Vertical Lines
# X location for columns
vert_lines = [10,21,32]
# Colour for the bar - This gets adjusted by "fade" upwards, so this is the colour for the darkest pixels
vert_start_colour = 90
# How much to increase the colour by each step
vert_fade = 40

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
power_map = { 5000 : red,
              500 : yellow,
              0 : spring,
              }
# bar_colours
power_bar_fg = plum
power_bar_bg = black

##
## Settings - Clock
##

ntp_pool = "pool.ntp.org"

# map what colour to use for each time unit: (needs to have entry in "clock_colours")
clock_colour_map = { 'hrs': 'spring_greens',
                     'min': 'sea_greens',
                     'sec': 'blues',
}

## Clock colours, need 6 for each, hours will only use [2] and [5].
## Not all of these are used, but serve as options for colours

## I really need to automate these to do "0% 15%, 30%, 50% 70%, 100%" and autofill the list, one day...
clock_colours = {
        'reds' : [graphics.create_pen(0, 0, 0),
                graphics.create_pen(80, 0, 0),
                graphics.create_pen(120, 0, 0),
                graphics.create_pen(160, 0, 0),
                graphics.create_pen(200, 0, 0),
                graphics.create_pen(240, 0, 0),
        ],
        'yellows' : [graphics.create_pen(0, 0, 0),
                graphics.create_pen(80, 80, 0),
                graphics.create_pen(120, 120, 0),
                graphics.create_pen(160, 160, 0),
                graphics.create_pen(200, 200, 0),
                graphics.create_pen(240, 240, 0),
        ],
        'blues' : [graphics.create_pen(0, 0, 0),
                graphics.create_pen(73, 103, 125),
                graphics.create_pen(93, 123, 155),
                graphics.create_pen(113, 138, 185),
                graphics.create_pen(133, 173, 215),
                graphics.create_pen(153, 203, 255),
        ],
        'spring_greens' : [graphics.create_pen(0, 0, 0),
                graphics.create_pen(5,105,58),
                graphics.create_pen(10,135,88),
                graphics.create_pen(14,160,108),
                graphics.create_pen(17,190,128),
                graphics.create_pen(20,225,148),
        ],
        'sea_greens' : [graphics.create_pen(0, 0, 0),
                graphics.create_pen(0,69,65),
                graphics.create_pen(0,89,85),
                graphics.create_pen(0,109,105),
                graphics.create_pen(0,139,135),
                graphics.create_pen(0,169,165),
        ],
        'mangos' : [graphics.create_pen(0, 0, 0),
                graphics.create_pen(90,39,11),
                graphics.create_pen(145,59,21),
                graphics.create_pen(185,79,31),
                graphics.create_pen(225,99,41),
                graphics.create_pen(255,119,51),
        ],

}



## Settings - Network

# ms to wait before drawing next pixel up in network display
net_animation_delay = 100

# Colours for the network bars each colour should increase through the array, we've got 5 columns for each colour, so we need 5 entries


net_colours = {
        'blues' : [graphics.create_pen(0, 0, 30),
                graphics.create_pen(0, 0, 60),
                graphics.create_pen(0, 0, 80),
                graphics.create_pen(0, 0, 100),
                graphics.create_pen(0, 0, 255),
        ],
        'honolulu' : [graphics.create_pen(2, 19, 45),
                graphics.create_pen(3, 29, 65),
                graphics.create_pen(3, 39, 85),
                graphics.create_pen(6, 49, 105),
                graphics.create_pen(14, 129, 200),
        ],
        'greens' : [graphics.create_pen(0, 30, 0),
                graphics.create_pen(0, 60, 0),
                graphics.create_pen(0, 80, 0),
                graphics.create_pen(0, 100, 0),
                graphics.create_pen(0, 255, 0),
        ],
        'sea_greens' : [graphics.create_pen(0,69,65),
                graphics.create_pen(0,89,85),
                graphics.create_pen(0,109,105),
                graphics.create_pen(0,139,135),
                graphics.create_pen(0,169,165),
        ],
        'spring_greens' : [graphics.create_pen(1,30,15),
                graphics.create_pen(4,55,35),
                graphics.create_pen(7,80,55),
                graphics.create_pen(9,100,77),
                graphics.create_pen(20,225,148),
        ],
}

net_upload = net_colours['honolulu']

net_download = net_colours['spring_greens']


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

## Min/maxblinks for each colour, adjust here, will render "min" at program start
dot_maxes = { 'blues' : 60, 'oranges': 5, 'reds': 5 }
dot_mins = { 'blues' : 10, 'oranges': 0, 'reds': 0 }

## Map the string we're going to search for in MQTT to a set of colours defined further down
dns_colour_map = { 'no_error' : 'blues',
              'blocked' : 'oranges',
              'servfail' : 'reds',
}

## Take the DNS queries and divide by X to give the number of dots (default 10 for all 3), will be adjusted to between min and max if necessary
dns_scale_factors = { 'no_error' : 10,
              'blocked' : 10,
              'servfail' : 10,
}

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
