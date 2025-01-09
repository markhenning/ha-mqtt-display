import math
import settings as settings
import asyncio

current_displayed_power = []

async def draw_power_chase(graphics):
    global current_displayed_power

    ## We've got 10 lines of LEDs, but might not have 10 values for power, that's line, pad the list out
    while len(current_displayed_power) < 10:
        current_displayed_power.append(0)
    #print("Current displayed power length: " + str(len(current_displayed_power)))
    

    ## Ok, so new array, 30 x 10 essentially, right 10 - current graphics, middle 10 - extend back to make a 10 long line, then black, first 10, new power stats
    #   # e.g, for if we're updating from 7 to 6:
    #  XXXXXX-----------XXXXXXXXXX---
    # |New Stats| Spacer   | Old Stats|
    #And essentiall, we slide a window of width 10 down from right to left

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
            ## We've only got 10 lines, so if we're over that, just give up
            if line_no == 10:
                break
            else:
                ## Work out how long the bar is ((percentage of total) /10) pixels
                #The following will show as a rough percentage, but since I've got one large use and the rest are small
                # it makes the graph pretty boring, soooo I'm changing it to draw percentages of the highest user
                #length = math.ceil(usage / total_energy * 10)
                length = math.ceil(usage / (power_list[0]) * 10)
                
                ## Sadly, we can get some stats from devices that are higher than last recorded total
                ## (e.g. 10 seconds after boiling a kettle)
                ## Not much we can do about this, so let's just make sure we never get more than 10 lights
                
                if length > 10:
                    length = 10
                
                ##
                #print(current_power_display_temp)
                current_power_display_temp.append(length)
                #print(current_power_display_temp)
                
                templine = ['C'] * length
                templine += (['B'] * (10 - length))

                power_display.append(templine)

                line_no = line_no + 1
                
        ## We've build the first third, next up, we need to know what the "new values" are and we draw#
        # 0's to pad the blank space until the point where we add in 1's to extend the current line backwards until it's 10 long
        ## E.g. if current power draw is 9, it's "9 x 0's a 1" (Adding in extension of 1 backwards)
        # then the current power draw of 9 ones and a 0 current power draw)
        
        for line in range(0,(len(power_display))):
            length = current_power_display_temp[line]
            
            if length == 10:
                power_display[line] += (['B'] * 10)
                power_display[line] += (['C'] * 10)
            elif length == 0:
                # Pad all 1's
                power_display[line] += (['C'] * 10)
                power_display[line] += (['B'] * 10)
            else:
                power_display[line] += (['B'] * (length))
                power_display[line] += (['C'] * 10)
                power_display[line] += (['B'] * (10 - length))
                
        ## Weaking - I did all the work, but 10 dots is too much, let's strip some out:      
        for line in range(0,len(power_display)):
            power_display[line].pop(19)
            power_display[line].pop(18)
            power_display[line].pop(17)
            power_display[line].pop(15)
            power_display[line].pop(13)
            power_display[line].pop(12)
            power_display[line].pop(11)
        
  
        ## Set the pens we want to use:
        fg_pen = settings.PURPLE
        bg_pen = settings.BLACK
        
        for shift in range(12,-1,-1):
            for y in range(0,len(power_display)):
                for x in range(0,10):
                    if power_display[y][(shift+x)] == 'C':
                        graphics.set_pen(fg_pen)
                    else:
                        graphics.set_pen(bg_pen)
                    graphics.pixel(x,y+1)         
            settings.gu.update(graphics)
            await asyncio.sleep_ms(75)
        
        current_power_display = []
        current_power_display += current_power_display_temp

        
    ## Finally tidy up and change the top bar:
    if total_energy >= 5000:
        graphics.set_pen(settings.RED)
    elif total_energy >=500:
        graphics.set_pen(settings.YELLOW)
    elif total_energy > 0:
        graphics.set_pen(settings.GREEN)
    else:
        graphics.set_pen(settings.WHITE)
    
    graphics.line(0, 0, 10, 0)
    
## Storage vars for actual energy data
energy_stats = {}
total_energy = 0


async def handle_energy(graphics, string_topic, string_message):
    
    ## Take a topic + message for a power stat and store it
    global  energy_stats, total_energy
       
    if "current_demand" in string_topic: ## "Current Demand" is the total energy draw from Octopus, store it
        total_energy = int(float(string_message))
        await draw_power_chase(graphics)
    
    else: ## Otherwise, it's a device specific power stat, store it
        messagestat = int(float(string_message))
        energy_stats.update({string_topic : messagestat})
