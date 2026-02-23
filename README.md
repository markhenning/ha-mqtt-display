# Home Assistant MQTT Galactic Unicorn Display

This project collects data from Home Assistant and uses it to update a Pimoroni Galactic Unicorn at appropriate times.
Please note - due to this being a learning/practice project, no AI has been used

**Displayed Data** 

From left to right
1. House Power usage, updates every 15 seconds
    Top bar - overall house usage, green is less than 500W, red more than 3KW, yellow inbetween)
    Below - Distribution by device (PC, Home Lab, Router, Kettle etc)
2. Internet Connection Load - Upload and Download
3. DNS Query Rate - More dots is more queries/min, blue are successful, yellow are ad-blocked, red are fails
4. Clock with dot graph updated every second to display current time

**Design Goals**
1. Simple updates (e.g. colours, text strings to adjust to different houses etc)
2. Modular setup to allow for replacement of a section without impacting other sections
3. Minimal interactions to maintain, should be set and forget

Full Docs:
 - [Overview and Internal Setup](https://markhenning.github.io/mqtt-ha-display/MQTT-HA-Display)
 - [Guide to Exporting Data from MQTT](https://markhenning.github.io/mqtt-ha-display/Exporting-with-MQTT)
 - [Adjusting Common Variables](https://markhenning.github.io/mqtt-ha-display/MQTT-HA-Adjustments)
