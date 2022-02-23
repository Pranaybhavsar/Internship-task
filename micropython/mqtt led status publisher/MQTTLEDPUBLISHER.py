from umqtt.simple import MQTTClient
import network
import esp
import machine
esp.osdebug(None)

led = machine.Pin(5,machine.Pin.OUT)
led.off()

import gc
gc.collect()

def on_connect(rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                
        Connected = True                
 
    else:
 
        print("Connection failed")
 
Connected = False   
ssid = 'SKP'
password = '02062001@'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())


broker_address= "14.97.22.54"
port = 1883
user_id = "admin"
password_id = "password"

#mqtt configuration

client= MQTTClient("umqtt_client",broker_address,user=user_id,password=password_id)
client.connect()
print('Connected to %s MQTT broker' % (broker_address))

import socket

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80)) # specifies that the socket is reachable 
#                 by any address the machine happens to have
s.listen(5)     # max of 5 socket connections

# ************************
# Function for creating the
# web page to be displayed
def web_page():
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  html = """<html><head> <title>ESP8266 Web Server in Micropython</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #8A2BE2; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 25px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>ESP32/8266 Web Server in Micropython</h1> 
  <p>LED state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
  <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
  return html



while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  if led_on == 6:
    print('LED ON')
    led.value(1)
    client.publish("python/test",'LED ON')
  if led_off == 6:
    print('LED OFF')
    client.publish("python/test",'LED OFF')
    led.value(0)
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()