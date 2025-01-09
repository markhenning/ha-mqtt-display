import time

## Display update management functions
def set_pixel(gu, graphics, X,Y,colour):
    graphics.set_pen(colour)
    graphics.pixel(X,Y)
    gu.update(graphics)    

def blink_pixel(gu, graphics, X,Y,colour):
    set_pixel(gu, graphics, X,Y,colour)
    time.sleep(0.3)
    set_pixel(gu, graphics, X,Y,BLACK)
