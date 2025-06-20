import math
import settings
import asyncio
import utils

current_displayed_power = []

start_x = settings.power_start_x
width = settings.power_width
rows = settings.power_rows

## Set the pens we want to use:
fg_pen = settings.power_bar_fg
bg_pen = settings.power_bar_bg

## Storage vars for actual energy data
energy_stats = {}
total_energy = 0

def get_topbar_colour(total_energy):
    bar_colour = settings.pens['white']
    for key in sorted(settings.power_map.keys(), reverse=True): 
        if total_energy >= key:
            bar_colour = settings.pens[settings.power_map[key]]
            break
    return bar_colour


async def draw_power_chase(graphics):
    global current_displayed_power

    ## We've got "row" lines of LEDs (default 10), but might not have that many values for power,, pad the list out as needed
    while len(current_displayed_power) < rows:
        current_displayed_power.append(0)
  
    ## Ok, so new array, 30 x 10 essentially, right 10 - current graphics, middle 10 - extend back to make a 10 long line, then black, first 10, new power stats
    #   # e.g, for if we're updating from 7 to 6:
    #  XXXXXX...........XXXXXXXXXX...
    #|New Stats| Spacer| Old Stats|
    #And essentiall, we slide a view window of width 10 down from right to left

    power_display = []

    ##Get the current recorded power values out for easy sorting
    power_list = []
    for key in energy_stats:
        power_list.append(energy_stats[key])
        
    # Reverse Sort the list so we get the stats descending for the graphs
    power_list.sort(reverse=True)
    ## Going to pull out the "new" power display stats in here so we can use them later
    current_power_display_temp = []
    
    ## Let's do the new stats first:
    ## We may still not have the total energy counter (their minimum update time is 15 seconds, skip if we don't)
    if total_energy != 0:
        
        line_no = 0
        for usage in power_list:
            ## Process only as many lines as we've got rows to display
            if line_no == rows:
                break
            else:
                ## Work out how long the bar is ((percentage of total) /10) pixels
                #The following will show as a rough percentage, but since I've got one large use and the rest are small
                # it makes the graph pretty boring, soooo I'm changing it to draw percentages of the highest user
                #length = math.ceil(usage / total_energy * 10)
                length = math.ceil(usage / (power_list[0]) * 10)
                
                ## Sadly, we can get some stats from devices that are higher than last recorded total
                ## (e.g. 10 seconds after boiling a kettle, kettle will say 3000, total power will still be 250)
                ## Not much we can do about this, so let's just make sure we never get more than 10 lights
                
                if length > width:
                    length = width
                
                current_power_display_temp.append(length)

                templine = ['X'] * length
                templine += (['.'] * (width - length))

                power_display.append(templine)

                line_no = line_no + 1
                
        ## We've build the first third, next up, we need to know what the "new values" are and we draw
        # .'s to pad the blank space until the point where we add in X's to extend the current line backwards until it's {width} long
        
        ## E.g. if current power draw is 9, it's "9 x X's, followed by a ." (Adding in extension of . backwards)
        # then the current power draw of 9 ones and a 0 current power draw)
        
        for line in range(0,(len(power_display))):
            length = current_power_display_temp[line]
            
            if length == width:
                power_display[line] += (['.'] * width)
                power_display[line] += (['X'] * width)
            elif length == 0:
                # Pad all 1's
                power_display[line] += (['X'] * width)
                power_display[line] += (['.'] * width)
            else:
                power_display[line] += (['.'] * (length))
                power_display[line] += (['X'] * width)
                power_display[line] += (['.'] * (width - length))
                
        ## Tweaking - I did all the work, but 10 dots is too much, let's strip some out:      
        for line in range(0,len(power_display)):
            power_display[line].pop(19)
            power_display[line].pop(18)
            power_display[line].pop(17)
            power_display[line].pop(16)
            power_display[line].pop(15)
            power_display[line].pop(13)

        ## Debugging stuff, will print line array to terminal
        # for line in power_display:
        #     print(line)
        # print()

        ## Display buffer is now built, array in memory of rows, with each row length of 3*width (excluding the fiddle of the last few lines)

        ## Now we can actually shift the "view window" backwards so the display scrolls 

        for shift in range((width + 2),-1,-1):
            for y in range(0,len(power_display)):
                for x in range(0,width):
                    if power_display[y][(shift+x)] == 'X':
                        graphics.set_pen(fg_pen)
                    else:
                        graphics.set_pen(bg_pen)
                    graphics.pixel(start_x + x,y+1)         
            utils.gu.update(graphics)
            await asyncio.sleep_ms(settings.power_animation_delay)
        
        current_power_display = []
        current_power_display += current_power_display_temp


    ## Draw the bar at the top of the section for total power
    graphics.set_pen(get_topbar_colour(total_energy))
    graphics.line(start_x, 0, width, 0)
    utils.gu.update(graphics)



async def handle_energy(graphics, string_topic, string_message):
    
    ## Take a topic + message for a power stat and store it
    global  energy_stats, total_energy

    ## MQTT will sometimes throw an "unavailable from HA there's a device error etc, just bin these"
    if string_message != "unavailable":

        ## Then work out what to do
        if "current_demand" in string_topic: ## "Current Demand" is the total energy draw from Octopus, store it
            total_energy = int(float(string_message))
            await draw_power_chase(graphics)
        
        else: ## Otherwise, it's a device specific power stat, store it
            messagestat = int(float(string_message))
            energy_stats.update({string_topic : messagestat})

