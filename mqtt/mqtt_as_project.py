'''
An alternative is to use mip at the REPL with WiFi connected:

>>> import mip
>>> mip.install("github:peterhinch/micropython-mqtt")

'''

from mqtt_as import MQTTClient, config
import asyncio

mqtt_server = b'73a3246b4410491692df6b23c34b84cc.s1.eu.hivemq.cloud'
port = 8883
user = b'noturno'
pwd = b'Cotuca25'
# Local configuration
config['ssid'] = 'casa'  # Optional on ESP8266
config['wifi_pw'] = ''
config['server'] = mqtt_server  # Change to suit e.g. 'iot.eclipse.org'
config['user'] = user
config['password'] = pwd
config['ssl'] = True
config['ssl_params'] = {"server_hostname": mqtt_server}

async def messages(client):  # Respond to incoming messages
    # If MQTT V5is used this would read
    # async for topic, msg, retained, properties in client.queue:
    async for topic, msg, retained in client.queue:
        print("dd", topic.decode(), msg.decode(), retained)

async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        await client.subscribe('foo_topic', 1)  # renew subscriptions

async def main(client):
    await client.connect()
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))
    n = 0
    while True:
        await asyncio.sleep(5)
        print('publish', n)
        # If WiFi is down the following will pause for the duration.
        await client.publish('result', '{}'.format(n), qos = 1)
        n += 1

config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
