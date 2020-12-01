# mutex-multicast

# UNLa - Sistemas Operativos - TP 3 - GRUPO 5
*******************************************

1) Primero debe configurarse la interfaz de red para multicast, ya que los mensajes se envian por este medio.

	# bash setup_enviroment.sh

2) Luego podremos correr el script de python

	$ python multicast_mutex.py

3) Si queremos correr otro proceso en otra consola del mismo equipo (ya que utiliza el nombre del host para identificarse), deberemos ejecutar el segundo script que es una copia pero con el nombre del host hardcodeado:

	$ python multicast_mutex_otro.py
