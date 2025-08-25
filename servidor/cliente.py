import network
from time import sleep
try:
    import usocket as socket
except:
    import socket
    

import esp    ## biblioteca especifica para esp
import gc     # biblioteca para garbage collector

esp.osdebug(None)
gc.collect()

# define em qual rede deseja conectar
SSID = 'Wokwi-GUEST'
pwd  = ''

# inicializando o WiFi
sta = network.WLAN(network.STA_IF)
sta.active(True)
print(sta.scan())
sta.connect(SSID, pwd)
    
while not sta.isconnected():
    print('.',end='')
    sleep(1)
    
## imprime os dados da conexao WiFi caso conectado
print(f'Conectado a rede {SSID} no endereço :')
print(sta.ifconfig())

HOST = 'www.sergio.dev.br'
PORT = 80


PORT = 80
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(( HOST, PORT ))
    print('Conectado')    
    # monta a requisicao HTTP para o site
    request = f'GET /vciot HTTP/1.1\r\nHost: {HOST}\r\n\r\n'
    
    sock.sendall(request)
    print('Enviando requisicao HTTP GET')
    data = sock.recv(1024)
    print(data.decode())
    
except OSError as e:
    print(f'Socket error {e}')

finally:
    if sock:
        sock.close()
        print('Fechada a conexão')