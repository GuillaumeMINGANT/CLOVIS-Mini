with open("server_settings", "r") as content:
	server_settings = {}
	content = [i.split("=") for i in content.read().split("\n")]
	for i in content:
		server_settings[i[0]] = i[1]
	print(server_settings["server_ip"])
