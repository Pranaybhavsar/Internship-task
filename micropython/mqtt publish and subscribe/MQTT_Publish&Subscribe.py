from umqtt.simple import MQTTClient
from machine import Pin
import network
import machine
import ubinascii
import time
 
led = Pin(5, Pin.OUT)
pin = machine.Pin(2, machine.Pin.OUT)
led.off()
ssid = 'SKP'
password = '02062001@'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

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

def listen():
    #instance of MQTTClient 
    client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])
    client.set_callback(onMessage)
    client.connect()
    client.publish("test2", "ESP8266 is Connected")
    client.subscribe(CONFIG['TOPIC'])
    print("ESP8266 is Connected to %s and subscribed to %s topic" % (CONFIG['MQTT_BROKER'], CONFIG['TOPIC']))
    

    try:
        while True:
            #msg = client.wait_msg()
            msg = (client.check_msg())

            if led.value() ==  1:
                client.publish("test2", b"LED is On")
            else: 
                client.publish("test2", b"LED is Off") 
            time.sleep(10)

                
    finally:
        client.disconnect()  

listen()        