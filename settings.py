from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
import colours
import utils

# # General Galactic Unicorn setup
# gu = GalacticUnicorn()
# gu.set_brightness(0.3)
# graphics = PicoGraphics(DISPLAY)
graphics = utils.graphics
gu = utils.gu
width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

### Individual Component strings
## Used by individiual handle_<thing> functions
## If these are found in the string, then it's an upload/download/full data etc
topic_network_download = 'download'
topic_network_upload = 'upload'

## Power - this string denotes the "total power usage" from the normal device stats
topic_power_total = "current_demand"

#### MQTT Topic Strings
#
# Used by the callback function in main
# If <any of the list> is in the string topic, route to power/network/dns etc
# These are all lists, not individual strings
topic_power = ['power','energy']
topic_network = ['router_current']
topic_dns = ['tdns']

## Convert all of the rgbs to "pens" so we can call them quickly and easily with pens['white'] etc
pens = colours.create_pens()

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


##
## Settings - Network
##

# ms to wait before drawing next pixel up in network display
net_animation_delay = 100

net_colour_map = { 'download': 'spring_greens',
                     'upload': 'honolulu',
}

## Scales - map a bps rate for each number of dots to draw, adjust to match connection
net_download_scale = {
    1 : 0,
    2 : 200000,
    3 : 1000000,
    4 : 5000000, 
    5 : 10000000,
    6 : 25000000,
    7 : 50000000,
    8 : 200000000,
    9 : 500000000,
    10 : 800000000,
}

net_upload_scale = {
    1 : 0,
    2 : 500000,
    3 : 1000000,
    4 : 3000000, 
    5 : 5000000,
    6 : 10000000,
    7 : 20000000,
    8 : 40000000,
    9 : 60000000,
    10 : 100000000,
}

##
## Settings - DNS Blink
##

# Flag to use data from mqtt or generate random data for the blinks
dns_use_mqtt = True

## Time to sleep between display updates (blink speed)
dns_blink_wait = 0.4

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




## The following calls functions in colours that will take the colour maps and generate lists of GU pens of various intensities
## These are used for the actual colours on the display
## Technically these should be in colours.py, but everything references them in settings.py, will migrate later
net_colours = colours.build_net_colours(net_colour_map)

clock_colours = colours.build_clock_colours(clock_colour_map)

dns_colours = colours.build_dns_colours(dns_colour_map)

## Finally, some don't need fading, just a list of pens, so we just make a list of the pens that the power display bar needs
power_colours = {}
for entry in power_map.values():
    power_colours[entry] = pens[entry]

