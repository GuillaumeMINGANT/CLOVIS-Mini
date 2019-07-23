import time
import serial
from detect_USB import find_arduino


POS1 = 1000
POS2 = 30
TIMEE = 0.1
TIMES = 0.1

def pos_to_byte(pos :int) -> [int, int]:
	lsb = pos%256
	msb = (pos - lsb) // 256
	return [msb,lsb]

ser = serial.Serial(find_arduino(), 115200)
count = 0

#while count < 5:

	##ser.write(bytes('Bonjour!;', "ASCII"))
	
	## ENVOI POSITION MAXIMALE -- POS1
	##ENVOI 1
	#msg = []
	#i = 2
	#while i<=5:
	
		#msg += [i] + pos_to_byte(POS1)
		#i= i +1
	
	#ser.write(msg)
	#time.sleep(TIMEE)	
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)
		

	##ENVOI 2
	#msg = []
	#while i<=9:
	
		#msg += [i] + pos_to_byte(POS1)
		#i= i +1
	#ser.write(msg)
	#time.sleep(TIMEE)	
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)
	
	##ENVOI 3
	#msg = []
	#while i<=13:
	
		#msg += [i] + pos_to_byte(POS1)
		#i= i +1
	#ser.write(msg)
	#time.sleep(TIMEE)	
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)
	
	##ENVOI 4
	#msg = []
	#while i<=17:
	
		#msg += [i] + pos_to_byte(POS1)
		#i= i +1
	#ser.write(msg)
	#time.sleep(TIMEE)	
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)
	
	##ENVOI 5
	#msg = []
	#while i<=20:
	
		#msg += [i] + pos_to_byte(POS1)
		#i= i +1
	#ser.write(msg)
	#time.sleep(TIMEE)	
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)
	
	##ENVOI 6
	#msg = []
	#while i<=23:
	
		#msg += [i] + pos_to_byte(POS1)
		#i= i +1
	#ser.write(msg)
	
	#time.sleep(TIMEE)
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)

	## ENVOI POSITION MINIMALE -- POS2
	##ENVOI 1
	#msg = []
	#i = 2
	#while i<=5:
	
		#msg += [i] + pos_to_byte(POS2)
		#i= i +1
	
	#ser.write(msg)
	#time.sleep(TIMEE)	
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)
	
	##ENVOI 2
	#msg = []
	#while i<=9:
	
		#msg += [i] + pos_to_byte(POS2)
		#i= i +1
	#ser.write(msg)
	#time.sleep(TIMEE)	
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)
	
	##ENVOI 3
	#msg = []
	#while i<=13:
	
		#msg += [i] + pos_to_byte(POS2)
		#i= i +1
	#ser.write(msg)
	#time.sleep(TIMEE)	
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)
	
	##ENVOI 4
	#msg = []
	#while i<=17:
	
		#msg += [i] + pos_to_byte(POS2)
		#i= i +1
	#ser.write(msg)
	#time.sleep(TIMEE)	
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)
	
	##ENVOI 5
	#msg = []
	#while i<=20:
	
		#msg += [i] + pos_to_byte(POS2)
		#i= i +1
	#ser.write(msg)
	#time.sleep(TIMEE)	
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)
	
	##ENVOI 6
	#msg = []
	#while i<=23:
	
		#msg += [i] + pos_to_byte(POS2)
		#i= i +1
	#ser.write(msg)
	
	#time.sleep(TIMEE)	
	#ser.write(bytes(';', "ASCII"))
	#time.sleep(TIMES)	
	#print(msg)
	#count += 1
	##msg = [11] + pos_to_byte(0)
	##msg += [12] + pos_to_byte(0)
	##msg += [13] + pos_to_byte(0)
	##msg += [14] + pos_to_byte(0)
	##ser.write(msg)
	##time.sleep(0.1)	
	##ser.write(bytes(';', "ASCII"))
	##time.sleep(0.5)	
	##print(msg)

nb_motor = 23     

#while True:
for i in range(5):
	buff = []
	msg = [255,255,255,22,254,254,254]
	ser.write(msg)
	time.sleep(0.11)
	print(msg)
	while ser.in_waiting != 0: 
		caract = int.from_bytes(ser.read(), byteorder='big')           
		buff += [caract]
		#print(caract)
	print(buff)
	time.sleep(1)	

	
	msg = []
	msg = [255, 255, 255]
	i = 2
	while i <= nb_motor:
		msg += [i] + pos_to_byte(30)
		i = i +1
	msg += [254, 254, 254]
	
	ser.write(msg)
	#ser.flush()
	#time.sleep(0.01)
	#ser.write(msg[30:])
	
	
	time.sleep(1)	
	print(msg)
	
	
	msg = []
	msg = [255, 255, 255]
	i = 2
	while i <= nb_motor:
		msg += [i] + pos_to_byte(1000)
		i = i +1
	msg += [254, 254, 254]
	
	ser.write(msg)
	#ser.flush()
	#time.sleep(0.01)
	#ser.write(msg[30:])
	
	time.sleep(1)	
	print(msg)

#from subprocess import check_output
#wifi_ip = check_output(['hostname', '-I'])
#wifi_ip = wifi_ip.decode("utf-8")[:-2].split(" ")
#for i in wifi_ip:
	#if i == '192.168.50.1':
		


