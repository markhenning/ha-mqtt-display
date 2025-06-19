import math
import settings
import asyncio
 
## Load in settings
start_x = settings.net_start_x
net_width = settings.net_width
# download_colours = settings.net_download
# upload_colours = settings.net_upload

## Rudimentary FIFO queues to store rolling data
download_stats = [0] * ((net_width // 2))
upload_stats = [0] * ((net_width // 2))

def draw_network_stats(graphics):
    ## We've got 10 ("net_width) columns here, to draw the graphs
    ## 5 download, 5 upload (net_width //2)
    ## New values should enter in the right column on each section
    
    ## Clear the section from memory
    graphics.set_pen(settings.pens['black'])
    graphics.rectangle(start_x,0,net_width,settings.height)    
    
    ## Adjust the display memory with new data
    
    ## Download stats:
    draw_network_history(graphics, start_x, download_stats, settings.net_download, flip=False, offset=0)
    ## Upload stats:
    draw_network_history(graphics, start_x, upload_stats, settings.net_upload, flip=False, offset=(net_width // 2))

    # And finally, display the new charts
    settings.gu.update(graphics)

def draw_network_history(graphics, start_x, drawdata, colour, flip=False, offset=0):

    values = drawdata[:-1]
    if flip:
        values.reverse()
            
    column = 0
    for net_stat in values:
        graphics.set_pen(colour[column])
        graphics.line((start_x + column + offset), settings.height, (start_x + column + offset), (settings.height - net_stat))
        column += 1
        
def calculate_network_pixels(bps, direction):
    dots = 1
    if direction == 'up':
        scale = settings.net_upload_scale
    else:
        scale = settings.net_download_scale
    for key in scale.keys():
        if scale[key] < bps:
            dots = key

    return dots

async def draw_current(graphics):
    
    ## Lock these so we don't have the underlying array changing in the 0.5s we're drawing
    upstat = upload_stats[-1]
    downstat = download_stats[-1]
    
    ## Work out how many we need to run, bigger number wins
    if downstat < upstat:
        loop = upstat
    else:
        loop = downstat
    
    ## Loop and add 1 pixel height every <period>, stopping when the height's correct
    for i in range(loop + 1):
        if i <= downstat:
            graphics.set_pen(settings.net_download[-1])
            ### I'm not insane, "line" function can have off by one errors if it's a single pixel width
            graphics.line((start_x + (net_width // 2) - 1), settings.height, (start_x + (net_width // 2) - 1), (settings.height-i))
        if i <= upstat:
            graphics.set_pen(settings.net_upload[-1])
            graphics.line((start_x + (net_width - 1)), settings.height, (start_x + (net_width - 1)), (settings.height-i))
        settings.gu.update(graphics)
        await asyncio.sleep_ms(settings.net_animation_delay)

async def handle_network(graphics, string_topic,string_message):

    global  download_stats,  upload_stats
    int_message = int(float(string_message))
    
    
    if "download" in string_topic:
        bar_height = calculate_network_pixels(int_message,'up')
        download_stats.pop(0)
        download_stats.append(bar_height)
        # We normally get up and down stats less than 0.1 seconds apart, there's no point in re-drawing for both
        #draw_network_stats(graphics)
    elif "upload" in string_topic:
        bar_height = calculate_network_pixels(int_message,'down')
        upload_stats.pop(0)
        upload_stats.append(bar_height)
        draw_network_stats(graphics)
        asyncio.create_task(draw_current(graphics))


    else:
        print("Error: Don't know what to do with " + string_topic)

