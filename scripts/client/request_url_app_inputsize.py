# request_burst
import requests, json, time, sys, numpy as np

iter = 1000
interval = 0.01

headers = {"Content-type": "application/json"}
app_name = 'hello-world'
input_size = 10
clipper_url = "192.168.56.101" # default: "localhost"

if len(sys.argv) >= 4:
	app_name = sys.argv[1]
	input_size = int(sys.argv[2])
	clipper_url = sys.argv[3]
elif len(sys.argv) >= 3:
	app_name = sys.argv[1]
	input_size = int(sys.argv[2])
elif len(sys.argv) >= 2:
	app_name = sys.argv[1]


start = time.time()
print requests.post("http://"+clipper_url+":1337/"+app_name+"/predict", 
	headers=headers, 
	data=json.dumps({"input": list(np.random.random(input_size))})).json()
latency = time.time()-start
print "latency: ", latency
