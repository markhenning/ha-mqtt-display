from mqtt_as import MQTTClient, config
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY
import asyncio

## Reference other files for imports:
import connectivity
import display_setup as ds
import display_power as dp
import display_network as dn
import display_blinks as db
import display_clock as dc
import settings

# Local configuration
config = connectivity.config

## Display instances and global variable loads
gu = settings.gu
graphics = settings.graphics

## =========================
## Overview
## =========================
## We're going to set up an asyncio queue that will run various tasks that will perform, and then sleep until awoken again
## Some of these will be triggered by time (e.g. clock updates, blinking lights) - These we kick off and let run, then...
## Start the listener client for MQTT messages appearing on the queue (e.g. power stats update) and sleep for 1s
##
## It's a bit of a mess, but bear with me


## Call backs
## Function called whenever MQTT has a message, reads it and triggers the action based on content
def callback(topic, msg, retained, properties=None): 
    
    #print((topic.decode(), msg.decode(), retained))
     
    ## Make the data usable  
    string_topic = topic.decode()
    string_message = msg.decode()
    
    ## Decide what to do with it based on message topic:
    if "router_current" in string_topic:
        asyncio.create_task(dn.handle_network(graphics, string_topic, string_message))
    elif 'tdns_' in string_topic:
        ## Don't need an async for this as we're just modifying an array in memory, there's already an async task for blinkies
        db.handle_dns(string_topic, string_message)
        #pass
    elif ('power' or 'energy' in string_topic): 
        asyncio.create_task(dp.handle_energy(graphics,string_topic,string_message))

## Connection Handler - essentially just "Subscribe to these topics")
async def conn_han(client):
    await client.subscribe(connectivity.mqtt_topic, 1)

## MQTT config options, configured down here as it needs callback/conn_han to exist
config['subs_cb'] = callback
config['connect_coro'] = conn_han
#MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)

## This will be the main client loop
async def main(client):

    ## One off actions for Setup
    ## Init Tasks - One off tasks necessary needed on startup

    ## Init the array for the blinkies DNS section
    db.init_dotgrid()
    ## Load the main display segment dividers
    ds.draw_gridline_vert(graphics)

    ## Wait for the Wifi to come up and the MQTT client to connect
    await client.connect()
    ## Update the clock, need the client connect first for network connectivity
    dc.set_time()
    
    ## Time based update tasks
    ## =======================
    ## Set up the blinkies to update outside of MQTT response as they're not directly related
    asyncio.create_task(db.update_dotgrid_display(graphics))
    
    ## Clock maintenance task
    asyncio.create_task(dc.print_clock(graphics))
    
    ## And the main wait task for asyncio, MQTT callbacks will trigger what it needs
    while True:
        await asyncio.sleep(1)



## And finally, kick off the async mqtt client loop
try:
    asyncio.run(main(client))
finally:
    client.close() 
