import settings
import asyncio

## Load in variables
cols = settings.vert_lines
start_colour = settings.vert_start_colour
fade_colour = settings.vert_fade

def draw_gridline_vert(graphics):

    ## Work out the height of a column, and then draw lines - increase brightness, decreasing size by one each time
    ## to give a fade effect

    ## // is integer division, work out the mid point
    mid = (settings.height//2) 

    for col in cols:
        up = 0
        down = settings.height
        colour = start_colour
        while up <= mid :

            graphics.set_pen((graphics.create_pen(colour, colour, colour)))
            graphics.line(col, up , col, down)
            up = up + 1
            down = down - 1
            colour = colour + fade_colour
        
        ## If we've got an odd number of LEDs to light, we need to finally paint the middle pixel
        if settings.height//2 :

            if colour > 255:
                colour = 255
            graphics.set_pen((graphics.create_pen(colour, colour, colour)))
            graphics.pixel(col,mid)
            
    settings.gu.update(graphics)
    
#################################################################################################
### Misc Functions for display etc, none of these are used but I want somewhere to store them
#################################################################################################
    

## Display update management functions
#def set_pixel(X,Y,colour):
#    graphics.set_pen(colour)
#    graphics.pixel(X,Y)
#    gu.update(graphics)    

# async def blink_pixel(X,Y,colour):
#     print("Start Blink")
#     set_pixel(X,Y,colour)
#     await asyncio.sleep(0.3)
#     set_pixel(X,Y,settings.black)
#     print("End Blink")

# async def set_pixel(X,Y,colour):
#     graphics.set_pen(colour)
#     graphics.pixel(X,Y)
#     gu.update(graphics)   

# def blink(x,y):
#     await set_pixel(x,y,GREEN)
#     await asyncio.sleep(0.1)
#     await set_pixel(x,y,BLACK)
#     await asyncio.sleep(0.1)

