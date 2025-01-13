from mqtt_as import MQTTClient, config
## WiFi/MQTT Settings - single quoted values please - e.g. 'my-wifi-network'

config['ssid'] = '<WiFI-SSID>'
config['wifi_pw'] = '<WiFi-Password'
config['server'] = '<MQTT-Server' 
config['user'] = '<MQTT-Username'
config['password'] = '<MQTT-Password'

## Don't forget the # on the end here to collect all of the entries
mqtt_topic = 'haexport/sensor/#'