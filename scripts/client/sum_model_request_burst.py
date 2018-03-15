# request_burst
import requests, json, time, sys, numpy as np

iter = 1000
interval = 0.01
if len(sys.argv) >= 3:
	iter = int(sys.argv[1])
	interval = float(sys.argv[2])
elif len(sys.argv) >= 2:
	iter = int(sys.argv[1])

headers = {"Content-type": "application/json"}
clipper_url = "192.168.56.101" # default: "localhost"

latency_sum = 0
for i in range(iter):
	print "request: %4d" % i,
	start = time.time()
	print requests.post("http://"+clipper_url+":1337/hello-world/predict", 
		headers=headers, 
		data=json.dumps({"input": list(np.random.random(10))})).json()
	latency = time.time()-start
	print "latency: ", latency
	latency_sum += latency
	time.sleep(interval)

print "Average Latency:", latency_sum/iter
