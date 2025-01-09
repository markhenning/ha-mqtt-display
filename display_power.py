import math
import settings as settings
import asyncio

current_displayed_power = []

def blank_power(graphics):
    global current_displayed_power
    print(current_displayed_power)
    # current_displayed_power contains an integer list of the displayed power, we're going to animate this
    
    ## We've got 10 linesof LEDs, but might not have 10 values for power, that's fine, pad the list out
    while len(current_displayed_power) < 10:
        current_displayed_power.append(0)

    ## list is already sorted by value, so we should be able to just pull the last value:    
    start = current_displayed_power[-1]
    
    added = 1
    ## Add as many extra dots as needed to make all 10 lines completely full
    while added <= (10 - start):
        current_line = 1
        # Loop the lines, adding 1 dot every time until we get 10
        for linelength in current_displayed_power:
            end = linelength + added
            print(end)
            if end > 10:
                end = 10
            graphics.set_pen(settings.PURPLE)
            graphics.line(0, current_line, end, current_line)
            current_line = current_line + 1
        
        ## Update LEDs after each additional dot
        gu.update(graphics)
        await asyncio.sleep_ms(100)
        added = added + 1
    
    ## Do the "black column chaser" to clear out the display, left -> right, add one black column and repeat
    blankcol = 0
    while blankcol < 10:
        graphics.set_pen(settings.BLACK)
        graphics.line(blankcol, 1, blankcol, 11)
        blankcol = blankcol + 1
        gu.update(graphics)
        await asyncio.sleep_ms(100)
        


async def draw_power_chase(graphics):
    global current_displayed_power
    #print(current_displayed_power)
    # current_displayed_power contains an integer list of the displayed power, we're going to animate this
    
    #print("Current displayed power length: " + str(len(current_displayed_power)))
    ## We've got 10 linesof LEDs, but might not have 10 values for power, that's line, pad the list out
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
    blank_power
    ## Going to pull out the "new" power display stats in here so we can use them later
    current_power_display_temp = []
    
    ## Let's do teh new stats first:
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
                #print("TEMPLINE")
                #print(templine)
                power_display.append(templine)
                #print(power_display[line_no])
                line_no = line_no + 1
                
        ## We've build the first third, next up, we need to know what the "new values" are and we draw#
        # 0's to pad the blank space until the point where we add in 1's to extend the current line backwards until it's 10 long
        ## E.g. if current power draw is 9, it's "9 x 0's a 1" (Adding in extension of 1 backwards)
        # then the current power draw of 9 ones and a 0 current power draw)
        
        #print("CURRENT POWER DISPLAY BEFORE USE")
        #for line in current_displayed_power:
        #    print(current_displayed_power[line])
        
        for line in range(0,(len(power_display))):
            length = current_power_display_temp[line]
            #print("LENGTH, then LINE")
            #print(length)
            #print(line)
            
            if length == 10:
                # Pad all 0's
                #print("length 10")
                #print(power_display[line])
                power_display[line] += (['B'] * 10)
                power_display[line] += (['C'] * 10)
                #print(power_display[line])
                #print("End Length10")
            elif length == 0:
                # Pad all 1's
                power_display[line] += (['C'] * 10)
                power_display[line] += (['B'] * 10)
            else:
                #print("LINE:")
                #print(power_display[line])
                power_display[line] += (['B'] * (length))
                power_display[line] += (['C'] * 10)
                power_display[line] += (['B'] * (10 - length))
                #print("MODIFIED TO:")
                #print(power_display[line])
                
                
        #print("POWER DISPLAY")
        #for lines in power_display:
        #    print(lines)
        
        ## Ok, we're all good, draw it out:
        # In this, there's 20 redraws (essentially moving 0,0 from  power_display[line][20] down to power_display[line][0]
        
        ## I did all the work, but 10 dots is too much, let's strip some out:
        
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
        #print("Current shift")
        #print(shift)
            for y in range(0,len(power_display)):
                for x in range(0,10):
                    #print("Looking at power_display, shift: " + str(shift) + ", x: " + str(x) + ", y: " + str(y))
                    #print(power_display[y][(shift+x)])
                    if power_display[y][(shift+x)] == 'C':
                        #print("Found C at " + str(shift) + ", x: " + str(x) + ", y: " + str(y))
                        graphics.set_pen(fg_pen)
                    else:
                        graphics.set_pen(bg_pen)
                    graphics.pixel(x,y+1)         
            settings.gu.update(graphics)
            await asyncio.sleep_ms(75)
        
        current_power_display = []
        current_power_display += current_power_display_temp
        #print("AFTER printing, current_power_display:")
        #print(current_power_display)
        #print(current_power_display_temp)
        
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



def draw_power_stats(graphics):
    
    global current_displayed_power
    
    await dp.blank_power(graphics)
    current_displayed_power.clear()
    
    ## OK, we're going to do some very arbitrary (sorry) things here.
    ## Top bar - total power usage, always, 10 wide, change colour depending on the value
    
    #print("TOTAL ENERGY:" + str(total_energy))
    #print(energy_stats)
    
    ## Clear the graph section
    graphics.set_pen(settings.BLACK)
    graphics.rectangle(1,0,9,11)
    
    ##Get the values out for easy sorting
    power_list = []
    for key in energy_stats:
        power_list.append(energy_stats[key])
        
    # Reverse Sort the list so we get the stats descending for the graphs
    power_list.sort(reverse=True)

    ## Top bar - 10 wide, red, yellow or green, depending on the value, if we haven't got it yet, white)

    if total_energy >= 5000:
        graphics.set_pen(settings.RED)
    elif total_energy >=500:
        graphics.set_pen(settings.YELLOW)
    elif total_energy > 0:
        graphics.set_pen(settings.GREEN)
    else:
        graphics.set_pen(settings.WHITE)
    
    graphics.line(0, 0, 10, 0)

    ## We may still not have the total energy counter (their minimum update time is 15 seconds, skip if we don't)
    if total_energy != 0:
        graphics.set_pen(PURPLE)
        line_no = 1
        for usage in power_list:
            ## We've only got 11 lines, so if we're over that, just give up
            if line_no == 12:
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
                graphics.line(0, line_no, (int(length)), line_no)
                line_no += 1
                current_displayed_power.append(int(length))
    gu.update(graphics)
    print("Displayed power...")
    print(current_displayed_power)