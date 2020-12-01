# import socket programming library 
import socket 
import struct
import time

# import thread module 
import threading 

# Para esperar tiempo random
from random import randint
from time import sleep

# Datos de multicast - requiere ejecutar antes setup_enviroment.sh  
MCAST_GRP = '224.0.0.1'
MCAST_PORT = 10000

# Nombre del EQUIPO - Hardcodear en una copia del script para usar 2 procesos en el mismo equipo y notar la diferencia
HOSTNAME = 'OTRO'

# Contador para saber cuantos nodos hay activos
count_hello = 0
# Contador de respuestas cuando necesito usar un recurso
count_use_it = 0
# Flag si estoy usando el recurso
using_resource = False
# Flag para saber si debo notificar que termine de usar el recurso
notify_release = False

# Contador de numero de mensaje de multicast enviado
msg_count = 0

# Socket de escucha
listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
listen_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Socket de respuesta
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    

print_lock = threading.Lock() 

def send(msg): 
    global msg_count
    msg_count += 1
    fecha = time.strftime("%Y/%m/%d %H:%M:%S")
    send_sock.sendto(HOSTNAME + " : " + msg + " : " + "#" + str(msg_count) + " - " + fecha, (MCAST_GRP, MCAST_PORT))  

def say_hello():
     send("HELLO")

def ask_hello(): 
    global count_hello
    count_hello = 0
    send("SAY_HELLO")

def ask_resource():
    global count_use_it
    count_use_it = 0
    send("CAN_I_USE")

def yes_resource(): 
    send("YES_USE")

def notify_lock(delay):
    send("Usando el recurso, demora " + str(delay))

# thread de escucha, actua segun el mensaje recibido 
def listen_thread(): 

    global count_hello
    global count_use_it
    global using_resource
    global notify_release

    while True: 
        # data received from client 
        data = listen_sock.recv(1024)
        host, msg, count = data.split(' : ')
        if host == HOSTNAME: 
            print("Mi mensaje : " + msg+ " : " + count)
        else: 
	    if msg == 'SAY_HELLO': 
                say_hello()
            elif msg == 'HELLO':
                count_hello += 1
            elif msg == 'CAN_I_USE':
                if not using_resource:
                    yes_resource()
                else: 
                    notify_release = True
            elif msg == 'YES_USE':
                count_use_it += 1
            print data

# Cada cierto tiempo intento usar el recurso ficticio
def ask_thread():	

    global notify_release
    global using_resource

    while True:
        sleep(randint(5,20))
        if not using_resource:
            ask_hello()
            sleep(1)
            ask_resource()

            # Espero hasta tener el OK de todos
            while count_hello > count_use_it:
                sleep(0.05)

            # Hago un uso FAKE del recurso un tiempo random
            using_resource = True
            demora = randint(30,60)
            notify_lock(demora)
            sleep(demora)
            using_resource = False

        if notify_release:
            notify_release = False
            yes_resource()

def Main(): 
    
    listen = threading.Thread(target=listen_thread)
    listen.start()

    send = threading.Thread(target=ask_thread)
    send.start()
    
  
if __name__ == '__main__': 
    Main() 
