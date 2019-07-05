
import time
import serial
 



ser = serial.Serial('/dev/ttyUSB0', 115200)

pos = 512
mop = 10
while True:
	#mip = 1
	#mop = ((mop+50)% 200)
	#message = bytes(str(mip) + ':' + str(mop)+';', "ASCII")
	#ser.write(message)
	#print(message)
	#time.sleep(0.09)
	#mip = 2
	#message = bytes(str(mip) + ':' + str(mop)+';', "ASCII")
	#ser.write(message)
	#print(message)
	#time.sleep(0.09)
	
	#message = bytes('0:2;', "ASCII")
	#ser.write(message)
	#print(message)
	#time.sleep(1)
	
	msg = ser.readline().decode("ASCII")[:-1]

	print(data)
	
	

	
	
	
	
	
	
	
	
		 
