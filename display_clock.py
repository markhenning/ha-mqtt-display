import settings
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
import asyncio
import time
import socket
import struct
import machine
import clock_font as cf
import utils

#### Clock Overview
##
## print_clock() is an async task that loops over:
## 1. check if the time has changed, if so
## 2. Generate a "Buffer" that holds a 2D array of '.' and 'X' for each needed number
## 3. Update pixels in memory
## 4. Updates the display

## Load variables
pool = settings.ntp_pool
fg_pen = settings.clock_time_fg
bg_pen = settings.clock_time_bg
clk_col = settings.clock_colours
clk_col_map = settings.clock_colour_map

## Display Location:
start_x = settings.clock_start_x
start_y = settings.clock_start_y

## Internal stuff
NTP_DELTA = 2208988800
rtc = machine.RTC()
hr_offset = 0

displayedTime = 0000
display_buffer = [] * 5


## set_time is from https://gist.github.com/aallan - set the hardware RTC from NTP
## Called one during main script startup
def set_time():
    print("Setting the time...")
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(pool, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
        print(f"Clock Set")
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - ( NTP_DELTA - (hr_offset * 3600))
    tm = time.gmtime(t)
    rtc.datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))


## Create and return a list of lists of X and . for foreground/background pixels
def create_buffer(curr_time):
    ## Create empty buffer
    display_buffer = []
    
    ## Split time into list of ints
    digits = list(curr_time)

    ## Loop and combine the relevant rows from each digit we need from the font
    ## Everything's 5 lines high, so...
    for i in range(5):
        display_buffer.append(cf.font[digits[0]][i] + '.' + cf.font[digits[1]][i] + '.' + cf.font[digits[2]][i] + '.' + cf.font[digits[3]][i])
    
    return display_buffer


def update_clock_display(graphics, curr_time):
       
    clock_buffer = create_buffer(curr_time)

    ## Loop and print
    for y in range(len(clock_buffer)):
        for x in range(len(clock_buffer[0])):
            if clock_buffer[y][x] == 'X':
                graphics.set_pen(fg_pen)
            else:
                graphics.set_pen(bg_pen)
            graphics.pixel((start_x + x),(start_y + y)) # type: ignore
    utils.gu.update(graphics)    

def update_bars(graphics):
    
    # Get the current times for each time unit
    times = { 'hrs' : time.localtime()[3],
              'min' : time.localtime()[4],
              'sec' : time.localtime()[5],
    }

    ## Start drawing the bars in the right locations:
    bar_start_x = start_x + 2
    bar_start_y = 7

    ## Change the memory for the bars to all black before the redraw
    graphics.set_pen(settings.pens['black'])
    graphics.rectangle(bar_start_x , bar_start_y, 12, 3)
      
    count = 0
    for unit in sorted(times.keys()):
        
        ## Take each of the time units and work out how many full and partial pixels we need:
        if unit == 'hrs':
            full_pixel = times[unit] // 2
            partial = times[unit] % 2
        else:
            full_pixel = times[unit] // 5
            partial = times[unit] % 5
        
        ## Draw a line of "full" pixels
        graphics.set_pen(clk_col[clk_col_map[unit]][-1])
        graphics.line(bar_start_x, bar_start_y + count,  bar_start_x + full_pixel, bar_start_y  + count)
        
        # Add on one pixel of the right colour for the "partial"
        graphics.set_pen(clk_col[clk_col_map[unit]][partial])
        graphics.pixel(bar_start_x + full_pixel, bar_start_y + count)
        
        count = count + 1
    
    # Finally, draw it to the display
    utils.gu.update(graphics) 



async def print_clock(graphics):
    # Last printed minute (so we're not redrawing over and over again)
    printed_min = -1
    
    draw_clock_chrome(graphics)
    
    while True:

        ## First off - update the bars under the clock, this needs to happen every second
        update_bars(graphics)
        
        
        ## Next - we need to check if we've updated the time display this minute, no point in doing lots of work for no reason
        ## time.datetime()[5] is current minute, adjust [5] to get other fields (3 is hour, 6 is seconds)

        if rtc.datetime()[5] != printed_min:
            ## Updated printed min so we don't do it again
            printed_min = rtc.datetime()[5]
            ## Generate a text string of HHMM
            curr_time = "%02d%02d"%time.localtime()[3:5]
            
            ## Test function - generate the pixels for the display and print to stdout
            #printBuffer(curr_time)
            
            ## Send the time off to be put on the screen
            update_clock_display(graphics, curr_time)
            
        ## Since we've got a check in place to prevent unecessary work, we can spin this every second
        await asyncio.sleep(1)

def draw_clock_chrome(graphics):
    # Put in the white vertical end bars for the bars, these don't need to be here, will move later
    graphics.set_pen(fg_pen)
    graphics.line(start_x+1, 7, start_x+1, 10)
    graphics.line(start_x+14, 7, start_x+14, 10)
    
# Debug function - not used - print out the buffer that would get made for display
def print_buffer(curr_time):
    print(curr_time)
    for line in create_buffer(curr_time):
        print(line)


## This one's just a test function, doesn't do anything in the end solution
#def setClock(graphics):
#    graphics.set_font("bitmap6")
#    graphics.set_pen(graphics.create_pen(0, 0, 0))
#    graphics.set_pen(graphics.create_pen(155, 155, 155))
#    graphics.text("2234", 33, 0, 0, 0)
#    utils.gu.update(graphics)
