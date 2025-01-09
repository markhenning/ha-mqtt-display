from mqtt_as import MQTTClient, config
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

# General Galactic Unicorn setup
gu = GalacticUnicorn()
gu.set_brightness(0.2)
graphics = PicoGraphics(DISPLAY)

## WiFi/MQTT Settings - single quoted values please - e.g. 'my-wifi-network'

config['ssid'] = '<WiFI-SSID>'
config['wifi_pw'] = '<WiFi-Password'
config['server'] = '<MQTT-Server' 
config['user'] = '<MQTT-Username'
config['password'] = '<MQTT-Password'

## Don't forget the # on the end here to collect all of the entries
mqtt_topic = 'haexport/sensor/#'

##
##   DISPLAY LOCATIONS
##

# Vertical Lines
# X location for columns
vert_lines = [10,21,32]

## Network Bars
net_start_x = 11
## DNS Blinks
dns_start_x = 22
# Clock
clock_start_x = 37
clock_start_y = 1

## DNS Blink Settings

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

## Set variables to the size of the display for looping later
width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

## Set colours so we can use them quickly later
WHITE = graphics.create_pen(255, 255, 255)
LGREY = graphics.create_pen(150, 150, 150)
GREEN = graphics.create_pen(0, 255, 0)
RED = graphics.create_pen(255, 0, 0)
BLUE = graphics.create_pen(0, 0, 255)
YELLOW = graphics.create_pen(255,255,0)
PURPLE = graphics.create_pen(128,0,128)
BLACK = graphics.create_pen(0, 0, 0)

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


## DNS Blinkies colours, same as above, 

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