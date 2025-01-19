import settings
import asyncio
import random

## DNS Blinkies Overview
##
## Sets up a dotgrid which maps to a section of the display
## Add dots of each colour set at "minimum"
## Start an async loop to update the display (reduce levels by 1 each time, and when 0 mark them as blank.)
##
## "desired" is the key part - adjusting this will cause dots to be added/removed as the loop runs

## Load in Settings

## Pull in colours from the globals files
dns_colours = settings.dns_colours
## Min/maxblinks for each colour
maxes = settings.dot_maxes
mins = settings.dot_mins

## X starting location for grid when drawn on display
# Note - "dotgrid" is internal array of 0 -> 11, we display it starting with at column specified
start_x = settings.dns_start_x

### Mapping - this maps the MQTT message string to look for with which colour dict to use later for display
colour_map = settings.dns_colour_map
scales = settings.dns_scale_factors

## Internal counts, don't change these
desired = mins.copy()
dotgrid = []
blanks_queue = []  # Holds (x,y) co-ordinates of unused/blank dots

## Generate the count dict to track number of each colour dot
count = {}
for colour in mins.keys():
    count[colour] = 0

## Basic object to hold all the info for a dot/pixel
class Dot:
  def __init__(self, colour, level):
    self.colour = colour
    self.level = level

## Init function - called once to set up the 10x11 array of Dots
def init_dotgrid():
    global dotgrid
    global blanks_queue

    ## Fill the dotgrid with Dots of setting (first colour in the colour array, level 0), and mark them all as "blank"
    dotgrid = [[Dot(next(iter(dns_colours)),0) for y in range(0,settings.height)] for x in range(0,settings.dns_width)]
    for x in range(0,settings.dns_width):
        for y in range(0,settings.height):
            dotgrid[x][y] = Dot(next(iter(dns_colours)),0)
            ## Mark the pixel as blank and available
            blanks_queue.append([x,y])


## Function to check if the actual number of dots is less than "desired", add missing ones
def check_rates_up():
    for colour in count.keys():

        if count[colour] < desired[colour]:
            for i in range(desired[colour] - count[colour]):
                #print(f"Correcting to add {colour}")
                add_dot(colour)

# Function to add a dot of the desired colour, it'll work out the location to put it in and check if we're over max/under min
def add_dot(colour):
    global blanks_queue
    global dotgrid

    if len(blanks_queue) < 1:
        print("ERROR - No room to add new pixel")
    else:
        index = random.randint(0, (len(blanks_queue) - 1))

        # Check we're not "over budget" and then add the dot
        if count[colour] < maxes[colour]:
            temp_x, temp_y = blanks_queue.pop(index)
            dotgrid[temp_x][temp_y]= Dot(colour,4)
            count[colour] += 1
            #print(f"Adding {colour}")
        else:
            print(f"ERROR - Already at max for {colour}")

# Unused function - 5% chance that to update the "desired" array with suitable random numbers
def randomise_desired():
    global desired
    
    if random.randint(0,20) == 1:
        for response in colour_map.keys():
            c = random.randint(mins[colour_map[response]], maxes[colour_map[response]])
        desired[response] = c
        print("Updated desired numbers")
        print(desired)

## Loop to drop the colour levels once every 0.4 seconds:
async def update_dotgrid_display(graphics):
    global blanks_queue
    global dotgrid
    global desired
    
    while True:
        
        ## If we're set to not use mqtt, generate appropriate data randomly
        if not settings.dns_use_mqtt:
            randomise_desired()
    
        ## Check if we've got the right amount of dots, add if we don't
        check_rates_up()
        
        ## Scan the array and adjust levels as needed
        for x in range(0, settings.dns_width):
            for y in range(0, settings.height):
                
                # For levels that will change to zero
                if dotgrid[x][y].level == 1:
                        
                        # Drop the dot level and write back to the dotgrid
                        dotgrid[x][y].level -= 1
                        
                        # Update the pixel colour
                        new_colour = (dns_colours[current_dot.colour])[0]
                        graphics.set_pen(new_colour)
                        graphics.pixel((start_x+x),y)
                        
                        # Mark cell as blank and available for use
                        blanks_queue.append([x,y])
                        count[(dotgrid[x][y].colour)] -= 1

                        # Only add a new dot to replace if we're below the desired number of those dots (we just removed this one from use (and the count)
                        if (count[current_dot.colour] < desired[current_dot.colour]):
                            add_dot(current_dot.colour)
                        else:
                            pass
                            #print(f"Dropping {current_dot.colour}")

                ## Other levels, just drop by one
                if 1 < (dotgrid[x][y].level) <= 4:
                    current_dot = dotgrid[x][y]
                    graphics.set_pen(dns_colours[current_dot.colour][current_dot.level])
                    graphics.pixel((start_x+x),y)
                    dotgrid[x][y].level -= 1
                    
        
        ## Draw out the changes we've made
        settings.gu.update(graphics)            
        await asyncio.sleep(0.4)

## Function to adjust amount of dots based on MQTT messages
## This is a lot of copy/paste for logic, I can tighted it up by using colour_map.keys, but if anyone ever wants to add something new/adjust individual rates, this is the best way to demo it

def handle_dns(string_topic, string_message):
    ## HA sometimes provides "unavailable" if one of the source connections fails (e.g. cert expires) - this skips it
    if "unavailable" in string_message:
        pass
    
    ## Loop the expected DNS responses (no_error , blocked, servfail) and if so, scale the number we got to change the number of blinks
    ## Also - make sure the number of blinks is between max and min required
    found = False
    for response in colour_map.keys():
        
        if response in string_topic:
            scaled_response = int(float(string_message)) // scales[response]
            
            if scaled_response <= mins[(colour_map[response])]:
                new_count = mins[colour_map[response]]
            
            elif mins[colour_map[response]] < scaled_response <= maxes[colour_map[response]]:
                new_count = scaled_response
            
            else:
                new_count = maxes[colour_map[response]]
            #print(f"Updating new values for {colour_map[response]} to {new_count}")
            desired[colour_map[response]] = new_count
            found = True
    
    if not found:
        ## Got a DNS response code that doesn't match a known response, ignore it
        #print(f"I don't know what to do with {string_topic} {string_message}")
        pass   


