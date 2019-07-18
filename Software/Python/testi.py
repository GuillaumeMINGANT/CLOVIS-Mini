with open("motors_settings", "r") as content:
	motors_settings = {}
	content = [i.split("=") for i in content.read().split("\n")]
	for i in content:
		motors_settings[i[0]] = i[1].split(",")
		for j, e in enumerate(motors_settings[i[0]]):
			motors_settings[i[0]][j] = int(e)
	print(motors_settings)
