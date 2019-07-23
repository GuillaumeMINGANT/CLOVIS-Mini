with open("motors_id", "r") as content:
	motors_settings = {}
	content = [i.split("=") for i in content.read().split("\n")]
	for i in content:
		if(len(i) == 2):
			motors_settings[i[0]] = i[1]
		
	print(motors_settings)
