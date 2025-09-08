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
import json

def sub_cb(topic, msg):
    global led_y
    global led_r
    global led_g
    print(f'{topic} send {msg}')
    try:
        msg_dec = json.loads(msg)
        if "led_y" in msg_dec:
            led_y.value(msg_dec["led_y"]) 
        if "led_g" in msg_dec:
            led_g.value(msg_dec["led_g"]) 
        if "led_r" in msg_dec:
            led_r.value(msg_dec["led_r"]) 
    
    except ValueError as e:
        print(f"erro ao decodificar {e}" )

def check_msg(client, c):
    print(c)
    while True:
        client.wait_msg()


try:
    c = MQTTClient(
        client_id,
        mqtt_server,
        port = port,
        user = user,
        password = pwd,
        ssl = True,
        ssl_params = {"server_hostname": mqtt_server}       
        )
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (mqtt_server, TOPIC))
    print('Conectou ao Broker')
    _thread.start_new_thread(check_msg,(c ,"certo"))
except OSError as e:
    print(f'Erro ao conectar {e}')
    sleep(3)
    machine.reset()

try:
    while 1:
       # micropython.mem_info()
#       c.wait_msg()
       pass
finally:
    c.disconnect()
    
    

