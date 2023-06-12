#--------------------------------------------------------------------------------------------------------
# PROJECT     		: iFridge
# FILE NAME   		: boot.py
# LANGUAGE			: MicroPython
# AUTHOR			: METHSARA DISSANAYEKA
# CONTRIBUTION      :  DINITHI DILSHANI
#                      VIRAJ PRIYAMANTHA
# DATE				: 2023/05/22
# ASSOCIATED WITH	: SLTC Research University
# REVISION HISTORY :
#			- Initial version
#			- With door sensor
# LICENSE			: MIT License
# DESCRIPTION		: This project related to internet of things based refrigerator monitoring system. 
# -------------------------------------------------------------------------------------------------------

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
from machine import Pin
import dht
esp.osdebug(None)
import gc
gc.collect()
import urequests as requests


ssid = 'SLTC_STAFF'
password = 'CrossRoads@2022'
mqtt_server = '91.121.93.94' #Replace with your MQTT Broker IP
THINGSPEAK_API_KEY = "FUQAAI2QB80TJMP1"
THINGSPEAK_URL1 = "https://api.thingspeak.com/update?api_key=FUQAAI2QB80TJMP1&field1=0"

client_id = ubinascii.hexlify(machine.unique_id())
TOPIC_PUB_TEMP = b'esp/dht/temperature'
TOPIC_PUB_HUM = b'esp/dht/humidity'
TOPIC_PUB_DIS= b'esp/dht/distance'
TOPIC_PUB_NOT= b'esp/dht/notification'
TOPIC_PUB_DNOT= b'esp/dht/dnotifi'

last_message = 0
message_interval = 5

sensor = dht.DHT22(Pin(16))

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

def send_temp(data):
    response = requests.get(THINGSPEAK_URL1 + "&field1=" + str(data))
