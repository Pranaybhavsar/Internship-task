from umqtt.simple import MQTTClient
from machine import Pin
import machine
import ubinascii
 
led = Pin(5, Pin.OUT)
pin = machine.Pin(2, machine.Pin.OUT)

CONFIG = {
     "MQTT_BROKER": "14.97.22.54",
     "USER": "admin",
     "PASSWORD": "password",
     "PORT": 1883, 
     "TOPIC": b"test1",
     #unique identifier of the chip
     "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())
}
 
#Act based on message received   
def onMessage(topic, msg):
    print("Topic: %s, Message: %s" % (topic, msg))
 
    if msg == b"on":
        pin.off()
        led.on()
    elif msg == b"off":
        pin.on()
        led.off()
 

client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
client.set_callback(onMessage)
client.connect()
client.publish("test1", "ESP8266 is Connected")
client.subscribe(topic_sub)
print("ESP8266 is Connected to %s and subscribed to %s topic" % (, topic_sub))
 
try:
    while True:
        msg = client.wait_msg()
            
finally:
    client.disconnect()  
    