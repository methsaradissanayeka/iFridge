#--------------------------------------------------------------------------------------------------------
# PROJECT     		: iFridge
# FILE NAME   		: main.py
# LANGUAGE			: Micropython
# AUTHOR			: METHSARA DISSANAYEKA
# CONTRIBUTION     : DINITHI DILSHANI
#                    VIRAJ PRIYAMANTHA
# DATE				: 2023/05/22
# ASSOCIATED WITH	: SLTC Research University
# REVISION HISTORY :
#			- Initial version
#			- With door sensor 
# LICENSE			: MIT License
# DESCRIPTION		: This project related to internet of things based refrigerator monitoring system. 
# -------------------------------------------------------------------------------------------------------

from hcsr04 import HCSR04
from time import sleep

ir= machine.Pin(4, machine.Pin.IN)

dsensor = HCSR04(trigger_pin=13, echo_pin=15, echo_timeout_us=10000)

def connect_mqtt():
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server)

  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    if (time.time() - last_message) > message_interval:
      sensor.measure()
      temp = sensor.temperature()
      hum = sensor.humidity()
      dis = int (dsensor.distance_cm())
      tempint = int (sensor.temperature())
      
      temp = (b'{0:3.1f}'.format(temp))
      hum =  (b'{0:3.1f}'.format(hum))
    
      print('Temperature: %s' %temp, 'Humidity: %s' %hum , 'Distance: %s' %dis)
      if (dis < 5) & (tempint < 8):
          print('Coke is available')
          client.publish(TOPIC_PUB_NOT, 'Coke is Available')
      else:
          print('Coke is not available')
          client.publish(TOPIC_PUB_NOT, 'Coke is not available')
      client.publish(TOPIC_PUB_TEMP, temp)
      client.publish(TOPIC_PUB_HUM, hum)
      last_message = time.time()
      if ir.value() == 1:
        print("Door Opened")
        client.publish(TOPIC_PUB_DNOT, 'Door is not closed')
      else:
        client.publish(TOPIC_PUB_DNOT, '') 
      send_temp(tempint)
      print("Data Uploaded")
      print()
      
  except OSError as e:
    restart_and_reconnect()
