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
import utils

# Local configuration
config = connectivity.config

## Display instances and global variable loads
# gu = settings.gu
# graphics = settings.graphics

## Import these here for now, there's a load of references that point back to "settings.gu and settings.graphics", will refactor later
gu = utils.gu
graphics = utils.graphics

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

    if any(entry in string_topic for entry in settings.topic_network):
        asyncio.create_task(dn.handle_network(graphics, string_topic, string_message))
    elif any(entry in string_topic for entry in settings.topic_dns):
        ## Don't need an async for this as we're just modifying an array in memory, there's already an async task for blinkies
        if settings.dns_use_mqtt:
            db.handle_dns(string_topic, string_message)
        else:
            pass
    elif any(entry in string_topic for entry in settings.topic_power): 
        asyncio.create_task(dp.handle_energy(graphics,string_topic,string_message))
    else:
        print(f"Unused message: {string_topic, string_message}")

## Connection Handler - essentially just "Subscribe to these topics")
async def conn_han(client):
    await client.subscribe(connectivity.mqtt_topic, 1)

## MQTT config options, configured down here as it needs callback/conn_han to exist
#MQTTClient.DEBUG = True  # Optional: print diagnostic messages
config['subs_cb'] = callback
config['connect_coro'] = conn_han
client = MQTTClient(config)

## This will be the main client loop
async def main(client):

    ##
    ## One off actions for Setup
    ##

    ## Init the array for the blinkies DNS section
    db.init_dotgrid()
    ## Load the main display segment dividers
    ds.draw_gridline_vert(graphics)

    ## Wait for the Wifi to come up and the MQTT client to connect
    await client.connect()
    ## Update the clock, need the client connect first for network connectivity
    dc.set_time()

    ## Set up the blinkies to update outside of MQTT response as they're not directly related
    asyncio.create_task(db.update_dotgrid_display(graphics))
    
    ## Clock maintenance task
    asyncio.create_task(dc.print_clock(graphics))
    
    ## End - One off actions

    ## And the main wait for MQTT, callbacks will trigger what it needs
    while True:
        await asyncio.sleep(1)



## And finally, kick off the async mqtt client loop
try:
    asyncio.run(main(client))
finally:
    client.close() 
