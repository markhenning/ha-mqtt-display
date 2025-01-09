import math
import settings as settings
import asyncio
 
## Load in settings
start_x = settings.net_start_x

## Rudimentary FIFO queues to store rolling data
download_stats = [0,0,0,0,0]
upload_stats = [0,0,0,0,0]


def draw_network_stats(graphics):
    ## We've got 10 columns here, 11 -> 20 to draw the graphs
    ## 5 download, 5 upload
    ## New values should enter in the middle, and then phase outward
    
    ## Clear the section from memory
    graphics.set_pen(settings.black)
    graphics.rectangle(start_x,0,10,11)    
    
    ## Adjust the display memory with new data
    
    ## Download stats:
    draw_network_bars(graphics, start_x, download_stats, settings.net_download, flip=False, offset=0)
    ## Upload stats:
    draw_network_bars(graphics, start_x, upload_stats, settings.net_upload, flip=False, offset=5)

    # And finally, display the new charts
    settings.gu.update(graphics)

def draw_network_bars(graphics, start_x, drawdata, colour, flip=False, offset=0):

    values = drawdata[:]
    if flip:
        values.reverse()
            
    column = 0
    for height in values:
        graphics.set_pen(colour[column])
        graphics.line((start_x + column + offset), 11, (start_x + column + offset), (11-height))
        column += 1
        
def calculate_network_pixels(bps):
    ## Since the value here can range from 0 -> 921,600 a single bar chart won't be a good idea here
    ## I'm sure there's a log function to work this out better, but I'm going to hard code some values here because mine won't change for years
    if bps > 8000000:
        return 10
    elif 6000000 < bps <= 8000000:
        return 9
    elif 2000000 < bps <= 4000000:
        return 8
    elif 500000 < bps <= 2000000:
        return 7
    elif 50000 < bps <= 500000:
        return 6
    elif 10000 < bps <= 50000:
        return 5
    elif 5000 < bps <= 10000:
        return 4
    elif 2000 < bps <= 5000:
        return 3
    elif 1000 < bps <= 2000:
        return 2
    else:
        return 1

async def handle_network(graphics, string_topic,string_message):
    global  download_stats,  upload_stats
    int_message = int(float(string_message))
    bar_height = calculate_network_pixels(int_message)
    
    if "download" in string_topic:
        download_stats.pop(0)
        download_stats.append(bar_height)
        # We normally get up and down stats less than 0.1 seconds apart, there's no point in re-drawing for both
        #draw_network_stats(graphics)
    elif "upload" in string_topic:
        upload_stats.pop(0)
        upload_stats.append(bar_height)
        draw_network_stats(graphics)

    else:
        print("Error: Don't know what to do with " + string_topic)