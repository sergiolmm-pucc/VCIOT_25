from simple import MQTTClient


import network
from time import sleep
from machine import Pin
import time
import _thread


led_g = Pin(27,Pin.OUT)
led_r = Pin(12,Pin.OUT)
led_y = Pin(14,Pin.OUT)

rede = network.WLAN(network.STA_IF)
rede.active(True)

rede.connect("Wokwi-GUEST", '')
while not rede.isconnected():
    print('.', end='')
    sleep(1)

print(f'Conectado ao ip {rede.ifconfig()[0]}')
# parametrizar o mqtt client e sua conexao com Broker Hivemq
mqtt_server = b'73a3246b4410491692df6b23c34b84cc.s1.eu.hivemq.cloud'
port = 8883
user = b'noturno'
pwd = b'Cotuca25'

import machine
import ubinascii
client_id = ubinascii.hexlify(machine.unique_id())

TOPIC = b'aula0509ns'


btnY = Pin(4, Pin.IN, Pin.PULL_UP)
btnR = Pin(0, Pin.IN, Pin.PULL_UP)
btnG = Pin(2, Pin.IN, Pin.PULL_UP)

estadoR = False
estadoG = False
estadoY = False
# Initialize last_press_time for debouncing
def PinId(pin):
    return int(str(pin)[4:6].rstrip(")"))

# Interrupt Service Routine (ISR) - this function runs when the interrupt is triggered
def button_handler(pin):
    global estadoR
    global estadoY
    global estadoG
    global client
    global last_press_time
   
    # Debounce: only process if enough time has passed since the last press
    # This helps prevent multiple triggers from a single physical button press
    current_time = time.ticks_ms()
    if (current_time - last_press_time) > 200: # 200ms debounce
        msg="1"
        if PinId(pin) == 2:    
         if not estadoY:
             msg= b'{"led_y" : 1}'             
         else:
            msg= b'{"led_y" : 0}'
         estadoY = not estadoY   
        if PinId(pin) == 0:    
         if not estadoR:
             msg= b'{"led_r" : 1}'
         else:
            msg= b'{"led_r" : 0}'
         estadoR = not estadoR   
        if PinId(pin) == 4:    
         if not estadoG:
             msg= b'{"led_g": 1}'
         else:
            msg= b'{"led_g": 0}'
         estadoG = not estadoG
        print(msg)
        client.publish(TOPIC, msg)
        last_press_time = current_time



last_press_time = 0

# Attach the interrupt to the button pin
# Pin.IRQ_FALLING means trigger when the pin goes from HIGH to LOW (button pressed with pull-up)
btnY.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)
btnR.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)
btnG.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)



try:
    client = MQTTClient(
        client_id,
        mqtt_server,
        port = port,
        user = user,
        password = pwd,
        ssl = True,
        ssl_params = {"server_hostname": mqtt_server}       
        )
    # Subscribed messages will be delivered to this callback
    client.connect()
    print("Connected to %s, publish to %s topic" % (mqtt_server, TOPIC))
    print('Conectou ao Broker')
except OSError as e:
    print(f'Erro ao conectar {e}')
    sleep(3)
    machine.reset()

try:
    while 1:
       # micropython.mem_info()
       pass
except KeyboardInterrupt:
    print('parou')

finally:
    client.disconnect()
